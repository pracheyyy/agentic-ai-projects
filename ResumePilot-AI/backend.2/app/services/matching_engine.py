from typing import List, Dict


RELATED_SKILLS = {
    "node.js": ["javascript"],
    "javascript": ["node.js"],

    "spring boot": ["java"],
    "java": ["spring boot"],

    "rest api": ["rest"],
    "rest": ["rest api"],

    "machine learning": [
        "scikit-learn",
        "tensorflow",
        "pytorch"
    ],

    "deep learning": [
        "tensorflow",
        "pytorch"
    ],

    "data structures": [
        "algorithms"
    ],

    "algorithms": [
        "data structures"
    ]
}


# ---------------------------------------------------------
# Normalization
# ---------------------------------------------------------

def normalize_text(text: str) -> str:
    return " ".join(
        text.lower()
        .strip()
        .split()
    )


# ---------------------------------------------------------
# Skill normalization
# ---------------------------------------------------------

def normalize_skills(
    skills: List[str]
) -> List[str]:

    normalized = []

    for skill in skills:

        skill = normalize_text(skill)

        if skill and skill not in normalized:
            normalized.append(skill)

    return normalized


# ---------------------------------------------------------
# Exact skill matching
# ---------------------------------------------------------

def find_exact_matches(
    resume_skills: List[str],
    jd_skills: List[str]
) -> List[str]:

    return [
        skill
        for skill in jd_skills
        if skill in resume_skills
    ]


# ---------------------------------------------------------
# Partial skill matching
# ---------------------------------------------------------

def find_partial_matches(
    resume_skills: List[str],
    jd_skills: List[str]
) -> List[str]:

    partial_matches = []

    for jd_skill in jd_skills:

        if jd_skill in resume_skills:
            continue

        related_skills = RELATED_SKILLS.get(
            jd_skill,
            []
        )

        for related in related_skills:

            if related in resume_skills:

                partial_matches.append(
                    jd_skill
                )

                break

    return partial_matches


# ---------------------------------------------------------
# Missing skills
# ---------------------------------------------------------

def find_missing_skills(
    resume_skills: List[str],
    jd_skills: List[str],
    matched: List[str],
    partial: List[str]
) -> List[str]:

    covered = set(
        matched + partial
    )

    return [
        skill
        for skill in jd_skills
        if skill not in covered
    ]


# ---------------------------------------------------------
# Skill percentage
# ---------------------------------------------------------

def calculate_match_percentage(
    jd_skills: List[str],
    matched: List[str],
    partial: List[str]
) -> float:

    total_skills = len(jd_skills)

    if total_skills == 0:
        return 0.0

    score = (
        len(matched)
        + (0.5 * len(partial))
    )

    return round(
        (score / total_skills) * 100,
        2
    )


# =========================================================
# NEW REQUIREMENT MATCHING
# =========================================================


# ---------------------------------------------------------
# Check whether resume contains requirement text
# ---------------------------------------------------------

def requirement_keyword_match(
    requirement: str,
    resume_text: str
) -> bool:

    requirement_words = set(
        normalize_text(requirement).split()
    )

    resume_words = set(
        normalize_text(resume_text).split()
    )

    if not requirement_words:
        return False

    common_words = (
        requirement_words
        & resume_words
    )

    # Percentage of requirement words
    # found in resume
    coverage = (
        len(common_words)
        / len(requirement_words)
    )

    return coverage >= 0.60


# ---------------------------------------------------------
# Calculate lexical evidence strength
# ---------------------------------------------------------

def calculate_evidence_strength(
    requirement: str,
    resume_text: str,
    category: str
) -> int:

    requirement_normalized = normalize_text(
        requirement
    )

    resume_normalized = normalize_text(
        resume_text
    )

    # -----------------------------------------
    # Strong: exact phrase appears
    # -----------------------------------------

    if requirement_normalized in resume_normalized:

        return 3

    # -----------------------------------------
    # Technical skills
    # -----------------------------------------

    if category == "technical_skill":

        if requirement_keyword_match(
            requirement,
            resume_text
        ):
            return 3

        return 0

    # -----------------------------------------
    # Other requirements
    # -----------------------------------------

    requirement_words = set(
        requirement_normalized.split()
    )

    resume_words = set(
        resume_normalized.split()
    )

    if not requirement_words:
        return 0

    common_words = (
        requirement_words
        & resume_words
    )

    coverage = (
        len(common_words)
        / len(requirement_words)
    )

    if coverage >= 0.70:
        return 3

    if coverage >= 0.40:
        return 2

    if coverage > 0:
        return 1

    return 0


# ---------------------------------------------------------
# Convert evidence strength to status
# ---------------------------------------------------------

def evidence_strength_to_status(
    strength: int
) -> str:

    if strength >= 3:
        return "matched"

    if strength == 2:
        return "partial"

    if strength == 1:
        return "weak"

    return "missing"


# ---------------------------------------------------------
# Match one requirement
# ---------------------------------------------------------

def match_requirement(
    requirement: Dict,
    resume_text: str
) -> Dict:

    text = requirement.get(
        "text",
        ""
    )

    category = requirement.get(
        "category",
        "keyword"
    )

    importance = requirement.get(
        "importance",
        "medium"
    )

    evidence_strength = (
        calculate_evidence_strength(
            text,
            resume_text,
            category
        )
    )

    status = (
        evidence_strength_to_status(
            evidence_strength
        )
    )

    return {
        "requirement": text,
        "category": category,
        "importance": importance,
        "status": status,
        "evidence_strength": evidence_strength
    }


# ---------------------------------------------------------
# Match all JD requirements
# ---------------------------------------------------------

def match_requirements(
    resume_data: Dict,
    jd_data: Dict
) -> Dict:

    resume_text = resume_data.get(
        "raw_text",
        ""
    )

    requirements = jd_data.get(
        "requirements",
        []
    )

    results = []

    for requirement in requirements:

        result = match_requirement(
            requirement,
            resume_text
        )

        results.append(result)

    matched = [
        item
        for item in results
        if item["status"] == "matched"
    ]

    partial = [
        item
        for item in results
        if item["status"] == "partial"
    ]

    weak = [
        item
        for item in results
        if item["status"] == "weak"
    ]

    missing = [
        item
        for item in results
        if item["status"] == "missing"
    ]

    return {
        "requirements": results,
        "matched": matched,
        "partial": partial,
        "weak": weak,
        "missing": missing,
        "total_requirements": len(results),
        "matched_count": len(matched),
        "partial_count": len(partial),
        "weak_count": len(weak),
        "missing_count": len(missing)
    }


# =========================================================
# LEGACY SKILL MATCHING
# Keep this for compatibility with current tests/code.
# =========================================================

def match_resume_to_jd(
    resume_data: Dict,
    jd_data: Dict
) -> Dict:

    resume_skills = normalize_skills(
        resume_data.get(
            "skills",
            []
        )
    )

    jd_skills = normalize_skills(
        jd_data.get(
            "required_skills",
            []
        )
    )

    matched = find_exact_matches(
        resume_skills,
        jd_skills
    )

    partial = find_partial_matches(
        resume_skills,
        jd_skills
    )

    missing = find_missing_skills(
        resume_skills,
        jd_skills,
        matched,
        partial
    )

    match_percentage = (
        calculate_match_percentage(
            jd_skills,
            matched,
            partial
        )
    )

    return {
        "matched": matched,
        "partial": partial,
        "missing": missing,
        "match_percentage": match_percentage,
        "total_jd_skills": len(jd_skills),
        "total_resume_skills": len(resume_skills)
    }