# Banking Analytics & ML Project

![Python](https://img.shields.io/badge/python-3.11-blue)
![Streamlit](https://img.shields.io/badge/streamlit-dashboard-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

## Project Overview
This project simulates a **real-world banking system** with Customers, Accounts, Transactions, Loans, and CreditCards.  
It demonstrates **full-stack Data Engineering, Data Science, and Dashboarding skills**, including:

- Building a **relational database** (MySQL)
- Designing **data pipelines** for cleaning and aggregation
- Performing **EDA and visual analytics**
- Building **ML models** for loan prediction, customer segmentation, and fraud detection
- Creating **interactive dashboards** (Streamlit + Plotly)

---

## 📂 Tech Stack
- **Database / ETL:** MySQL, Pandas, SQLAlchemy  
- **Data Analysis / Visualization:** Python, Pandas, Matplotlib, Seaborn  
- **Machine Learning:** Scikit-learn  
- **Synthetic Data Generation:** Faker  
- **Dashboarding:** Streamlit, Plotly

---

## Features

### Data Engineering (DE)
- Relational schema with **Customers, Accounts, Transactions, Loans, CreditCards**
- **ETL pipeline:** MySQL → Pandas → Cleaned CSVs
- Joins and aggregations for **customer profiles & KPIs**

### Data Science (DS)
- **EDA & Visualization**:
  - Customer demographics (age, account opening trends)
  - Account balances & distributions
  - Loan types & status
  - Credit card utilization
  - Transaction trends and types
  - Multi-table KPIs (balance vs loans vs credit usage)

### Machine Learning (ML)
- **Loan Default Prediction** → Predict Approved/Rejected loans
- **Customer Segmentation** → Cluster customers by financial profile
- **Transaction Fraud Detection** → Flag anomalous transactions

---

## Example Insights
- Most customers are **25–45 years old**
- **Top 10 customers** hold disproportionately high balances (VIP segment)
- **Home and Personal Loans** dominate, majority approved
- **15–20% of credit card users** are above 80% utilization → high-risk
- Transactions are mostly **debit**, few failed transactions
- **Customer Segmentation** identifies potential VIP, standard, and high-risk groups

---

## Project Structure
```
banking-project/
├── data/               # Cleaned CSVs ready for analysis
├── raw_data/           # Optional: original CSVs
├── sql/
│   └── banking.sql     # Schema + queries
├── pipeline.ipynb      # ETL / data cleaning
├── analysis.ipynb      # EDA + visualizations
├── ml.ipynb            # ML models: loan prediction, segmentation, fraud
├── dashboard/          # Streamlit / Plotly dashboard (optional)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

---

## Setup Instructions

1. **Clone repository**
```bash
git clone <your_repo_url>
cd banking-project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Create MySQL database**
```sql
source sql/banking.sql;
```

4. **Run ETL pipeline**
```bash
jupyter notebook pipeline.ipynb
```

5. **Run analysis**
```bash
jupyter notebook analysis.ipynb
```

6. **Run ML models**
```bash
jupyter notebook ml.ipynb
```

7. **Optional:** Launch dashboard
```bash
streamlit run dashboard/app.py
```

---

## 📊 Visualizations

### Account Openings Distribution
![Account openings](images/account_openings_per_year.png)

### Loan Distribution
![Loan distribution](images/loan_distribution_by_type.png)

### Transaction Type
![Transaction type](images/transaction_type_piechart.png)

### Fraud Detection Distribution
![Fraud detection](images/fraud_distribution.png)

---

## Business Value
- Helps **bank managers identify VIP clients**
- Flags **high-risk credit card users**
- Automates **loan approval insights**
- Detects **fraudulent transactions** early
- Demonstrates **full DE + DS + ML workflow** on real-w