# Mapping Datasets Guide

This folder contains all intermediate and final mapping outputs used by the project pipeline.

## Quick Start: Which file for what?

- Main dashboard fact table for skills: occupation_skill_bridge_onet.csv
- Base occupation list (all SOC rows, including no-skill rows): occupation_base_soc.csv
- Skill demand chart source (already aggregated): skill_demand_summary_onet.csv
- Coverage QA (which occupations have zero skills): occupation_skill_coverage_onet.csv
- Program to career mapping (best row per program): program_career_sentence_transformer_best_thr30.csv
- Program to career mapping (all candidates): program_career_sentence_transformer_candidates_thr30_long.csv

## File-by-file explanation

| File | Grain | Purpose | Where produced | When to use |
|---|---|---|---|---|
| degree_career_sentence_transformer_candidates_thr30.csv | one row per degree_clean x career_match candidate | Degree-level semantic candidate pool at similarity threshold 0.30 | map.ipynb | Use for degree-level analysis, threshold experiments, and candidate quality checks |
| degree_career_sentence_transformer_candidate_stats_thr30.csv | one row per degree_clean | Candidate volume stats per degree | map.ipynb | Use for diagnostics, distribution plots, and strictness tuning |
| program_career_sentence_transformer_candidates_thr30_long.csv | one row per program x career candidate | Program-level candidate table after reconstructing from degree mapping | map.ipynb | Use for recommendation candidate generation and drill-down views |
| program_career_sentence_transformer_best_thr30.csv | one row per program | Best current career match per program | map.ipynb | Use for top-match cards, summaries, and demo tables |
| occupation_technology_skills_onet.csv | one row per occupation x technology skill | O*NET technology skill details mapped to project occupation SOC universe | build_onet_technology_outputs.py | Use when dashboard needs concrete tools/technology examples |
| occupation_technology_skills_onet_summary.csv | one row per occupation (SOC6) | Technology skill counts and hot/in-demand counts per occupation | build_onet_technology_outputs.py | Use for quick occupation ranking by technology intensity |
| occupation_base_soc.csv | one row per occupation (SOC6) | Master occupation dimension for all automation SOC rows | build_onet_skill_bridge.py | Use as the base table to keep zero-skill occupations visible |
| occupation_skill_bridge_onet.csv | one row per occupation x skill item | Unified bridge of Skills, Knowledge, Abilities, Technology | build_onet_skill_bridge.py | Primary dashboard source for skill drill-down and filtering |
| skill_demand_summary_onet.csv | one row per skill_source x skill_name | Aggregated skill demand metrics across occupations | build_onet_skill_bridge.py | Use for skill demand charts and top-skill leaderboards |
| occupation_skill_coverage_onet.csv | one row per occupation (SOC6) | Coverage QA table with has_skills flag and skill row count | build_onet_skill_bridge.py | Use for data quality panel and missing-coverage alerts |

## Join keys and schema notes

- Main join key across occupation/skill files is SOC6.
- SOC6 format is six-digit SOC with hyphen, for example 11-3021.
- O*NET source key O*NET-SOC Code is normalized by dropping decimal suffixes, for example 11-3021.00 -> 11-3021.
- program_row_id is used within program-level mapping outputs.
- skill_source values in occupation_skill_bridge_onet.csv are: skills, knowledge, abilities, technology.

## Recommended dashboard data model

1. Occupation dimension:
- Source: occupation_base_soc.csv
- Role: master list of careers and automation probability

2. Occupation-skill bridge:
- Source: occupation_skill_bridge_onet.csv
- Role: one-to-many skill records for each occupation

3. Skill-demand fact:
- Source: skill_demand_summary_onet.csv
- Role: pre-aggregated metrics for charts and KPI cards

4. Coverage/QA fact:
- Source: occupation_skill_coverage_onet.csv
- Role: identifies occupations with no mapped skills

## Current coverage snapshot

From the latest generated files:
- occupation_base_soc.csv rows: 702
- occupation_skill_bridge_onet.csv rows: 94682
- skill_demand_summary_onet.csv rows: 7086
- occupation_skill_coverage_onet.csv occupations with skills: 618
- occupation_skill_coverage_onet.csv occupations without skills: 84
- occupation_technology_skills_onet.csv rows: 21732

## Where and when to use each group in the workflow

- During semantic matching tuning:
  - Use degree_career_sentence_transformer_candidates_thr30.csv
  - Use degree_career_sentence_transformer_candidate_stats_thr30.csv

- During program recommendation development:
  - Use program_career_sentence_transformer_candidates_thr30_long.csv
  - Use program_career_sentence_transformer_best_thr30.csv

- During skills and demand dashboard development:
  - Use occupation_base_soc.csv
  - Use occupation_skill_bridge_onet.csv
  - Use skill_demand_summary_onet.csv
  - Use occupation_skill_coverage_onet.csv
  - Use occupation_technology_skills_onet.csv and occupation_technology_skills_onet_summary.csv
