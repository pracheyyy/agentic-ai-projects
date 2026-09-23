import re


# ---------------------------------------------------------
# Technical skills
# ---------------------------------------------------------

SKILLS = [
    "python",
    "java",
    "javascript",
    "typescript",
    "c++",
    "c",
    "sql",
    "html",
    "css",
    "react",
    "node.js",
    "node",
    "express",
    "fastapi",
    "flask",
    "spring boot",
    "spring",
    "mongodb",
    "mysql",
    "postgresql",
    "docker",
    "kubernetes",
    "git",
    "github",
    "aws",
    "azure",
    "gcp",
    "tensorflow",
    "pytorch",
    "scikit-learn",
    "pandas",
    "numpy",
    "opencv",
    "langchain",
    "rag",
    "llm",
    "machine learning",
    "deep learning",
    "rest api",
    "rest",
    "microservices",
    "linux",
    "data structures",
    "algorithms",
    "oops",
    "object oriented programming",
]


ALIASES = {
    "node": "node.js",
    "spring": "spring boot",
    "rest": "rest api",
    "object oriented programming": "oops",
}


# ---------------------------------------------------------
# Soft skills
# ---------------------------------------------------------

SOFT_SKILLS = [
    "communication",
    "problem solving",
    "problem-solving",
    "teamwork",
    "collaboration",
    "leadership",
    "analytical thinking",
    "critical thinking",
    "time management",
    "adaptability",
    "creativity",
    "attention to detail",
    "interpersonal skills",
    "presentation skills",
]


# ---------------------------------------------------------
# JD section headings
# ---------------------------------------------------------

SECTION_HEADINGS = {
    "responsibilities": "responsibilities",
    "responsibility": "responsibilities",
    "what you'll do": "responsibilities",
    "what you will do": "responsibilities",
    "key responsibilities": "responsibilities",
    "job responsibilities": "responsibilities",
    "role and responsibilities": "responsibilities",

    "requirements": "requirements",
    "requirement": "requirements",
    "qualifications": "qualifications",
    "qualification": "qualifications",
    "required qualifications": "qualifications",
    "preferred qualifications": "preferred_qualifications",

    "experience": "experience",
    "experience required": "experience",
    "work experience": "experience",

    "skills": "skills",
    "technical skills": "skills",

    "about the role": "about_role",
    "about the job": "about_role",
    "job description": "about_role",
}


# ---------------------------------------------------------
# Normalization
# ---------------------------------------------------------

def normalize(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9+#./\-\s]",
        " ",
        text
    )

    return re.sub(
        r"\s+",
        " ",
        text
    ).strip()


# ---------------------------------------------------------
# Skill extraction
# ---------------------------------------------------------

def find_skills(text: str) -> list:
    normalized_text = normalize(text)

    found_skills = []

    for skill in SKILLS:

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):

            canonical_skill = ALIASES.get(
                skill,
                skill
            )

            if canonical_skill not in found_skills:
                found_skills.append(
                    canonical_skill
                )

    return found_skills


# ---------------------------------------------------------
# Soft skill extraction
# ---------------------------------------------------------

def find_soft_skills(text: str) -> list:
    normalized_text = normalize(text)

    found = []

    for skill in SOFT_SKILLS:

        canonical_skill = skill.replace(
            "problem-solving",
            "problem solving"
        )

        pattern = (
            r"(?<!\w)"
            + re.escape(skill)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized_text):

            if canonical_skill not in found:
                found.append(canonical_skill)

    return found


# ---------------------------------------------------------
# Section detection
# ---------------------------------------------------------

def extract_sections(text: str) -> dict:

    lines = text.splitlines()

    sections = {}

    current_section = "general"

    sections[current_section] = []

    for line in lines:

        clean_line = line.strip()

        if not clean_line:
            continue

        normalized_line = (
            clean_line
            .lower()
            .replace(":", "")
            .strip()
        )

        if normalized_line in SECTION_HEADINGS:

            current_section = SECTION_HEADINGS[
                normalized_line
            ]

            if current_section not in sections:
                sections[current_section] = []

            continue

        sections[current_section].append(
            clean_line
        )

    return sections


# ---------------------------------------------------------
# Experience extraction
# ---------------------------------------------------------

def find_experience_requirements(text: str) -> list:

    normalized_text = normalize(text)

    requirements = []

    patterns = [
        r"\b\d+\+?\s+years?\s+of\s+experience\b",
        r"\b\d+\+?\s+years?\s+experience\b",
        r"\bminimum\s+\d+\s+years?\b",
        r"\bat least\s+\d+\s+years?\b",
        r"\binternship experience\b",
        r"\bprofessional experience\b",
        r"\bsoftware development experience\b",
    ]

    for pattern in patterns:

        matches = re.findall(
            pattern,
            normalized_text
        )

        for match in matches:

            if match not in requirements:
                requirements.append(match)

    return requirements


# ---------------------------------------------------------
# Education extraction
# ---------------------------------------------------------

def find_education_requirements(text: str) -> list:

    normalized_text = normalize(text)

    education_patterns = [
        "bachelor's degree",
        "bachelor degree",
        "b.tech",
        "btech",
        "master's degree",
        "master degree",
        "m.tech",
        "mtech",
        "computer science",
        "information technology",
        "computer engineering",
        "engineering degree",
    ]

    found = []

    for requirement in education_patterns:

        if requirement in normalized_text:

            if requirement not in found:
                found.append(requirement)

    return found


# ---------------------------------------------------------
# Importance detection
# ---------------------------------------------------------

