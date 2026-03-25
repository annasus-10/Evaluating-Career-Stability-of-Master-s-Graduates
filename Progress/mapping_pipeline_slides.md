# Degree-to-Career Mapping Pipeline (Slide Version)

## 1. Objective
Build a reliable bridge between two different datasets:
- Dataset A: masters programs (program_name, program_type, degree text)
- Dataset B: occupations/careers

Output needed for recommendation and dashboard work:
- program-level career candidates
- similarity scores for ranking/filtering

---

## 2. End-to-End Pipeline (From clean.ipynb to final mapping)

### Stage A: Cleaning and Normalization (clean.ipynb)
1. Load raw masters and occupation datasets.
2. Standardize text (lowercase, spacing, punctuation cleanup).
3. Clean noisy degree labels (remove junk tokens, artifacts, tags, route/foundation/track terms, etc.).
4. Produce final normalized degree field (degree_final) for matching.
5. Export cleaned files for mapping.

Why this stage matters:
- Reduces label noise.
- Makes semantically similar labels map consistently.
- Prevents bad matches caused by formatting artifacts.

### Stage B: Semantic Candidate Mapping (map.ipynb)
1. Encode cleaned degree labels and occupation labels using Sentence Transformer (all-MiniLM-L6-v2).
2. Compute cosine similarity between degree and occupation embeddings.
3. Keep candidate pairs at threshold >= 0.30.
4. Save degree-level candidate table and candidate statistics.

Why this stage matters:
- Captures semantic similarity beyond exact word overlap.
- Produces a candidate pool for later ranking with additional signals (e.g., GCSI).

### Stage C: Program-Level Reconstruction (map.ipynb)
1. Join degree-level candidates back to original program rows.
2. Build long candidate table (many careers per program).
3. Build best-match table (top career per program at current stage).

Why this stage matters:
- Restores business context (program_name + program_type).
- Makes results ready for dashboard display and next-stage recommendation logic.

### Stage D: O*NET Skill and Technology Enrichment
1. Normalize O*NET-SOC Code to SOC6 (drop decimal suffix).
2. Join SOC6 to project occupation universe from automation data.
3. Build occupation-skill bridge from O*NET Skills, Knowledge, Abilities, and Technology Skills.
4. Aggregate into skill-demand summary for dashboard charts.
5. Track coverage so occupations with zero skills are visible.

Why this stage matters:
- Adds career-specific skill context beyond semantic title matching.
- Enables skill-demand and technology-demand views in the dashboard.
- Preserves "no skill mapped yet" occupations for transparency.

---

## 3. Main Showcase: How Text Turns Into Career Matches

### 3.1 Before and After Cleaning (Real rows from output)

| program_name | degree_source (before) | degree_final (after) |
|---|---|---|
| Information Technology (ITM) - 21 Month | information technology itm 21 month | information technology itm |
| Information Technology - 12 Month | information technology 12 month | information technology |
| Public Administration (Online pathway) | public administration online pathway | public administration |
| Tourism (Tourism Stream) | tourism tourism stream | tourism tourism |
| Teaching - Primary R-7 | teaching primary r 7 | teaching primary r |
| Economics by coursework | economics by coursework | economics by |

This is the key transition you wanted to show: noisy degree text is normalized first, then semantic mapping is done on degree_final.

### 3.2 How Sentence Transformer Mapping Works
1. Input text to model: degree_final labels and occupation/career labels.
2. all-MiniLM-L6-v2 converts each text into an embedding vector.
3. Similarity is computed with cosine similarity:

$$
	ext{sim}(d, c)=\frac{d\cdot c}{\|d\|\|c\|}
$$

4. Keep candidates where similarity >= 0.30.
5. Reattach candidates to each program row.

### 3.3 Example: From Cleaned Degree to Career Match

| degree_final | matched career | similarity |
|---|---|---:|
| information technology itm | computer and information systems managers | 0.6170 |
| information technology | computer and information research scientists | 0.6339 |
| public administration | administrative services managers | 0.6438 |
| tourism tourism | tour and travel guides | 0.5548 |
| teaching primary r | secondary school teachers | 0.4703 |
| economics by | economists | 0.7386 |

---

## 4. Run Summary Table (Scanned from notebook result)

