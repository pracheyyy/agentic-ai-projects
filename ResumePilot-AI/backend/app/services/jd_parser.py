import re


SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "c", "sql",
    "html", "css", "react", "node.js", "node", "express", "fastapi", "flask",
    "spring boot", "spring", "mongodb", "mysql", "postgresql", "docker",
    "kubernetes", "git", "github", "aws", "azure", "gcp", "tensorflow",
    "pytorch", "scikit-learn", "pandas", "numpy", "opencv", "langchain",
    "rag", "llm", "machine learning", "deep learning", "rest api", "rest",
    "microservices", "linux", "data structures", "algorithms", "oops",
    "object oriented programming", "communication", "problem solving"
]

ALIASES = {
    "node": "node.js",
    "spring": "spring boot",
    "rest": "rest api",
    "object oriented programming": "oops"
}

SOFT_SKILLS = [
    "communication", "problem solving", "problem-solving",
    "teamwork", "collaboration", "leadership",
    "analytical thinking", "critical thinking",
    "time management", "adaptability", "creativity",
    "attention to detail", "interpersonal skills",
    "presentation skills"
]

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
    "job description": "about_role"
}


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9+#./\-\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def find_skills(text: str) -> list:
    normalized_text = normalize(text)
    found_skills = []

    for skill in SKILLS:
        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            canonical_skill = ALIASES.get(skill, skill)

            if canonical_skill not in found_skills:
                found_skills.append(canonical_skill)

    return found_skills


def find_soft_skills(text: str) -> list:
    normalized_text = normalize(text)
    found = []

    for skill in SOFT_SKILLS:
        canonical_skill = skill.replace(
            "problem-solving",
            "problem solving"
        )

        pattern = r"(?<!\w)" + re.escape(skill) + r"(?!\w)"

        if re.search(pattern, normalized_text):
            if canonical_skill not in found:
                found.append(canonical_skill)

    return found


def extract_sections(text: str) -> dict:
    lines = text.splitlines()

    sections = {
        "general": []
    }

    current_section = "general"

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

        sections[current_section].append(clean_line)

    return sections


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
        r"\bsoftware development experience\b"
    ]

    for pattern in patterns:
        for match in re.findall(pattern, normalized_text):
            if match not in requirements:
                requirements.append(match)

    return requirements


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
        "engineering degree"
    ]

    return [
        requirement
        for requirement in education_patterns
        if requirement in normalized_text
    ]


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
        "proficiency"
    ]

    medium_indicators = [
        "preferred",
        "good to have",
        "nice to have",
        "bonus",
        "plus",
        "familiarity"
    ]

    if any(
        keyword in normalized_text
        for keyword in high_indicators
    ):
        return "high"

    if any(
        keyword in normalized_text
        for keyword in medium_indicators
    ):
        return "medium"

    return "medium"


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


def extract_bullet_requirements(
    sections: dict
) -> list:
    requirements = []

    category_mapping = {
        "responsibilities": "responsibility",
        "requirements": "qualification",
        "qualifications": "education",
        "preferred_qualifications": "qualification",
        "experience": "experience"
    }

    for section, lines in sections.items():

        category = category_mapping.get(section)

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


def create_skill_requirements(
    skills: list
) -> list:
    return [
        {
            "text": skill,
            "category": "technical_skill",
            "importance": "high"
        }
        for skill in skills
    ]


def create_soft_skill_requirements(
    soft_skills: list
) -> list:
    return [
        {
            "text": skill,
            "category": "soft_skill",
            "importance": "medium"
        }
        for skill in soft_skills
    ]


def find_keywords(text: str) -> list:
    normalized_text = normalize(text)

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
        "version control"
    ]

    return [
        keyword
        for keyword in keyword_patterns
        if keyword in normalized_text
    ]


def find_signals(text: str) -> dict:
    normalized_text = normalize(text)

    experience_keywords = [
        "internship",
        "intern",
        "experience",
        "years of experience",
        "work experience",
        "professional experience"
    ]

    education_keywords = [
        "bachelor",
        "b.tech",
        "btech",
        "degree",
        "graduate",
        "computer science",
        "information technology"
    ]

    return {
        "experience_signals": [
            keyword
            for keyword in experience_keywords
            if keyword in normalized_text
        ],
        "education_signals": [
            keyword
            for keyword in education_keywords
            if keyword in normalized_text
        ]
    }


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
            unique.append(requirement)

    return unique


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

    requirements.extend(
        create_skill_requirements(skills)
    )

    requirements.extend(
        create_soft_skill_requirements(
            soft_skills
        )
    )

    requirements.extend(
        extract_bullet_requirements(
            sections
        )
    )

    for experience in experience_requirements:
        requirements.append({
            "text": experience,
            "category": "experience",
            "importance": "high"
        })

    for education in education_requirements:
        requirements.append({
            "text": education,
            "category": "education",
            "importance": "high"
        })

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
        "experience_signals": signals[
            "experience_signals"
        ],
        "education_signals": signals[
            "education_signals"
        ],
        "experience_requirements":
            experience_requirements,
        "education_requirements":
            education_requirements,
        "keywords": keywords,
        "sections": sections,
        "requirements": requirements
    }
