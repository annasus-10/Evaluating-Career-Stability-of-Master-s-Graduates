# CareerScope API Documentation

**Version:** 1.0.0  
**Production URL:** `https://careerscope-api-production.up.railway.app`  
**Local URL:** `http://localhost:8000`  
**Interactive docs:** `https://careerscope-api-production.up.railway.app/docs`  
**Demo frontend:** `Final/demo.html` — open directly in browser, no server needed

---

## Overview

The CareerScope API provides career recommendation and stability data for masters degree graduates. It powers two core features:

- **Dashboard** — market-level overview of career stability across academic fields
- **Recommendations** — personalized top-career suggestions for a specific program

All responses are JSON. All endpoints are GET requests. No authentication required. CORS is open — any origin can call the API.

---

## Quick Start

```bash
# Check API is running
curl https://careerscope-api-production.up.railway.app/health

# Get all broad fields for dropdown
curl https://careerscope-api-production.up.railway.app/recommend/fields

# Get programs in a field
curl "https://careerscope-api-production.up.railway.app/recommend/programs/Computing%20%26%20Technology"

# Get career recommendations
curl "https://careerscope-api-production.up.railway.app/recommend/Economics?program_type=MSc&top_n=10"

# Get dashboard overview
curl https://careerscope-api-production.up.railway.app/dashboard/overview

# Search a career
curl "https://careerscope-api-production.up.railway.app/dashboard/careers/search?q=financial"
```

---

## Frontend Integration — Recommended Pattern

```javascript
const API = 'https://careerscope-api-production.up.railway.app';

// Step 1 — Load fields for Level 1 dropdown
const fields = await fetch(`${API}/recommend/fields`).then(r => r.json());

// Step 2 — Load programs for selected field (Level 2 dropdown)
const programs = await fetch(
  `${API}/recommend/programs/${encodeURIComponent(fieldName)}`
).then(r => r.json());

// Step 3 — Get recommendations for selected program
const recs = await fetch(
  `${API}/recommend/${encodeURIComponent(programName)}?program_type=${type}&top_n=10`
).then(r => r.json());

// Step 4 — Get career detail on click
const detail = await fetch(
  `${API}/dashboard/career/${encodeURIComponent(careerName)}`
).then(r => r.json());
```

---

## Endpoints

---

### `GET /health`

Confirms the API is running and all datasets are loaded.

**Parameters:** None

**Response:**
```json
{
  "status": "ok",
  "datasets": {
    "occupation_gcsi": 702,
    "program_recs": 365035,
    "field_dropdown": 27793,
    "skill_bridge": 94682,
    "tech_summary": 618
  }
}
```

---

### `GET /recommend/fields`

Returns all 14 broad academic fields for the Level 1 dropdown. Sorted alphabetically.

**Parameters:** None

**Response:** Array of field objects
```json
[
  { "broad_field": "Arts, Design & Media",              "program_count": 2284 },
  { "broad_field": "Business & Management",             "program_count": 3980 },
  { "broad_field": "Computing & Technology",            "program_count": 1558 },
  { "broad_field": "Education",                         "program_count": 1961 },
  { "broad_field": "Engineering",                       "program_count": 1476 },
  { "broad_field": "Environmental Sciences",            "program_count": 812  },
  { "broad_field": "Finance & Economics",               "program_count": 1289 },
  { "broad_field": "Health & Medicine",                 "program_count": 1823 },
  { "broad_field": "Humanities",                        "program_count": 1654 },
  { "broad_field": "Interdisciplinary & Other",         "program_count": 1543 },
  { "broad_field": "Law & Policy",                      "program_count": 1342 },
  { "broad_field": "Life Sciences & Biology",           "program_count": 987  },
  { "broad_field": "Physical & Mathematical Sciences",  "program_count": 1678 },
  { "broad_field": "Social Sciences",                   "program_count": 2087 }
]
```

| Field | Type | Description |
|---|---|---|
| `broad_field` | string | Field name — use this as the key for subsequent calls |
| `program_count` | integer | Number of unique programs in this field |

---

### `GET /recommend/programs/{field_name}`

Returns all programs within a broad field for the Level 2 dropdown.

