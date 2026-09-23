from typing import Dict

from app.services.matching_engine import match_requirements
from app.services.rag_retriever import retrieve_evidence


def analyze_requirements(
    resume_data: Dict,
    jd_data: Dict
) -> Dict:

    # -----------------------------------------------------
    # Step 1: Match all JD requirements
    # -----------------------------------------------------

    matching_result = match_requirements(
        resume_data,
        jd_data
    )

    resume_text = resume_data.get(
        "raw_text",
        ""
    )

    analyzed_requirements = []

    # -----------------------------------------------------
    # Step 2: Retrieve resume evidence for each
    # requirement
    # -----------------------------------------------------

    for item in matching_result["requirements"]:

        requirement = item["requirement"]

        evidence = retrieve_evidence(
            resume_text,
            requirement,
            top_k=3
        )

        # -------------------------------------------------
        # Only keep meaningful evidence
        # -------------------------------------------------

        meaningful_evidence = [
            evidence_item
            for evidence_item in evidence
            if evidence_item.get("score", 0) > 0
        ]

        # -------------------------------------------------
        # Add evidence to requirement
        # -------------------------------------------------

        analyzed_requirements.append({
            "requirement": requirement,
            "category": item["category"],
            "importance": item["importance"],
            "status": item["status"],
            "evidence_strength": item["evidence_strength"],
            "evidence": meaningful_evidence
        })

    # -----------------------------------------------------
    # Step 3: Recalculate groups using analyzed data
    # -----------------------------------------------------

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

        "requirements": analyzed_requirements,

        "summary": {
            "total": len(analyzed_requirements),
            "matched": len(matched),
            "partial": len(partial),
            "weak": len(weak),
            "missing": len(missing)
        }
    }