def determine_importance(text: str) -> str:

    normalized_text = normalize(text)

    high_indicators = [
        "required",
        "must",
        "mandatory",
        "essential",
        "need",
        "needed",
        "strong knowledge",
        "proficiency",
    ]

    medium_indicators = [
        "preferred",
        "good to have",
        "nice to have",
        "bonus",
        "plus",
        "familiarity",
    ]

    for keyword in high_indicators:

        if keyword in normalized_text:
            return "high"

    for keyword in medium_indicators:

        if keyword in normalized_text:
            return "medium"

    return "medium"


# ---------------------------------------------------------
# Requirement creation
# ---------------------------------------------------------

def create_requirement(
    text: str,
    category: str,
    importance: str = None
) -> dict:

    clean_text = text.strip()

    if not clean_text:
        return None

    if importance is None:
        importance = determine_importance(
            clean_text
        )

    return {
        "text": clean_text,
        "category": category,
        "importance": importance
    }


# ---------------------------------------------------------
# Extract bullet requirements
# ---------------------------------------------------------

def extract_bullet_requirements(
    sections: dict
) -> list:

    requirements = []

    category_mapping = {
        "responsibilities": "responsibility",
        "requirements": "qualification",
        "qualifications": "education",
        "preferred_qualifications": "qualification",
        "experience": "experience",
    }

    for section, lines in sections.items():

        category = category_mapping.get(
            section
        )

        if not category:
            continue

        for line in lines:

            clean_line = re.sub(
                r"^[\-\•\*\▪\●\d\.\)\s]+",
                "",
                line
            ).strip()

            if len(clean_line) < 8:
                continue

            requirement = create_requirement(
                clean_line,
                category
            )

            if requirement:
                requirements.append(
                    requirement
                )

    return requirements


# ---------------------------------------------------------
# Skill requirements
# ---------------------------------------------------------

def create_skill_requirements(
    skills: list
) -> list:

    requirements = []

    for skill in skills:

        requirements.append({
            "text": skill,
            "category": "technical_skill",
            "importance": "high"
        })

    return requirements


# ---------------------------------------------------------
# Soft-skill requirements
# ---------------------------------------------------------

def create_soft_skill_requirements(
    soft_skills: list
) -> list:

    requirements = []

    for skill in soft_skills:

        requirements.append({
            "text": skill,
            "category": "soft_skill",
            "importance": "medium"
        })

    return requirements


# ---------------------------------------------------------
# Important domain keywords
# ---------------------------------------------------------

def find_keywords(text: str) -> list:

    normalized_text = normalize(text)

    keywords = []

    keyword_patterns = [
        "software development",
        "web development",
        "backend development",
        "frontend development",
        "full stack",
        "api development",
        "rest api",
        "cloud",
        "database",
        "distributed systems",
        "machine learning",
        "artificial intelligence",
        "data science",
        "generative ai",
        "deployment",
        "testing",
        "debugging",
        "agile",
        "version control",
    ]

    for keyword in keyword_patterns:

        if keyword in normalized_text:

            if keyword not in keywords:
                keywords.append(keyword)

    return keywords


# ---------------------------------------------------------
# Signals
# ---------------------------------------------------------

def find_signals(text: str) -> dict:

    normalized_text = normalize(text)

    experience_signals = []
    education_signals = []

    experience_keywords = [
        "internship",
        "intern",
        "experience",
        "years of experience",
        "work experience",
        "professional experience",
    ]

    education_keywords = [
        "bachelor",
        "b.tech",
        "btech",
        "degree",
        "graduate",
        "computer science",
        "information technology",
    ]

    for keyword in experience_keywords:

        if keyword in normalized_text:
            experience_signals.append(keyword)

    for keyword in education_keywords:

        if keyword in normalized_text:
            education_signals.append(keyword)

    return {
        "experience_signals": experience_signals,
        "education_signals": education_signals
    }


# ---------------------------------------------------------
# Remove duplicate requirements
# ---------------------------------------------------------

def deduplicate_requirements(
    requirements: list
) -> list:

    unique = []

    seen = set()

    for requirement in requirements:

        key = (
            requirement["text"].lower(),
            requirement["category"]
        )

        if key not in seen:

            seen.add(key)

            unique.append(
                requirement
            )

    return unique


# ---------------------------------------------------------
# Main JD parser
# ---------------------------------------------------------

def parse_job_description(
    text: str
) -> dict:

    if not text or not text.strip():

        raise ValueError(
            "Job Description cannot be empty."
        )

    skills = find_skills(text)

    soft_skills = find_soft_skills(text)

    signals = find_signals(text)

    sections = extract_sections(text)

    experience_requirements = (
        find_experience_requirements(text)
    )

    education_requirements = (
        find_education_requirements(text)
    )

    keywords = find_keywords(text)

    requirements = []

    # Technical skills
    requirements.extend(
        create_skill_requirements(
            skills
        )
    )

    # Soft skills
    requirements.extend(
        create_soft_skill_requirements(
            soft_skills
        )
    )

    # Bullet-based requirements
    requirements.extend(
        extract_bullet_requirements(
            sections
        )
    )

    # Experience
    for experience in experience_requirements:

        requirements.append({
            "text": experience,
            "category": "experience",
            "importance": "high"
        })

    # Education
    for education in education_requirements:

        requirements.append({
            "text": education,
            "category": "education",
            "importance": "high"
        })

    # Domain keywords
    for keyword in keywords:

        requirements.append({
            "text": keyword,
            "category": "domain_keyword",
            "importance": "medium"
        })

    requirements = deduplicate_requirements(
        requirements
    )

    return {
        "raw_text": text,

        "required_skills": skills,

        "soft_skills": soft_skills,

        "experience_signals":
            signals["experience_signals"],

        "education_signals":
            signals["education_signals"],

        "experience_requirements":
            experience_requirements,

        "education_requirements":
            education_requirements,

        "keywords": keywords,

        "sections": sections,

        "requirements": requirements
    }