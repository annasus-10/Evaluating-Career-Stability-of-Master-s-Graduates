import pandas as pd
import numpy as np
import data

def get_recommendations(program_name: str, program_type: str = None, top_n: int = 10):
    mask = data.program_recs["program_name_lower"] == program_name.lower().strip()

    if program_type:
        mask = mask & (
            data.program_recs["program_type"].str.lower() ==
            program_type.lower().strip()
        )

    results = data.program_recs[mask].copy()

    if results.empty:
        return None

    meta    = results.iloc[0]
    results = results.head(top_n)

    total_unique = int(results["total_unique_careers"].iloc[0]) \
                   if "total_unique_careers" in results.columns else len(results)

    recommendations = []
    for _, row in results.iterrows():
        soc6   = str(row.get("SOC6", "")).strip()
        skills = data.top_skills_map.get(soc6)
        tech   = data.tech_map.get(soc6, {})

        def safe(val):
            return None if (
                val is None or
                (isinstance(val, float) and np.isnan(val))
            ) else val

        recommendations.append({
            "career_match":           str(row["career_match"]),
            "similarity":             round(float(row["similarity"]), 4),
            "GCSI":                   round(float(row["GCSI"]), 2),
            "GCSI_imputed":           bool(row.get("GCSI_imputed", False)),
            "hybrid_score":           round(float(row["hybrid_score"]), 4),
            "A_MEDIAN":               safe(row.get("A_MEDIAN")),
            "automation_probability": safe(row.get("automation_probability")),
            "top_skills":             skills,
            "technology_items":       safe(tech.get("technology_items")),
            "hot_tech_items":         safe(tech.get("hot_tech_items")),
        })

    return {
        "program_name":     str(meta["program_name"]),
        "program_type":     str(meta["program_type"]),
        "broad_field":      str(meta.get("broad_field", "Unknown")),
        "degree_norm":      str(meta.get("degree_final", "")),
        "total_candidates": total_unique,
        "recommendations":  recommendations,
    }