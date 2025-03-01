def calculate_accuracy(predictions, ground_truths):
    """
    Calculate the accuracy of predictions against ground truths.
    """
    correct = 0
    for pred, truth in zip(predictions, ground_truths):
        # Basic string comparison - can be enhanced with more sophisticated matching
        if pred.strip().lower() == truth.strip().lower():
            correct += 1
    
    return correct / len(predictions) if predictions else 0

def calculate_metrics(results):
    """
    Calculate various metrics for evaluation.
    """
    metrics = {
        "total_problems": len(results),
        "total_correct": 0,
        "accuracy": 0,
        "avg_iterations": 0,
        "avg_subquestions": 0
    }
    
    if not results:
        return metrics
    
    total_iterations = 0
    total_subquestions = 0
    
    for result in results:
        # Count as correct if the prediction matches ground truth
        if result.get("solution", "").strip().lower() == result.get("ground_truth", "").strip().lower():
            metrics["total_correct"] += 1
            
        total_iterations += result.get("iterations_needed", 0)
        total_subquestions += len(result.get("subquestions", []))
    
    metrics["accuracy"] = metrics["total_correct"] / metrics["total_problems"]
    metrics["avg_iterations"] = total_iterations / metrics["total_problems"]
    metrics["avg_subquestions"] = total_subquestions / metrics["total_problems"]
    
    return metrics