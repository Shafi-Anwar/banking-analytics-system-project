import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
st.set_page_config(page_title="Banking Analytics Dashboard", layout="wide")

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
customer_profiles_path = BASE_DIR.parent / "data" / "customer_profiles.csv"
transactions_path = BASE_DIR.parent / "data" / "clean_transactions.csv"
loans_path = BASE_DIR.parent / "data" / "clean_loans.csv"
credit_cards_path = BASE_DIR.parent / "data" / "clean_credit_cards.csv"

customer_profiles = pd.read_csv(customer_profiles_path)
transactions = pd.read_csv(transactions_path)
loans = pd.read_csv(loans_path)
credit_cards = pd.read_csv(credit_cards_path)

credit_cards['usage_percent'] = (credit_cards['balance'] / credit_cards['credit_limit']) * 100

st.title("Banking Analytics & ML Dashboard")
st.markdown("Interactive dashboard combining customer insights, financial metrics, and ML predictions")

st.sidebar.header("Filters")
customer_id = st.sidebar.selectbox("Select Customer ID", customer_profiles['customer_id'].unique())

cust_profile = customer_profiles[customer_profiles['customer_id'] == customer_id]
cust_loans = loans[loans['customer_id'] == customer_id]
cust_cc = credit_cards[credit_cards['customer_id'] == customer_id]
cust_accounts = cust_profile[['total_balance', 'total_loans', 'credit_card_balance']]

# -----------------------
st.header("Customer Profile Overview")
st.write(cust_profile.T)


st.subheader("Total Balance Distribution")
fig_balance = px.histogram(customer_profiles, x="total_balance", nbins=50,
                           title="Distribution of Total Customer Balances")
st.plotly_chart(fig_balance)

st.subheader("Loan Amounts")
fig_loans = px.histogram(cust_loans, x="amount", color="loan_type", barmode="overlay",
                         title=f"Loans for Customer {customer_id}")
st.plotly_chart(fig_loans)

st.subheader("Credit Card Utilization")
fig_cc = px.bar(cust_cc, x='card_type', y='usage_percent', color='usage_percent',
                title=f"Credit Card Utilization (%) for Customer {customer_id}")
st.plotly_chart(fig_cc)

st.subheader("Transactions Over Time")
cust_txn = transactions[transactions['account_id'].isin(cust_profile['customer_id'])]
cust_txn['timestamp'] = pd.to_datetime(cust_txn['timestamp'])
txn_time = cust_txn.groupby(cust_txn['timestamp'].dt.date)['amount'].sum().reset_index()
fig_txn = px.line(txn_time, x='timestamp', y='amount', title=f"Transactions Over Time for Customer {customer_id}")
st.plotly_chart(fig_txn)


st.subheader("Customer Segmentation")
X_cluster = customer_profiles[['total_balance','total_loans','credit_card_balance']].fillna(0)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_cluster)
kmeans = KMeans(n_clusters=4, random_state=42)
customer_profiles['segment'] = kmeans.fit_predict(X_scaled)

fig_segment = px.scatter(customer_profiles, x='total_balance', y='total_loans', 
                         color='segment', hover_data=['customer_id'],
                         title="Customer Segmentation (All Customers)")
st.plotly_chart(fig_segment)

# Highlight selected customer's segment
cust_seg = customer_profiles[customer_profiles['customer_id'] == customer_id]['segment'].values[0]
st.info(f"Customer {customer_id} belongs to Segment {cust_seg}")


st.subheader("Loan Risk Prediction (Approved / Rejected)")
loan_model = RandomForestClassifier(n_estimators=100, random_state=42)
loan_df = loans[loans['status'].isin(['Approved','Rejected'])].copy()
loan_df['status_enc'] = loan_df['status'].map({'Approved':0,'Rejected':1})
X_train = loan_df[['amount','interest_rate']]
y_train = loan_df['status_enc']
loan_model.fit(X_train, y_train)

if not cust_loans.empty:
    X_cust = cust_loans[['amount','interest_rate']]
    cust_loans['predicted_risk'] = loan_model.predict(X_cust)
    cust_loans['predicted_status'] = cust_loans['predicted_risk'].map({0:'Approved',1:'Rejected'})
    st.dataframe(cust_loans[['loan_type','amount','interest_rate','status','predicted_status']])
else:
    st.write("No loans for this customer.")

st.subheader("Credit Card Usage Alert")
high_usage = cust_cc[cust_cc['usage_percent'] > 80]
if not high_usage.empty:
    st.warning(f"Customer {customer_id} has high credit card utilization!")
    st.dataframe(high_usage[['card_type','balance','credit_limit','usage_percent']])
else:
    st.success("Credit card usage is within safe limits.")

st.subheader("Download Customer Report")

report_sections = []


cust_profile_report = cust_profile.copy()
cust_profile_report['section'] = 'Profile'
report_sections.append(cust_profile_report)

if not cust_loans.empty:
    cust_loans_report = cust_loans.copy()
    cust_loans_report['section'] = 'Loans'
    report_sections.append(cust_loans_report)

if not cust_cc.empty:
    cust_cc_report = cust_cc.copy()
    cust_cc_report['section'] = 'Credit Cards'
    report_sections.append(cust_cc_report)

# Combine all sections
report_df = pd.concat(report_sections, ignore_index=True)
csv = report_df.to_csv(index=False).encode('utf-8')

st.download_button(
    label="Download Customer Report as CSV",
    data=csv,
    file_name=f'customer_{customer_id}_report.csv',
    mime='text/csv'
)