**Path parameter:**
| Parameter | Type | Description |
|---|---|---|
| `field_name` | string | Broad field name exactly as returned by `/recommend/fields` |

**Query parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `search` | string | No | Filter programs by name (partial match, case insensitive) |

**Examples:**
```
GET /recommend/programs/Computing%20%26%20Technology
GET /recommend/programs/Health%20%26%20Medicine?search=nursing
GET /recommend/programs/Engineering?search=aerospace
```

**Response:** Array sorted alphabetically by program name
```json
[
  {
    "program_name": "Computer Science",
    "program_type": "MSc",
    "degree_norm": "computer science"
  }
]
```

| Field | Type | Description |
|---|---|---|
| `program_name` | string | Full program name — use this for the recommendation call |
| `program_type` | string | Degree type (MSc, MA, MBA, MEng, LLM, MFA, etc.) |
| `degree_norm` | string | Normalized degree label used internally |

**Error:**
```json
{ "detail": "Field 'Unknown Field' not found" }  // 404
```

---

### `GET /recommend/{program_name}`

**Main recommendation endpoint.** Returns top N career paths for a given program ranked by hybrid score (40% semantic similarity + 60% GCSI stability with similarity-scaled penalty).

**Path parameter:**
| Parameter | Type | Description |
|---|---|---|
| `program_name` | string | Full program name from `/recommend/programs` |

**Query parameters:**
| Parameter | Type | Required | Default | Constraints |
|---|---|---|---|---|
| `program_type` | string | No | null | Filter by degree type |
| `top_n` | integer | No | 10 | Min 1, max 20 |

**Examples:**
```
GET /recommend/Economics?program_type=MSc&top_n=10
GET /recommend/Computer%20Science?top_n=5
GET /recommend/Business%20Administration?program_type=MBA
GET /recommend/Nursing?program_type=Master&top_n=15
```

**Response:**
```json
{
  "program_name": "Economics",
  "program_type": "MSc",
  "broad_field": "Finance & Economics",
  "degree_norm": "economics",
  "total_candidates": 28,
  "recommendations": [
    {
      "career_match": "economists",
      "similarity": 0.8615,
      "GCSI": 34.4,
      "GCSI_imputed": false,
      "hybrid_score": 0.5510,
      "A_MEDIAN": 101050.0,
      "automation_probability": 0.43,
      "top_skills": [
        "Mathematics",
        "Economics and Accounting",
        "Written Comprehension",
        "Mathematical Reasoning",
        "Writing"
      ],
      "technology_items": 24,
      "hot_tech_items": 8
    }
  ]
}
```

**Top-level response fields:**

| Field | Type | Description |
|---|---|---|
| `program_name` | string | Program name |
| `program_type` | string | Degree type |
| `broad_field` | string | Broad academic field |
| `degree_norm` | string | Normalized degree label |
| `total_candidates` | integer | Total unique careers matched for this program |
| `recommendations` | array | Ranked career list (length ≤ top_n) |

**Recommendation item fields:**

| Field | Type | Nullable | Description |
|---|---|---|---|
| `career_match` | string | No | Occupation title |
| `similarity` | float | No | Semantic similarity (0–1) — how closely degree matches career |
| `GCSI` | float | No | Career stability score (0–100) |
| `GCSI_imputed` | boolean | No | `true` = GCSI estimated from median, no direct BLS match |
| `hybrid_score` | float | No | Final ranking score (see Hybrid Score section) |
| `A_MEDIAN` | float | Yes | Annual median salary USD |
| `automation_probability` | float | Yes | Automation risk (0–1). Lower = safer |
| `top_skills` | string[] | Yes | Top 5 skills by O*NET importance score |
| `technology_items` | integer | Yes | Total tech tools used in this occupation |
| `hot_tech_items` | integer | Yes | Emerging/hot technology tools count |

**Error:**
```json
{ "detail": "Program 'Unknown' not found" }  // 404
```

---

### `GET /dashboard/overview`

Returns field-level summary statistics for the market overview page. Sorted by average GCSI descending.

**Parameters:** None

