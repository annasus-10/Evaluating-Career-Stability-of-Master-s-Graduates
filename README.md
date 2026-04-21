# CareerScope — Dataset Guide

All datasets are stored on Google Drive:  
**https://drive.google.com/drive/folders/1iYCo4m1O8UmIHUXf6DaVW3aO6X3Z_YLZ?usp=sharing**

---

## Folder Structure

```
datasets/
├── og/          — original raw source files
├── cleaned/     — cleaned and normalized files ready for mapping
├── mapping/     — intermediate mapping outputs from the pipeline
└── final/       — final enriched files used by the API
```

---

## og/ — Original Source Files

| File | Description |
|---|---|
| `mastersportal-programs.csv` | Raw masters program dataset from MastersPortal via Kaggle. Contains program name, university, country, and degree type for programs worldwide. Filtered to US scope for the project. |
| `occupation-salary.xlsx` | BLS Occupational Employment and Wage Statistics (OES). Contains median salary, employment size, and wage percentiles (P10, P25, P75, P90) for ~1,394 US occupations at detailed level. |
| `automation-data-by-state.csv` | Automation probability per occupation with employment counts broken down by US state. 702 occupations. Source: Frey & Osborne automation risk estimates matched to SOC codes. |

---

## cleaned/ — Cleaned Files

| File | Description |
|---|---|
| `masters_cleaned_for_mapping.csv` | Masters programs after text normalization. Contains `program_name`, `program_type`, `degree_norm` (cleaned label used for semantic matching), and `remove_flag`. 57,085 rows. |
| `masters_with_fields.csv` | Same as above with an added `broad_field` column assigning each program to one of 14 academic fields. Used for the two-level dropdown in the recommendation UI. |
| `occupations_cleaned_for_mapping.csv` | Cleaned occupation labels used as targets during semantic mapping. 1,120 rows. |

---

## mapping/ — Pipeline Intermediate Files

| File | Description |
|---|---|
| `occupation_base_soc.csv` | Master occupation dimension table. One row per occupation with SOC6 code, occupation name, automation probability, and O*NET title. 702 rows. |
| `occupation_skill_bridge_onet.csv` | Occupation-to-skill bridge from O*NET. One row per occupation × skill item covering Skills, Knowledge, Abilities, and Technology. Includes importance and level scores. 94,682 rows. |
| `occupation_skill_coverage_onet.csv` | QA table showing which occupations have O*NET skill records. Includes `has_skills` flag and `skill_row_count`. 702 rows. |
| `occupation_technology_skills_onet.csv` | Technology tools per occupation from O*NET. Includes commodity title, hot technology flag, and in-demand flag. 21,732 rows. |
| `occupation_technology_skills_onet_summary.csv` | Aggregated technology counts per occupation — total tools, hot tech count, in-demand count. One row per occupation. 618 rows. |
| `skill_demand_summary_onet.csv` | Pre-aggregated skill demand metrics. One row per skill × skill source with average importance, average level, and occupation coverage count. 7,086 rows. |
| `degree_career_sentence_transformer_candidates_thr30.csv` | Degree-level semantic candidate pairs at similarity threshold ≥ 0.30. One row per degree label × career match. Used for threshold experiments and candidate quality analysis. |
| `degree_career_sentence_transformer_candidate_stats_thr30.csv` | Candidate volume statistics per degree label — candidate count, max similarity, mean similarity. Used for diagnostics and distribution analysis. |
| `program_career_sentence_transformer_best_thr30.csv` | Best career match per program row. One row per program with top-ranked career and similarity score. 57,085 rows. |
| `program_career_sentence_transformer_candidates_thr30_long.csv` | All career candidates per program at threshold ≥ 0.30, ranked by match_rank. 4,357,772 rows. |
| `occupation_gcsi.csv` | Occupation GCSI scores. One row per occupation with all four GCSI components (income strength, employment scale, wage stability, automation safety) and the final composite score (0–100). 702 rows. |
| `program_best_enriched_gcsi.csv` | Best-match table enriched with GCSI scores and hybrid scores. One row per program. Superseded by `program_recommendations.csv` in the final pipeline. 57,085 rows. |
| `program_field_dropdown.csv` | Two-level dropdown lookup table. Maps each program to its broad field. Used by the API to power the field → program selection UI. 27,793 rows. |
| `program_recommendations.csv` | Final recommendation table. Top 15 careers per program ranked by hybrid score, enriched with GCSI, salary, automation probability, and broad field. Built from the full candidates table. 365,035 rows. |

---

## final/ — API-Ready Files

These are the five files loaded by the production API. Parquet versions are used in Docker for faster loading and smaller image size.

| File | Description |
|---|---|
| `occupation_gcsi.csv` / `.parquet` | GCSI scores for all 702 occupations with component breakdown. |
| `program_recommendations.csv` / `.parquet` | Final ranked career recommendations per program. Main recommendation data source. |
| `program_field_dropdown.csv` / `.parquet` | Field → program dropdown lookup for the recommendation UI. |
| `occupation_skill_bridge_onet.csv` / `.parquet` | Skills and abilities per occupation used to populate career skill cards. |
| `occupation_technology_skills_onet_summary.csv` / `.parquet` | Technology tool counts per occupation used in career detail views. |