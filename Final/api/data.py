import pandas as pd
import numpy as np
import os

BASE = os.path.join(os.path.dirname(__file__), "..", "datasets")

def _path(f):
    return os.path.join(BASE, f)

print("Loading datasets...")

occupation_gcsi  = pd.read_parquet(_path("occupation_gcsi.parquet"))
program_recs     = pd.read_parquet(_path("program_recommendations.parquet"))
field_dropdown   = pd.read_parquet(_path("program_field_dropdown.parquet"))
skill_bridge     = pd.read_parquet(_path("occupation_skill_bridge_onet.parquet"))
tech_summary     = pd.read_parquet(_path("occupation_technology_skills_onet_summary.parquet"))

# Normalize keys
occupation_gcsi["occupation_name_lower"] = (
    occupation_gcsi["occupation_name"].str.lower().str.strip()
)
program_recs["program_name_lower"] = (
    program_recs["program_name"].str.lower().str.strip()
)
program_recs["SOC6"]    = program_recs["SOC6"].astype(str).str.strip()
occupation_gcsi["SOC6"] = occupation_gcsi["SOC6"].astype(str).str.strip()
skill_bridge["SOC6"]    = skill_bridge["SOC6"].astype(str).str.strip()
tech_summary["SOC6"]    = tech_summary["SOC6"].astype(str).str.strip()

# Top 5 skills per occupation
top_skills_map = (
    skill_bridge
    .dropna(subset=["SOC6", "skill_name", "importance"])
    .sort_values("importance", ascending=False)
    .groupby("SOC6")
    .head(5)
    .groupby("SOC6")["skill_name"]
    .apply(list)
    .to_dict()
)

# Tech summary dict
tech_map = tech_summary.set_index("SOC6")[
    ["technology_items", "hot_tech_items", "in_demand_items"]
].to_dict("index")

print(f"  occupation_gcsi: {occupation_gcsi.shape}")
print(f"  program_recs:    {program_recs.shape}")
print(f"  field_dropdown:  {field_dropdown.shape}")
print(f"  skill_bridge:    {skill_bridge.shape}")
print(f"  tech_summary:    {tech_summary.shape}")
print("All datasets loaded.")