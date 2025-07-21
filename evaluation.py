def evaluate_response(response):
    # Dummy evaluator: score based on length & keywords
    accuracy = min(5, len(response.split()) / 30)
    depth = 4 if "however" in response or "implications" in response else 3
    clarity = 5 if response.count('.') > 3 else 4
    return round(accuracy, 2), depth, clarity
