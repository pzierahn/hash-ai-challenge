def calculate_candidate_score(assessment: dict) -> int:
    """
    Calculate the overall score for the candidate based on required and nice-to-have skills.
    Required skills are weighted more heavily than nice-to-have skills.
    """

    score = 0

    for eval in assessment["required"]:
        match eval["rating"]:
            case "strong":
                score += 3 * 2
            case "moderate":
                score += 2 * 2
            case "weak":
                score += 1 * 2

    for eval in assessment["preferred"]:
        match eval["rating"]:
            case "strong":
                score += 3
            case "moderate":
                score += 2
            case "weak":
                score += 1
            case "none":
                score -= 3
            case _:
                score += 0

    return score


def has_required_criteria(candidate: dict) -> bool:
    """
    Check if the candidate meets all required criteria.
    Returns True if all required criteria are rated as 'strong' or 'moderate'.
    """

    for eval in candidate["required"]:
        if eval["rating"] not in ["strong", "moderate"]:
            return False

    return True
