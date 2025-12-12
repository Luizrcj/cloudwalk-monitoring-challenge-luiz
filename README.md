# PROJECT NAME AND OBJECTIVE
Cloudwalk Monitoring Challenge – Analysis of checkout metrics with anomaly detection

# BRIEF DESCRIPTION
This project analyzes checkout metrics from CSV files, calculates percentage variations compared to previous periods, detects anomalies, and generates reports automatically.

# FILE STRUCTURE
- `data/` → CSV files with raw checkout metrics (`checkout_1.csv`, `checkout_2.csv`)
- `notebook_steps.ipynb` → Detailed step-by-step analysis, showing calculations and validations
- `notebook_final.ipynb` → Final version generating reports automatically
- `README.md` → Project documentation (this file)
- `requirements.txt` → Python libraries required to run the notebooks

# HOW TO RUN
1. Open `notebook_final.ipynb` in VSCode
2. Install dependencies from `requirements.txt` (e.g., run `pip install -r requirements.txt`)
3. Run all cells to generate anomaly reports