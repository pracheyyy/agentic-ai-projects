from typing import Dict, List


# =========================================================
# Priority calculation
# =========================================================

PRIORITY_SCORE = {
    "high": 3,
    "medium": 2,
    "low": 1
}


def determine_priority(
    importance: str,
    status: str
) -> str:

    # Missing high-importance requirements
    # should receive the highest priority.

    if status == "missing":

        if importance == "high":
            return "high"

        return "medium"

    if status == "weak":

        if importance == "high":
            return "high"

        return "medium"

    if status == "partial":

        if importance == "high":
            return "medium"

        return "low"

    return "low"


# =========================================================
# Category-specific recommendation
# =========================================================

def create_category_recommendation(
    requirement: str,
    category: str,
    status: str
) -> str:

    # -----------------------------------------------------
    # Technical skills
    # -----------------------------------------------------

    if category == "technical_skill":

        if status == "missing":
            return (
                f"{requirement} is required by the job description "
                f"but was not found in your resume. Only add it if "
                f"you genuinely have this skill. Otherwise, consider "
                f"learning it before claiming it."
            )

        if status == "weak":
            return (
                f"{requirement} appears weakly represented. If you "
                f"have used it, make the technology more explicit in "
                f"your Skills, Projects, or Experience section."
            )

        if status == "partial":
            return (
                f"Your resume contains related evidence for "
                f"{requirement}, but the exact skill is not strongly "
                f"demonstrated. Clarify your actual usage if truthful."
            )

        return (
            f"{requirement} is clearly represented in your resume. "
            f"Keep it visible and connect it to relevant experience "
            f"where appropriate."
        )

    # -----------------------------------------------------
    # Responsibilities
    # -----------------------------------------------------

    if category == "responsibility":

        if status == "missing":
            return (
                f"The responsibility '{requirement}' is not supported "
                f"by evidence in your resume. If you have performed "
                f"this work, add a specific project or experience "
                f"bullet describing what you actually did."
            )

        if status == "weak":
            return (
                f"Your resume contains limited evidence for the "
                f"responsibility '{requirement}'. Strengthen the "
                f"relevant project or experience bullet with a "
                f"specific action and technology."
            )

        if status == "partial":
            return (
                f"Your resume partially demonstrates '{requirement}'. "
                f"Make the relevant contribution more explicit and "
                f"describe the actual work you performed."
            )

        return (
            f"Your resume provides strong evidence for "
            f"'{requirement}'. Preserve this evidence in the most "
            f"relevant experience or project section."
        )

    # -----------------------------------------------------
    # Experience
    # -----------------------------------------------------

    if category == "experience":

        if status == "missing":
            return (
                f"The job asks for '{requirement}', but corresponding "
                f"experience was not found. Do not fabricate experience. "
                f"If you have equivalent experience, describe it "
                f"clearly."
            )

        if status in ["weak", "partial"]:
            return (
                f"Your resume provides limited evidence for "
                f"'{requirement}'. Make the duration, role, or relevant "
                f"work more explicit if accurate."
            )

        return (
            f"Your resume provides evidence supporting "
            f"'{requirement}'. Keep the relevant experience clearly "
            f"described."
        )

    # -----------------------------------------------------
    # Education
    # -----------------------------------------------------

    if category == "education":

        if status == "missing":
            return (
                f"The job description mentions '{requirement}', but "
                f"matching education information was not detected. "
                f"If you meet this qualification, make your degree "
                f"and specialization explicit."
            )

        if status in ["weak", "partial"]:
            return (
                f"Your education partially matches '{requirement}'. "
                f"Make your degree, specialization, or relevant "
                f"qualification clearer."
            )

        return (
            f"Your education clearly supports '{requirement}'. "
            f"Keep the degree and specialization easy to identify."
        )

    # -----------------------------------------------------
    # Domain keywords
    # -----------------------------------------------------

    if category == "domain_keyword":

        if status == "missing":
            return (
                f"The domain term '{requirement}' appears important "
                f"to this role but was not found in your resume. "
                f"If your experience genuinely relates to this area, "
                f"use accurate terminology when describing it."
            )

        if status in ["weak", "partial"]:
            return (
                f"The concept '{requirement}' is only partially "
                f"represented. Consider making the relevant domain "
                f"experience more explicit."
            )

        return (
            f"Your resume already contains relevant evidence for "
            f"'{requirement}'."
        )

    # -----------------------------------------------------
    # Soft skills
    # -----------------------------------------------------

    if category == "soft_skill":

        if status == "missing":
            return (
                f"Evidence for '{requirement}' was not found. Avoid "
                f"simply adding the phrase as a claim; demonstrate "
                f"the skill through a project, leadership, teamwork, "
                f"or experience example when truthful."
            )

        if status in ["weak", "partial"]:
            return (
                f"Your resume gives limited evidence of "
                f"'{requirement}'. Demonstrate it through a concrete "
                f"example rather than relying only on a Skills list."
            )

        return (
            f"Your resume provides evidence related to "
            f"'{requirement}'."
        )

    # -----------------------------------------------------
    # Fallback
    # -----------------------------------------------------

    if status == "missing":
        return (
            f"Evidence for '{requirement}' was not found in your "
            f"resume. Add it only if you genuinely have the "
            f"relevant experience."
        )

    if status in ["weak", "partial"]:
        return (
            f"Strengthen the evidence supporting '{requirement}' "
            f"using a specific and truthful example."
        )

    return (
        f"Your resume already provides evidence for "
        f"'{requirement}'."
    )


# =========================================================
# Create one recommendation
# =========================================================

def create_recommendation(
    requirement: str,
    status: str,
    evidence: List[Dict],
    category: str = "keyword",
    importance: str = "medium"
) -> Dict:

    priority = determine_priority(
        importance,
        status
    )

    recommendation = create_category_recommendation(
        requirement=requirement,
        category=category,
        status=status
    )

    return {
        "requirement": requirement,
        "category": category,
        "importance": importance,
        "status": status,
        "priority": priority,
        "recommendation": recommendation,
        "evidence": evidence
    }


# =========================================================
# Generate all recommendations
# =========================================================

def generate_improvements(
    analysis_result: Dict
) -> List[Dict]:

    recommendations = []

    requirements = analysis_result.get(
        "requirements",
        []
    )

    for item in requirements:

        recommendation = create_recommendation(
            requirement=item.get(
                "requirement",
                ""
            ),
            status=item.get(
                "status",
                "missing"
            ),
            category=item.get(
                "category",
                "keyword"
            ),
            importance=item.get(
                "importance",
                "medium"
            ),
            evidence=item.get(
                "evidence",
                []
            )
        )

        recommendations.append(
            recommendation
        )

    return recommendations


# =========================================================
# Sort recommendations
# =========================================================

def prioritize_recommendations(
    recommendations: List[Dict]
) -> List[Dict]:

    return sorted(
        recommendations,
        key=lambda item: (
            -PRIORITY_SCORE.get(
                item.get("priority"),
                0
            ),
            -PRIORITY_SCORE.get(
                item.get("importance"),
                0
            )
        )
    )