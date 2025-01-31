from flask import Flask, request, jsonify
from llm_guard.vault import Vault
from llm_guard.input_scanners.prompt_injection import MatchType
from llm_guard.input_scanners import Anonymize, Toxicity, TokenLimit, PromptInjection, Gibberish
from llm_guard.output_scanners import Relevance
from input_scanner import scanner_service as input_scanner
from output_scanner import scanner_service as output_scanner


app = Flask(__name__)


# Pre-initialise input scanners
vault = Vault()
anonymize_scanner = Anonymize(vault)
tokenlimit_scanner = TokenLimit(limit=256)
gibberish_scanner = Gibberish(match_type=MatchType.FULL)
toxicity_scanner = Toxicity(threshold=0.5, match_type=MatchType.SENTENCE)
injection_scanner = PromptInjection(threshold=0.5, match_type=MatchType.SENTENCE)


# Pre-initialise output scanners
relevance_scanner = Relevance(threshold=0.5)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


@app.route('/input/evaluate', methods=['POST'])
def handle_input_evaluation_request():
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
    return input_scanner.evaluate(payload, scanners=scanners)


@app.route('/output/evaluate', methods=['POST'])
def handle_output_evaluation_request():
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid payload"}), 400

    input_payload = data.get('prompt_input')
    generated_output = data.get('generated_output')

    if not input_payload:
        return jsonify({"error": "No input payload provided"}), 400

    if not generated_output:
        return jsonify({"error": "No generated output provided"}), 400

    scanners = [relevance_scanner]
    return output_scanner.evaluate(input_payload, generated_output, scanners=scanners)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)