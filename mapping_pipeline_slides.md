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

---

## 3. Run Summary Table (Scanned from notebook result)

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

## 4. Threshold Sensitivity Table (Scanned from notebook result)

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

## 5. Final Program-Level Mapping Sample (Scanned from notebook result)

| program_name | program_type | degree_source | degree_final | career_match | similarity |
|---|---|---|---|---|---:|
| Economics | MSc | economics | economics | economists | 0.8615 |
| Political Science and International Affairs | Master | political science and international affairs | political science and international affairs | political scientists | 0.6841 |
| Business Administration | MBA | business administration | business administration | administrative services managers | 0.6968 |
| Computer and Information Science | MSc | computer science | computer science | computer programmers | 0.7445 |
| Industrial Engineering and Systems Management | MEng | industrial engineering and systems management | industrial engineering and systems management | industrial production managers | 0.7183 |

---

## 6. Key Talking Points for Slides
- The mapping layer is the integration bridge between program data and career outcomes.
- Cleaning quality directly improves semantic matching quality.
- Sentence Transformer gives stronger semantic behavior than basic TF-IDF in this dataset.
- Thresholded candidates create a flexible pool for downstream ranking.
- This is a baseline integration stage before adding GCSI and final recommendation scoring.

---

## 7. Suggested Slide Order
1. Problem and objective
2. Data sources
3. Cleaning pipeline (clean.ipynb)
4. Semantic mapping pipeline (map.ipynb)
5. Run summary table
6. Threshold sensitivity table
7. Program-level sample outputs
8. Next step: GCSI + ranking policy
