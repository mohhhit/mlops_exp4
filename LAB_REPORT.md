# EXPERIMENT NO. 04: DATA INGESTION WITH PREPROCESSING PIPELINE

---

## 1. EXPERIMENT DETAILS
* **Subject:** Machine Learning Operations (MLOps)
* **Experiment No:** 04
* **Title:** Automated Data Ingestion with Data Preprocessing and Feature Engineering Pipeline
* **Domain / Problem Statement:** Air Quality Index (AQI) Prediction & Classification
* **Data Source:** Open-Meteo Air Quality REST API (Live, Free, Public)

---

## 2. AIM & OBJECTIVES
### Aim:
To design, implement, and validate an automated, modular MLOps data ingestion and preprocessing pipeline that fetches real-world atmospheric pollutant data, performs automated cleaning and feature engineering, manages versioned artifacts, and produces machine-learning-ready training and testing datasets.

### Objectives:
1. Ingest raw multi-attribute data from a live REST API endpoint.
2. Implement automated data preprocessing to handle missing sensor values, duplicate records, and invalid values.
3. Engineer domain-specific and temporal features (e.g., pollutant ratios, cyclical hour encodings, AQI categories).
4. Implement semantic artifact versioning (`v1` and `v2`) to demonstrate data lineage and version control in MLOps.
5. Create ML-ready train/test splits for downstream model training.
6. Automate data validation checks to ensure zero-defect data quality before model consumption.

---

## 3. SOFTWARE & HARDWARE REQUIREMENTS
* **Operating System:** Windows 10/11, Linux, or macOS
* **Programming Language:** Python 3.10+
* **Key Libraries:**
  * `requests`: For HTTP REST API data ingestion
  * `pandas`: For structured tabular manipulation and preprocessing
  * `numpy`: For mathematical and cyclical trigonometric transformations
  * `json`, `os`, `argparse`: Standard utility modules for artifact management and CLI orchestration
* **Data Provider:** Open-Meteo Air Quality API (`https://air-quality-api.open-meteo.com`)

---

## 4. ARCHITECTURE & WORKFLOW

