# Cloudwalk Monitoring Challenge

## Project Objective
Analysis of checkout and transaction metrics with anomaly detection, using historical comparisons to support monitoring and alerting scenarios.

## Brief Description
This project processes raw CSV data related to checkout and transaction events, calculates variations compared to previous periods (yesterday, last week, and monthly averages), detects anomalies, and generates structured reports automatically.

The goal is to simulate a real monitoring workflow with clean, reproducible analysis.

## Project Structure
- `data/`  
  Raw CSV input files (`checkout_1.csv`, `checkout_2.csv`, `transactions_1.csv`, `transactions_2.csv`)

- `notebooks/`  
  - `notebook_checkout_final.ipynb` → Final checkout analysis and anomaly detection  
  - `notebook_transactions_final.ipynb` → Transaction status analysis and aggregation  

- `reports/`  
  Generated outputs and reports:
  - Checkout anomaly reports (`checkout_*_report.csv`)
  - Transaction metrics reports (`transactions_*_report.csv`)
  - `alerts_report.txt`

- `README.md`  
  Project documentation

- `requirements.txt`  
  Python dependencies required to run the notebooks

## How to Run
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
3. Open the notebooks in VS Code or Jupyter
4. Run all cells from top to bottom

All reports will be generated automatically inside the reports/ directory.