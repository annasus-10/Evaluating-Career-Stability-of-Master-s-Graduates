# Project Progress Report: Data Integration Baseline for GCSI-Based Recommendation Dashboard

## Objective of this Phase

This progress phase focused on building the **integration baseline** between degree/program data and occupation labor-market data.  

The goal was **not** to deliver the final recommendation engine, but to establish a **reliable mapping layer** required before GCSI-based ranking.

---

## Work Completed

- Completed data cleaning pipelines for masters programs and occupations  
- Standardized degree and occupation text fields for semantic matching  
- Built Sentence Transformer-based semantic mapping from degree text to occupation candidates  
- Shifted from fixed top-k matching to threshold-based candidate mapping to avoid premature ranking  
- Reconstructed mapping back to original program rows, including `program_name` and `program_type`, to support dashboard use cases  
- Produced dashboard-ready candidate outputs at both degree level and program level  

---

## Current Baseline Outputs

- Degree-to-career candidate mapping above semantic threshold  
- Degree-level candidate statistics for coverage and quality checks  
- Program-level long candidate table  
  - (`program_name`, `program_type`, matched careers, similarity)  
- Program-level best-candidate table for baseline linkage  

---

## Why This Matters for the Final System

This mapping layer is the **required bridge** between the two source datasets.  

It enables attaching occupation-level metrics such as:

- Income  
- Employment scale  
- Wage stability  
- Automation risk  

to programs/degrees, which is necessary before computing final **GCSI-driven recommendation scores**.

---

## Scope Boundary in This Progress Stage

### Not Included Yet

- Final composite recommendation scoring policy  
- Final top recommendation ranking logic  
- Full recommendation interface behavior and user evaluation  

### Included

- Cleaned data foundation  
- Semantic connection layer  
- Program-level reconstruction for downstream dashboard integration  

---

## Next Phase Plan

- Compute and validate occupation-level GCSI components and normalized scores  
- Merge GCSI into mapped candidates  
- Apply final transparent scoring rule that combines semantic fit and GCSI  
- Produce final recommendation views for dashboard presentation  
