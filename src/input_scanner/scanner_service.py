from flask import Flask, request, jsonify
from llm_guard import scan_prompt
from llm_guard.vault import Vault
from llm_guard.input_scanners.prompt_injection import MatchType
from llm_guard.input_scanners import Anonymize, Toxicity, TokenLimit, PromptInjection, Gibberish


app = Flask(__name__)


vault = Vault()
anonymize_scanner = Anonymize(vault)
tokenlimit_scanner = TokenLimit(limit=256)
gibberish_scanner = Gibberish(match_type=MatchType.FULL)
toxicity_scanner = Toxicity(threshold=0.5, match_type=MatchType.SENTENCE)
injection_scanner = PromptInjection(threshold=0.5, match_type=MatchType.SENTENCE)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Use LLM Guard to evaluate input payloads
def evaluate(payload, scanners):
    output = None
    results_valid = None
    results_score = None

    try:
        output, results_valid, results_score = scan_prompt(scanners, payload)

        if any(not result for result in results_valid.values()):
            print(f"Prompt {payload} is not valid, scores: {results_score}")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        return jsonify({
            "output": {
                "prompt": output, 
                "results_valid": results_valid, 
                "results_score": results_score
            }
        })


@app.route('/evaluate', methods=['POST'])
def handle_evaluation_request():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid input"}), 400

    payload = data.get('input')

    if not payload:
        return jsonify({"error": "No input provided"}), 400

    scanners = [
        anonymize_scanner, 
        toxicity_scanner, 
        tokenlimit_scanner, 
        injection_scanner,
        gibberish_scanner
    ]
    return evaluate(payload, scanners=scanners)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
