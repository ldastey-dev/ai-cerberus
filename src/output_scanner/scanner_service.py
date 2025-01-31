from flask import request, jsonify
from llm_guard import scan_output


# Use LLM Guard to evaluate output against their input payloads
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