from typing import Dict, List


WEIGHTS = {
    "technical_skill": 0.30,
    "responsibility": 0.25,
    "experience": 0.15,
    "education": 0.10,
    "domain_keyword": 0.10,
    "soft_skill": 0.05,
    "structure": 0.05
}


EVIDENCE_SCORES = {
    "matched": 1.0,
    "partial": 0.65,
    "weak": 0.35,
    "missing": 0.0
}


def calculate_category_score(
    requirements: List[Dict],
    category: str
) -> float:

    category_requirements = [
        item
        for item in requirements
        if item.get("category") == category
    ]

    if not category_requirements:
        return 100.0

    total = sum(
        EVIDENCE_SCORES.get(
            item.get(
                "status",
                "missing"
            ),
            0.0
        )
        for item in category_requirements
    )

    return round(
        (
            total
            / len(category_requirements)
        ) * 100,
        2
    )


def calculate_structure_score(
    resume_data: Dict
) -> float:

    sections = resume_data.get(
        "sections",
        {}
    )

    important_sections = [
        "education",
        "skills",
        "experience",
        "projects"
    ]

    present_sections = sum(
        1
        for section in important_sections
        if sections.get(section)
    )

    return round(
        (
            present_sections
            / len(important_sections)
        ) * 100,
        2
    )


def calculate_ats_score(
    resume_data: Dict,
    jd_data: Dict,
    matching_result: Dict
) -> Dict:

    requirements = matching_result.get(
        "requirements",
        []
    )

    technical_score = calculate_category_score(
        requirements,
        "technical_skill"
    )

    responsibility_score = calculate_category_score(
        requirements,
        "responsibility"
    )

    experience_score = calculate_category_score(
        requirements,
        "experience"
    )

    education_score = calculate_category_score(
        requirements,
        "education"
    )

    domain_score = calculate_category_score(
        requirements,
        "domain_keyword"
    )

    soft_skill_score = calculate_category_score(
        requirements,
        "soft_skill"
    )

    structure_score = calculate_structure_score(
        resume_data
    )

    final_score = round(
        technical_score
        * WEIGHTS["technical_skill"]

        + responsibility_score
        * WEIGHTS["responsibility"]

        + experience_score
        * WEIGHTS["experience"]

        + education_score
        * WEIGHTS["education"]

        + domain_score
        * WEIGHTS["domain_keyword"]

        + soft_skill_score
        * WEIGHTS["soft_skill"]

        + structure_score
        * WEIGHTS["structure"],
        2
    )

    statuses = [
        item.get(
            "status",
            "missing"
        )
        for item in requirements
    ]

    return {
        "ats_score": final_score,

        "components": {
            "technical_skills":
                technical_score,
            "responsibilities":
                responsibility_score,
            "experience":
                experience_score,
            "education":
                education_score,
            "domain_keywords":
                domain_score,
            "soft_skills":
                soft_skill_score,
            "resume_structure":
                structure_score
        },

        "weights": {
            "technical_skills":
                WEIGHTS["technical_skill"],
            "responsibilities":
                WEIGHTS["responsibility"],
            "experience":
                WEIGHTS["experience"],
            "education":
                WEIGHTS["education"],
            "domain_keywords":
                WEIGHTS["domain_keyword"],
            "soft_skills":
                WEIGHTS["soft_skill"],
            "resume_structure":
                WEIGHTS["structure"]
        },

        "summary": {
            "total_requirements":
                len(requirements),
            "matched":
                statuses.count("matched"),
            "partial":
                statuses.count("partial"),
            "weak":
                statuses.count("weak"),
            "missing":
                statuses.count("missing")
        }
    }
