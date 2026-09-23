from typing import Dict

from app.services.matching_engine import (
    match_requirements
)

from app.services.rag_retriever import (
    retrieve_requirement_evidence
)


def analyze_requirements(
    resume_data: Dict,
    jd_data: Dict
) -> Dict:

    matching_result = match_requirements(
        resume_data,
        jd_data
    )

    resume_text = resume_data.get(
        "raw_text",
        ""
    )

    analyzed_requirements = []

    for item in matching_result["requirements"]:

        requirement = item[
            "requirement"
        ]

        rag_result = (
            retrieve_requirement_evidence(
                resume_text=resume_text,
                requirement=requirement,
                top_k=3
            )
        )

        analyzed_requirements.append({
            "requirement": requirement,
            "category": item["category"],
            "importance": item["importance"],
            "status": item["status"],
            "evidence_strength":
                item["evidence_strength"],
            "rag_relevance":
                rag_result["relevance"],
            "evidence":
                rag_result["evidence"]
        })

    matched = [
        item
        for item in analyzed_requirements
        if item["status"] == "matched"
    ]

    partial = [
        item
        for item in analyzed_requirements
        if item["status"] == "partial"
    ]

    weak = [
        item
        for item in analyzed_requirements
        if item["status"] == "weak"
    ]

    missing = [
        item
        for item in analyzed_requirements
        if item["status"] == "missing"
    ]

    return {
        "matching": {
            **matching_result,
            "matched": matched,
            "partial": partial,
            "weak": weak,
            "missing": missing
        },
        "requirements":
            analyzed_requirements,
        "summary": {
            "total":
                len(analyzed_requirements),
            "matched":
                len(matched),
            "partial":
                len(partial),
            "weak":
                len(weak),
            "missing":
                len(missing)
        }
    }
