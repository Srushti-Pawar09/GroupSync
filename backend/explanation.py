def generate_explanation(recommendations):

    if not recommendations:
        return {
            "summary": "No destinations satisfy the group's vibe and budget constraints.",
            "details": []
        }

    explanations = []

    for rec in recommendations:

        coverage_percent = int(rec["coverage_ratio"] * 100)

        explanation_text = (
            f"{rec['city']} was selected because it satisfies "
            f"{coverage_percent}% of the group's preferred vibes "
            f"({', '.join(rec['covered_vibes'])}). "
        )

        if rec["missing_vibes"]:
            explanation_text += (
                f"It does not fully cover: "
                f"{', '.join(rec['missing_vibes'])}. "
            )

        explanation_text += (
            f"\n\nRecommended trip duration: {rec['suggested_days']} days.\n"
            f"Estimated total cost per person: ₹{rec['total_cost_per_person']} "
            f"(Stay: ₹{rec['stay_cost_per_person']} + Travel: ₹{rec['travel_cost_per_person']}).\n"
            f"Remaining budget headroom: ₹{rec['budget_headroom']}.\n"
            f"Average rating: {rec['avg_rating']}.\n"
        )

        if rec["famous_foods"]:
            explanation_text += (
                f"\nFamous local food: {', '.join(rec['famous_foods'])}.\n"
            )

        explanation_text += (
            f"\nSample attractions: {', '.join(rec['sample_places'])}."
        )

        explanations.append({
            "city": rec["city"],
            "explanation": explanation_text
        })

    return {
        "summary": "Top destinations ranked by vibe match, budget feasibility, and quality.",
        "details": explanations
    }