**Response:**
```json
[
  {
    "broad_field": "Health & Medicine",
    "program_count": 1823,
    "avg_gcsi": 48.2,
    "avg_salary": 87450.0,
    "avg_automation_risk": 0.18,
    "top_careers": [
      "registered nurses",
      "physicians and surgeons",
      "health educators"
    ]
  }
]
```

| Field | Type | Nullable | Description |
|---|---|---|---|
| `broad_field` | string | No | Field name |
| `program_count` | integer | No | Unique programs |
| `avg_gcsi` | float | No | Average GCSI across all careers in this field |
| `avg_salary` | float | Yes | Average annual median salary |
| `avg_automation_risk` | float | No | Average automation probability |
| `top_careers` | string[] | No | Top 3 most common matched careers |

---

### `GET /dashboard/field/{field_name}`

Deep dive into a single field. Returns top 10 careers ranked by average hybrid score, plus field-level stats.

**Path parameter:**
| Parameter | Type | Description |
|---|---|---|
| `field_name` | string | Broad field name |

**Examples:**
```
GET /dashboard/field/Computing%20%26%20Technology
GET /dashboard/field/Health%20%26%20Medicine
GET /dashboard/field/Engineering
```

**Response:**
```json
{
  "broad_field": "Computing & Technology",
  "total_programs": 1558,
  "avg_gcsi": 51.3,
  "avg_salary": 98200.0,
  "avg_automation_risk": 0.22,
  "gcsi_min": 17.6,
  "gcsi_max": 71.4,
  "top_careers": [
    {
      "career_match": "computer and information systems managers",
      "avg_hybrid": 0.6548,
      "avg_gcsi": 61.91,
      "avg_salary": 135800.0,
      "avg_automation": 0.035,
      "program_count": 312
    }
  ]
}
```

**Top career item fields:**

| Field | Type | Nullable | Description |
|---|---|---|---|
| `career_match` | string | No | Occupation title |
| `avg_hybrid` | float | No | Average hybrid score across programs in this field |
| `avg_gcsi` | float | No | Average GCSI |
| `avg_salary` | float | Yes | Average annual salary |
| `avg_automation` | float | Yes | Average automation probability |
| `program_count` | integer | No | Programs mapping to this career |

---

### `GET /dashboard/career/{career_name}`

Full detail for a single occupation — GCSI component breakdown, salary, employment, skills, and technology tools.

**Path parameter:**
| Parameter | Type | Description |
|---|---|---|
| `career_name` | string | Exact occupation name in lowercase |

**Tip:** Use `/dashboard/careers/search?q=...` first to find the exact name.

**Examples:**
```
GET /dashboard/career/financial%20managers
GET /dashboard/career/registered%20nurses
GET /dashboard/career/software%20developers
GET /dashboard/career/computer%20and%20information%20systems%20managers
```

**Response:**
```json
{
  "career_match": "Financial Managers",
  "SOC6": "11-3031",
  "GCSI": 59.24,
  "income_strength": 0.72,
  "employment_scale": 0.58,
  "wage_stability": 0.61,
  "automation_safety": 0.93,
  "A_MEDIAN": 121750.0,
  "TOT_EMP": 543300.0,
  "automation_probability": 0.069,
  "top_skills": [
    "Critical Thinking",
    "Judgment and Decision Making",
    "Active Listening",
    "Reading Comprehension",
    "Speaking"
  ],
  "technology_items": 38,
  "hot_tech_items": 12,
  "in_demand_items": 8
}
```

**GCSI component fields (all normalized 0–1):**

| Field | Weight | Description |
|---|---|---|
| `income_strength` | 35% | Normalized median annual salary |
| `employment_scale` | 25% | Normalized total employment size |
| `wage_stability` | 20% | Inverted salary spread (P90–P10). Higher = narrower = more stable |
| `automation_safety` | 20% | `1 − automation_probability`. Higher = safer from automation |

**Error:**
```json
{ "detail": "Career 'unknown' not found" }  // 404
```

---

### `GET /dashboard/careers/search`

Search all 702 occupations by name. Primary use is autocomplete in the career lookup UI.

**Query parameters:**
| Parameter | Type | Required | Description |
|---|---|---|---|
| `q` | string | Yes | Search string, minimum 2 characters |