```
┌─────────────────────────────────────────────────────────────┐
│             Open-Meteo Air Quality REST API                 │
└──────────────────────────────┬──────────────────────────────┘
                               │ HTTP GET (Hourly Pollutants)
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 1: Ingestion Pipeline (ingestion.py)                 │
│  - Queries endpoint with city coordinates & day range       │
│  - Saves: artifacts/<version>/raw_data.json                 │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 2: Preprocessing Pipeline (preprocessing.py)         │
│  - Flattens JSON to tabular DataFrame                       │
│  - Forward/backward fill + median imputation for sensors    │
│  - Enforces physical bounds (clips negative values)         │
│  - Saves: artifacts/<version>/cleaned_data.csv              │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 3: Transformation Pipeline (transformation.py)       │
│  - Extracts hour, day of week, weekend flags                │
│  - Cyclical encoding (sin/cos of hour)                      │
│  - Computes fine-to-coarse ratio: PM2.5 / PM10              │
│  - Discretizes AQI into categories (Good, Moderate, etc.)   │
│  - Splits data into 80% Train and 20% Test                  │
│  - Saves: processed_data.csv, train_data.csv, test_data.csv │
└──────────────────────────────┬──────────────────────────────┘
                               │
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  STAGE 4: Validation Pipeline (validation.py)               │
│  - Verifies zero nulls, zero duplicates, valid ranges       │
│  - Emits quality status: "PASS"                             │
│  - Saves: artifacts/<version>/validation_report.json        │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. PROBLEM STATEMENT & DATA DESCRIPTION
### Problem Statement:
Air pollution poses significant environmental and health risks. Building robust predictive models requires a continuous supply of clean, validated pollutant data. This pipeline automates the ingestion of atmospheric pollutants to classify air quality and predict the Air Quality Index (US AQI).

### Ingested Features:
1. `time`: ISO 8601 hourly timestamp
2. `pm10`: Particulate matter $\le 10\ \mu\text{m}\ (\mu\text{g}/\text{m}^3)$
3. `pm2_5`: Fine particulate matter $\le 2.5\ \mu\text{m}\ (\mu\text{g}/\text{m}^3)$
4. `carbon_monoxide`: CO concentration $(\mu\text{g}/\text{m}^3)$
5. `nitrogen_dioxide`: $\text{NO}_2$ concentration $(\mu\text{g}/\text{m}^3)$
6. `sulphur_dioxide`: $\text{SO}_2$ concentration $(\mu\text{g}/\text{m}^3)$
7. `ozone`: $\text{O}_3$ surface concentration $(\mu\text{g}/\text{m}^3)$
8. `us_aqi`: United States Air Quality Index (0 to 500+)

### Engineered Features:
* `hour`, `day_of_week`, `is_weekend`: Temporal indicator variables.
* `hour_sin`, `hour_cos`: Continuous trigonometric transformation representing the 24-hour diurnal cycle.
* `pm_ratio`: $\frac{\text{PM}_{2.5}}{\text{PM}_{10}}$ indicating the proportion of hazardous fine particles.
* `aqi_category`: Categorical classification (`Good`, `Moderate`, `Unhealthy_Sensitive`, `Unhealthy`).
* `aqi_category_code`: Numeric label encoding for ML classifiers.

---

## 6. ARTIFACT VERSIONING STRATEGY
In MLOps, datasets change over time as new data arrives or new regions are onboarded. This implementation uses folder-based semantic versioning:

| Version | Target City | Coordinates (Lat, Lon) | Time Window | Ingested Records |
| :--- | :--- | :--- | :--- | :--- |
| **v1** | Mumbai | 19.0760° N, 72.8777° E | Past 7 Days | 288 hourly records |
| **v2** | Delhi | 28.6139° N, 77.2090° E | Past 14 Days | 456 hourly records |

---

## 7. EXECUTION STEPS & COMMANDS

### Step 1: Verify API Connectivity
```bash
python test_api.py
```

### Step 2: Run End-to-End Pipeline for Version 1 (Mumbai)
```bash
python pipeline.py --version v1
```

### Step 3: Run End-to-End Pipeline for Version 2 (Delhi)
```bash
python pipeline.py --version v2
```

### Step 4: Run Both Versions Simultaneously
```bash
python pipeline.py --version all
```

---

## 8. RESULTS & VALIDATION REPORTS

### Directory Structure of Generated Artifacts:
```
artifacts/
├── v1/
│   ├── raw_data.json
│   ├── cleaned_data.csv
│   ├── processed_data.csv
│   ├── train_data.csv
│   ├── test_data.csv
│   └── validation_report.json
└── v2/
    ├── raw_data.json
    ├── cleaned_data.csv
    ├── processed_data.csv
    ├── train_data.csv
    ├── test_data.csv
    └── validation_report.json
```

### Validation Report Output (Version 1 - Mumbai):
```json
{
    "version": "v1",
    "total_records": 288,
    "train_records": 230,
    "test_records": 58,
    "missing_values": 0,
    "duplicates": 0,
    "invalid_aqi_values": 0,
    "invalid_pollutant_values": 0,
    "missing_required_columns": [],
    "status": "PASS"
}
```

### Validation Report Output (Version 2 - Delhi):
```json
{
    "version": "v2",
    "total_records": 456,
    "train_records": 364,
    "test_records": 92,
    "missing_values": 0,
    "duplicates": 0,
    "invalid_aqi_values": 0,
    "invalid_pollutant_values": 0,
    "missing_required_columns": [],
    "status": "PASS"
}
```

---

## 9. CONCLUSION & LEARNING OUTCOMES
1. Successfully built an automated MLOps data pipeline connecting a live REST API to clean, ML-ready datasets.
2. Implemented data imputation techniques suitable for continuous time-series sensor observations.
3. Applied feature engineering including cyclical hour encodings and domain pollutant ratios.
4. Demonstrated artifact versioning across different temporal and geographical configurations (`v1` and `v2`).
5. Established automated quality validation gates that ensure only validated data reaches the model training phase.

