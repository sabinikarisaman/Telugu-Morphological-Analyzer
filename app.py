import re
from flask import Flask, render_template, request, jsonify
import morfessor
import sentencepiece as spm
import json

app = Flask(__name__)   # Initialize Flask application

# --- Load Data from Files ---
def load_json_data(filepath):
    """Load and parse a JSON file, or return None on error."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {filepath}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in {filepath}")
        return None

# Load and sort prefix/suffix lists and load sandhi rules & known roots
prefixes = load_json_data("prefixes.json") or []
prefixes = sorted(prefixes, key=len, reverse=True)   # Sort long-to-short for greedy matching
suffixes = load_json_data("suffixes.json") or []
suffixes = sorted(suffixes, key=len, reverse=True)
sandhi_rules = load_json_data("sandhi_rules.json") or {}
known_roots = set(load_json_data("known_roots.json") or [])
known_words = set(["ఇది", "ఒక"])  # Small built-in set of common words

# --- Load Morfessor and BPE models ---
try:
    morfessor_model = morfessor.MorfessorIO().read_binary_model_file("morfessor_telugu.model")
except FileNotFoundError:
    print("Error: Morfessor model file 'morfessor_telugu.model' not found.")
    morfessor_model = None

try:
    sp = spm.SentencePieceProcessor()
    sp.load("bpe_telugu.model")
except FileNotFoundError:
    print("Error: BPE model file 'bpe_telugu.model' not found.")
    sp = None

# --- Helper Functions ---
def apply_sandhi_rules(word):
    """Return list of subwords if a sandhi rule applies, else [word]."""
    return sandhi_rules.get(word, [word])

def extract_prefix(word):
    """
    Greedily find a prefix from 'prefixes';
    return (prefix, remainder) if found, else (None, word).
    """
    for prefix in prefixes:
        if word.startswith(prefix):
            remainder = word[len(prefix):]
            if len(remainder) > 1:
                return prefix, remainder
    return None, word

def extract_suffix(word):
    """
    Greedily find a suffix from 'suffixes';
    return (remainder, suffix) if found, else (word, None).
    """
    for suffix in suffixes:
        if word.endswith(suffix):
            remainder = word[:-len(suffix)]
            if len(remainder) > 1:
                return remainder, suffix
    return word, None

def morfessor_segment(word):
    """Use Morfessor to segment a word, or return [word] on error."""
    if morfessor_model is None:
        return [word]
    try:
        segments, _ = morfessor_model.viterbi_segment(word)
        return segments if len(segments) > 1 else [word]
    except Exception as e:
        print(f"Morfessor error: {e}")
        return [word]

def bpe_segment(word):
    """Use SentencePiece BPE to segment a word, or return [word] on error."""
    if sp is None:
        return [word]
    try:
        segments = sp.encode(word, out_type=str)
        # Clean up special markers
        segments = [seg.replace(" ", "").replace("▁", "") for seg in segments if seg.strip()]
        return segments if len(segments) > 1 else [word]
    except Exception as e:
        print(f"BPE error: {e}")
        return [word]

def is_reduplication(word):
    """Return True if 'word' is an exact two-part repetition."""
    n = len(word)
    if n % 2 == 0 and n > 4:
        half = n // 2
        return word[:half] == word[half:]
    return False

# --- Hybrid Morphological Analysis ---
def hybrid_analysis(word, is_sentence=False):
    """
    Perform full analysis:
    - If sentence, split on spaces/punctuation and analyze each token.
    - Apply sandhi, suffix/prefix extraction, known-root check,
      reduplication, then statistical fallback.
    - Label each segment with its role.
    """
    # Handle sentences by splitting on spaces/punct
    if is_sentence or " " in word or "." in word or "," in word:
        parts = re.split(r"([ .,])", word)
        results = []
        for part in parts:
            if part in [" ", ".", ","]:
                results.append(part)
            elif part:
                results.append(hybrid_analysis(part))
        return "".join(results)

    word = word.strip()
    if not word:
        return ""

    # Known small words as root
    if word in known_words:
        return f"{word}_Root"

    # 1. Sandhi rules
    sandhi_result = apply_sandhi_rules(word)
    if len(sandhi_result) > 1:
        parts = []
        for i, part in enumerate(sandhi_result):
            if i == len(sandhi_result) - 1 and part in suffixes:
                parts.append(f"{part}_Suffix")
            elif part in known_roots or part in known_words:
                parts.append(f"{part}_Root")
            else:
                parts.append(hybrid_analysis(part))
        return " + ".join(parts)

    # 2. Suffix extraction
    root, suffix = extract_suffix(word)
    if suffix:
        prefix, root_part = extract_prefix(root)
        if prefix:
            return f"{prefix}_Prefix + {root_part}_Root + {suffix}_Suffix"
        return f"{root}_Root + {suffix}_Suffix"

    # 3. Prefix extraction
    prefix, root_part = extract_prefix(word)
    if prefix:
        return f"{prefix}_Prefix + {root_part}_Root"

    # 4. Known-root check
    if root_part in known_roots or root_part in known_words:
        return f"{root_part}_Root"

    # 5. Reduplication check
    if is_reduplication(root_part):
        return f"{root_part}_Reduplication"

    # 6. Fallback to root
    return f"{word}_Root"

# --- Flask Routes ---
@app.route("/")
def index():
    """Serve the main HTML page."""
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    """
    Receive JSON POST with 'word';
    return JSON with 'input' and 'output'.
    """
    data = request.json
    word = data.get("word", "").strip()
    if not word:
        return jsonify({"error": "Please enter a Telugu word or sentence."})
    result = hybrid_analysis(word, is_sentence=True)
    return jsonify({"input": word, "output": result})

if __name__ == "__main__":
    app.run(debug=True)   # Run Flask in debug mode for development
