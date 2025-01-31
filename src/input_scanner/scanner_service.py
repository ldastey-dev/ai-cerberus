from flask import request, jsonify
from llm_guard import scan_prompt


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