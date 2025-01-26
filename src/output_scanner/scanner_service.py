from flask import Flask, request, jsonify
from llm_guard import scan_output
from llm_guard.output_scanners import Relevance


app = Flask(__name__)


relevance_scanner = Relevance(threshold=0.5)


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"}), 200


# Use LLM Guard to evaluate output against input payloads
def evaluate(input_payload, generated_output, scanners):
    results_valid = None
    results_score = None
    scanner_output = None

    try:
        scanner_output, results_valid, results_score = scan_output(
            scanners, 
            input_payload, 
            generated_output
        )

        relevance_score = float(results_score['Relevance'])

        if any(not result for result in results_valid.values()):
            print(f"Output {generated_output} is not valid, scores: {relevance_score}")

        print(f"Output: {scanner_output}\n")
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        return jsonify({
            "output": {
                "scanner_output": scanner_output, 
                "results_valid": results_valid, 
                "results_score": relevance_score
            }
        })


@app.route('/scanoutput', methods=['POST'])
def handle_evaluation_request():
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
    return evaluate(input_payload, generated_output, scanners=scanners)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