**Examples:**
```
GET /dashboard/careers/search?q=financial
GET /dashboard/careers/search?q=engineer
GET /dashboard/careers/search?q=nurse
GET /dashboard/careers/search?q=software
```

**Response:** Up to 15 matches
```json
[
  {
    "occupation_name": "Financial Managers",
    "GCSI": 59.24,
    "A_MEDIAN": 121750.0
  },
  {
    "occupation_name": "Financial Analysts",
    "GCSI": 37.08,
    "A_MEDIAN": 81760.0
  }
]
```

---

## GCSI — Graduate Career Stability Index

The GCSI is a composite score (0–100) measuring long-term career stability across four labor market dimensions.

**Formula:**
```
GCSI = (0.35 × IncomeStrength
      + 0.25 × EmploymentScale
      + 0.20 × WageStability
      + 0.20 × AutomationSafety) × 100
```

Each component is min-max normalized across all 702 occupations in the dataset.

**Score interpretation:**

| Range | Stability level |
|---|---|
| 55–100 | High — strong salary, large workforce, low automation risk |
| 40–54 | Moderate — average across most dimensions |
| 0–39 | Lower — high automation risk, small workforce, or volatile wages |

**Imputed GCSI:** 27.4% of career matches use an estimated GCSI (median = 41.78) because their occupation name could not be directly matched to the BLS database. These are flagged with `GCSI_imputed: true`. Show a visual indicator (asterisk, tooltip, or muted badge) when rendering imputed scores.

---

## Hybrid Score

The hybrid score is the final ranking signal for career recommendations.

**Formula:**
```
HybridScore = 0.40 × similarity
            + 0.60 × (GCSI/100) × min(1, similarity/0.65)
```

**Weight rationale:**
- GCSI is weighted at 60% because the project's core objective is career stability guidance
- Similarity leads at 40% to ensure careers are meaningfully related to the degree
- The `min(1, similarity/0.65)` penalty reduces GCSI contribution for loosely-matched careers, preventing high-GCSI but unrelated occupations from dominating results

---

## Data Coverage

| Dataset | Size | Notes |
|---|---|---|
| Masters programs | 57,085 rows, 23,780 unique programs | Global programs, US scope for labor data |
| Occupations with GCSI | 702 | BLS/O*NET US data only |
| Programs with real GCSI | 72.6% | Remaining 27.4% use median imputation |
| Occupations with skill data | 618 of 702 (88%) | O*NET coverage |
| Recommendation table | 365,035 rows | Top 15 careers per program, pre-ranked |

---

## Error Reference

| HTTP Status | When |
|---|---|
| 200 | Success |
| 404 | Program, field, or career name not found |
| 422 | Invalid parameter type or value out of allowed range |
| 500 | Server error |

All errors return:
```json
{ "detail": "Human-readable error message" }
```

---

## URL Encoding

Always encode special characters in path parameters using `encodeURIComponent()` in JavaScript.

| Character | Encoded |
|---|---|
| space | `%20` |
| `&` | `%26` |
| `+` | `%2B` |

**Common field name encodings:**
```
"Computing & Technology"          →  Computing%20%26%20Technology
"Health & Medicine"               →  Health%20%26%20Medicine
"Life Sciences & Biology"         →  Life%20Sciences%20%26%20Biology
"Physical & Mathematical Sciences" → Physical%20%26%20Mathematical%20Sciences
"Arts, Design & Media"            →  Arts%2C%20Design%20%26%20Media
"Interdisciplinary & Other"       →  Interdisciplinary%20%26%20Other
```

---

## Null Handling

These fields can be `null` — always check before rendering:

| Field | When null |
|---|---|
| `A_MEDIAN` | Occupation not in BLS salary data |
| `automation_probability` | Not in automation dataset |
| `top_skills` | Occupation not in O*NET skills data |
| `technology_items`, `hot_tech_items`, `in_demand_items` | Not in O*NET tech data |
| `avg_salary`, `avg_automation` | Field-level aggregates with no data |

**Suggested display:** Show `"N/A"` or `"—"` for null salary/risk values. Hide the skills section entirely if `top_skills` is null.
