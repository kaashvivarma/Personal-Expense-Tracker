import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Personal Expense Tracker" , layout="wide")
filepath="expenses.csv"
def load_data():
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
def save_data(df):
    df.to_csv(filepath,index=False)

if "bank_balance" not in st.session_state:
    st.session_state.bank_balance = 10000 
expenses=load_data()

if "page" not in st.session_state:
    st.session_state.page = "Home"
st.sidebar.header("Menu") 
# Navigation buttons
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Add Transactions"):
    st.session_state.page = "Add Transactions"
if st.sidebar.button("View Transaction"):
    st.session_state.page="View Transactions"
if st.sidebar.button("Analytics"):
    st.session_state.page="Analytics"
if st.sidebar.button("Report"):
    st.session_state.page="Report"
if st.sidebar.button("Loans and Debts"):
    st.session_state.page="Loans and Debts"
if st.sidebar.button("Settings"):
    st.session_state.page="Settings"

# Display pages
if st.session_state.page == "Home":
    st.title("Dashboard")
    st.markdown(f"<h2>Current Balance: Rs. {st.session_state.bank_balance}</h2>",unsafe_allow_html=True)

elif st.session_state.page == "Add Transactions":
    st.title("Add Transaction")
    st.markdown("<h2>Add Expense</h2>",unsafe_allow_html=True)
    expense_date=st.date_input("Date" ,key="expense_date")
    expense_category=st.selectbox("Category",["Food and Lifestyle","Rent","Groceries","Internet and Mobile Bills","Transportation","Health and Wellness","Entertainment","Miscellaneous"])
    expense_description=st.text_input("Description", key="expense_description")
    expense_amount=st.number_input("Amount",min_value=0.0,format="%.2f", key="expense_amount")
    if st.button("Add Expense"):
        st.session_state.bank_balance-=expense_amount
        date_str = expense_date.strftime("%Y-%m-%d")
        new_expense=pd.DataFrame([[date_str,"Expenditure",expense_category,expense_description,expense_amount,st.session_state.bank_balance]],columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
        expenses=pd.concat([expenses,new_expense],ignore_index=True)
        save_data(expenses)
        st.success("Expense added!")



    st.markdown("<h2>Add Income</h2>",unsafe_allow_html=True)
    income_date=st.date_input("Date" ,key="income_date")
    income_description=st.text_input("Description", key="income_description")
    income_amount=st.number_input("Amount",min_value=0.0,format="%.2f",key="income_amount")
    if st.button("Add Income"):
        st.session_state.bank_balance+=income_amount
        date_str = income_date.strftime("%Y-%m-%d")
        new_income=pd.DataFrame([[date_str,"Income",income_description,income_amount,st.session_state.bank_balance]],columns=["Date","Transaction","Description","Amount","Bank Balance"])
        expenses=pd.concat([expenses,new_income],ignore_index=True)
        save_data(expenses)
        st.success("Income added!")
        