| Metric | Value |
|---|---:|
| masters_rows | 57,085 |
| occupations_rows | 1,120 |
| unique_degree_labels | 22,641 |
| unique_occupation_labels | 1,119 |
| degree_candidate_rows | 1,215,700 |
| program_candidate_rows | 4,357,770 |
| program_best_rows | 57,085 |
| avg_candidates_per_degree | 53.69 |
| median_candidates_per_degree | 35 |
| similarity_min | 0.30 |
| similarity_max | 1.00 |

---

## 5. Threshold Sensitivity Table (Scanned from notebook result)

| threshold | candidate_rows | unique_degrees | unique_careers | avg_candidates_per_degree |
|---:|---:|---:|---:|---:|
| 0.30 | 1,215,700 | 22,641 | 1,119 | 53.69 |
| 0.35 | 639,714 | 21,912 | 1,112 | 29.19 |
| 0.40 | 331,462 | 20,396 | 1,091 | 16.25 |
| 0.45 | 169,809 | 18,179 | 1,037 | 9.34 |

Interpretation:
- Increasing threshold decreases candidate volume.
- Higher threshold means stricter matching and lower recall.
- 0.30 currently acts as broad candidate-generation baseline.

---

## 6. Final Program-Level Mapping Sample (Scanned from notebook result)

| program_name | program_type | degree_source | degree_final | career_match | similarity |
|---|---|---|---|---|---:|
| Economics | MSc | economics | economics | economists | 0.8615 |
| Political Science and International Affairs | Master | political science and international affairs | political science and international affairs | political scientists | 0.6841 |
| Business Administration | MBA | business administration | business administration | administrative services managers | 0.6968 |
| Computer and Information Science | MSc | computer science | computer science | computer programmers | 0.7445 |
| Industrial Engineering and Systems Management | MEng | industrial engineering and systems management | industrial engineering and systems management | industrial production managers | 0.7183 |

---

## 7. New Skill and Technology Layer (O*NET)

### 7.1 New Outputs Added

| File | Role |
|---|---|
| datasets/mapping/occupation_base_soc.csv | Occupation base dimension (all SOC careers) |
| datasets/mapping/occupation_skill_bridge_onet.csv | Unified occupation-to-skill bridge |
| datasets/mapping/skill_demand_summary_onet.csv | Aggregated skill demand metrics |
| datasets/mapping/occupation_skill_coverage_onet.csv | Coverage QA (has_skills and skill_row_count) |
| datasets/mapping/occupation_technology_skills_onet.csv | Detailed technology skills per occupation |
| datasets/mapping/occupation_technology_skills_onet_summary.csv | Occupation-level technology summary |

### 7.2 Coverage Snapshot

| Metric | Value |
|---|---:|
| occupation_base_rows | 702 |
| occupation_skill_bridge_rows | 94,682 |
| skill_demand_summary_rows | 7,086 |
| occupations_with_skills | 618 |
| occupations_without_skills | 84 |
| occupation_technology_skill_rows | 21,732 |

### 7.3 Why This Helps the Dashboard
- Career page: show mapped skills, abilities, knowledge, and technology tools per occupation.
- Skill-demand page: rank skills by occupation coverage and average importance.
- Data-quality page: explicitly flag occupations with no mapped skill records.

---

## 8. Key Talking Points for Slides
- The mapping layer is the integration bridge between program data and career outcomes.
- Cleaning quality directly improves semantic matching quality.
- Sentence Transformer gives stronger semantic behavior than basic TF-IDF in this dataset.
- O*NET enrichment adds explicit career-specific skill and technology context.
- Thresholded candidates create a flexible pool for downstream ranking.
- This is now a stronger baseline before adding GCSI and final recommendation scoring.

---

## 9. Suggested Slide Order
1. Problem and objective
2. Data sources
3. Main showcase: before -> after cleaning
4. Main showcase: Sentence Transformer flow (embedding + cosine + threshold)
5. Run summary table
6. Threshold sensitivity table
7. Program-level sample outputs
8. O*NET skill and technology enrichment
9. Coverage snapshot and data-quality view
10. Next step: GCSI + ranking policy

---

## 10. Data Dictionary Reference
For dashboard implementation details, use the mapping folder guide:
- datasets/mapping/README.md
