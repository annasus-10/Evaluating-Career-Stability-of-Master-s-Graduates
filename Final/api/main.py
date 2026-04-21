from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import numpy as np
import pandas as pd

import data
from recommend import get_recommendations
from models import (
    RecommendationResponse, FieldOverview,
    CareerDetail, DropdownField, DropdownProgram
)

app = FastAPI(
    title="CareerScope API",
    description="Career recommendation and stability API for masters graduates",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def safe(val):
    if val is None:
        return None
    if isinstance(val, float) and np.isnan(val):
        return None
    return val


# ── Health ────────────────────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {
        "status": "ok",
        "datasets": {
            "occupation_gcsi": len(data.occupation_gcsi),
            "program_recs":    len(data.program_recs),
            "field_dropdown":  len(data.field_dropdown),
            "skill_bridge":    len(data.skill_bridge),
            "tech_summary":    len(data.tech_summary),
        }
    }


# ── Dashboard ─────────────────────────────────────────────────────────────────

@app.get("/dashboard/overview", response_model=List[FieldOverview])
def dashboard_overview():
    results = []
    grouped = data.program_recs.groupby("broad_field")

    for field, group in grouped:
        top_careers = (
            group["career_match"]
            .value_counts()
            .head(3)
            .index
            .tolist()
        )
        results.append({
            "broad_field":         str(field),
            "program_count":       int(group["program_name"].nunique()),
            "avg_gcsi":            round(float(group["GCSI"].mean()), 2),
            "avg_salary":          safe(
                float(group["A_MEDIAN"].mean())
                if group["A_MEDIAN"].notna().any() else None
            ),
            "avg_automation_risk": round(
                float(group["automation_probability"].mean()), 4
            ) if group["automation_probability"].notna().any() else 0.0,
            "top_careers":         top_careers,
        })

    results.sort(key=lambda x: x["avg_gcsi"], reverse=True)
    return results


@app.get("/dashboard/field/{field_name}")
def dashboard_field(field_name: str):
    group = data.program_recs[
        data.program_recs["broad_field"].str.lower() ==
        field_name.lower().strip()
    ]

    if group.empty:
        raise HTTPException(status_code=404,
                            detail=f"Field '{field_name}' not found")

    top_careers = (
        group.groupby("career_match")
        .agg(
            avg_hybrid=("hybrid_score", "mean"),
            avg_gcsi=("GCSI", "mean"),
            avg_salary=("A_MEDIAN", "mean"),
            avg_automation=("automation_probability", "mean"),
            program_count=("program_name", "nunique"),
        )
        .sort_values("avg_hybrid", ascending=False)
        .head(10)
        .reset_index()
    )

    careers_list = []
    for _, row in top_careers.iterrows():
        careers_list.append({
            "career_match":   str(row["career_match"]),
            "avg_hybrid":     round(float(row["avg_hybrid"]), 4),
            "avg_gcsi":       round(float(row["avg_gcsi"]), 2),
            "avg_salary":     safe(float(row["avg_salary"])),
            "avg_automation": safe(float(row["avg_automation"])),
            "program_count":  int(row["program_count"]),
        })

    return {
        "broad_field":         field_name,
        "total_programs":      int(group["program_name"].nunique()),
        "avg_gcsi":            round(float(group["GCSI"].mean()), 2),
        "avg_salary":          safe(float(group["A_MEDIAN"].mean())),
        "avg_automation_risk": safe(float(group["automation_probability"].mean())),
        "gcsi_min":            round(float(group["GCSI"].min()), 2),
        "gcsi_max":            round(float(group["GCSI"].max()), 2),
        "top_careers":         careers_list,
    }


@app.get("/dashboard/career/{career_name}", response_model=CareerDetail)
def dashboard_career(career_name: str):
    row = data.occupation_gcsi[
        data.occupation_gcsi["occupation_name_lower"] ==
        career_name.lower().strip()
    ]

    if row.empty:
        raise HTTPException(status_code=404,
                            detail=f"Career '{career_name}' not found")

    row  = row.iloc[0]
    soc6 = str(row["SOC6"]).strip()

    skills = data.top_skills_map.get(soc6)
    tech   = data.tech_map.get(soc6, {})

    return {
        "career_match":           str(row["occupation_name"]),
        "SOC6":                   soc6,
        "GCSI":                   round(float(row["GCSI"]), 2),
        "income_strength":        safe(float(row.get("income_strength", None))),
        "employment_scale":       safe(float(row.get("employment_scale", None))),
        "wage_stability":         safe(float(row.get("wage_stability", None))),
        "automation_safety":      safe(float(row.get("automation_safety", None))),
        "A_MEDIAN":               safe(float(row.get("A_MEDIAN", None))),
        "TOT_EMP":                safe(float(row.get("TOT_EMP", None))),
        "automation_probability": safe(float(row.get("automation_probability", None))),
        "top_skills":             skills,
        "technology_items":       safe(tech.get("technology_items")),
        "hot_tech_items":         safe(tech.get("hot_tech_items")),
        "in_demand_items":        safe(tech.get("in_demand_items")),
    }


# ── Recommend ─────────────────────────────────────────────────────────────────

@app.get("/recommend/fields", response_model=List[DropdownField])
def recommend_fields():
    counts = (
        data.field_dropdown
        .groupby("broad_field")["program_name"]
        .nunique()
        .reset_index()
        .rename(columns={"program_name": "program_count"})
        .sort_values("broad_field")
    )
    return [
        {"broad_field": str(row["broad_field"]),
         "program_count": int(row["program_count"])}
        for _, row in counts.iterrows()
    ]


@app.get("/recommend/programs/{field_name}",
         response_model=List[DropdownProgram])
def recommend_programs(
    field_name: str,
    search: Optional[str] = Query(None)
):
    group = data.field_dropdown[
        data.field_dropdown["broad_field"].str.lower() ==
        field_name.lower().strip()
    ]

    if group.empty:
        raise HTTPException(status_code=404,
                            detail=f"Field '{field_name}' not found")

    if search:
        group = group[
            group["program_name"].str.lower().str.contains(
                search.lower().strip(), na=False)
        ]

    group = group.sort_values("program_name")

    return [
        {"program_name": str(row["program_name"]),
         "program_type": str(row["program_type"]),
         "degree_norm":  str(row["degree_norm"])}
        for _, row in group.iterrows()
    ]


@app.get("/recommend/{program_name}",
         response_model=RecommendationResponse)
def recommend(
    program_name: str,
    program_type: Optional[str] = Query(None),
    top_n: int = Query(10, ge=1, le=20)
):
    result = get_recommendations(
        program_name=program_name,
        program_type=program_type,
        top_n=top_n
    )
    if result is None:
        raise HTTPException(status_code=404,
                            detail=f"Program '{program_name}' not found")
    return result


@app.get("/dashboard/careers/search")
def search_careers(q: str = Query(..., min_length=2)):
    matches = data.occupation_gcsi[
        data.occupation_gcsi["occupation_name"].str.lower()
        .str.contains(q.lower().strip(), na=False)
    ][["occupation_name", "GCSI", "A_MEDIAN"]].head(15)

    return [
        {
            "occupation_name": str(row["occupation_name"]),
            "GCSI":            round(float(row["GCSI"]), 2),
            "A_MEDIAN":        None if pd.isna(row["A_MEDIAN"])
                               else float(row["A_MEDIAN"]),
        }
        for _, row in matches.iterrows()
    ]