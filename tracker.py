import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Personal Expense Tracker" , layout="wide")
filepath="expenses.csv"
balancefile="balance.csv"
def load_data():
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
def save_data(df):
    df.to_csv(filepath,index=False)

def load_balance():
    if  os.path.exists(balancefile):
        return pd.read_csv(balancefile).iloc[0,0]
    else:
        return 10000
def save_balance(balance):
    pd.DataFrame([{"Balance":balance}]).to_csv(balancefile,index=False)

def calculate_expenses(csv_file):
    sum=0
    for i in range(len(csv_file["Amount"])):
        sum+=csv_file["Amount"][i]
    return sum




expenses=load_data()
balance=load_balance()



if "page" not in st.session_state:
    st.session_state.page = "Home"
st.sidebar.header("Menu") 
# Navigation buttons
if st.sidebar.button("Home"):
    st.session_state.page = "Home"
if st.sidebar.button("Add Transactions"):
    st.session_state.page = "Add Transactions"
if st.sidebar.button("View Transactions"):
    st.session_state.page="View Transactions"
if st.sidebar.button("Analytics and Report"):
    st.session_state.page="Analytics"
if st.sidebar.button("Loans and Debts"):
    st.session_state.page="Loans and Debts"
if st.sidebar.button("Settings"):
    st.session_state.page="Settings"

# Display pages
if st.session_state.page == "Home":
    if not os.path.exists(balancefile):
        initial_balance = st.number_input("Enter your bank balance:", value=10000)
        if st.button("Save Balance"):
            save_balance(initial_balance)
            st.rerun()
    st.title("Dashboard")
    recent=load_data()
    total_expense=calculate_expenses(recent)
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<h4>Current Balance: ₹{balance}</h4>",unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4>Total Expenditure: ₹{total_expense}</h4>",unsafe_allow_html=True)
   

    st.subheader("Recent Transactions")
    
    st.table(recent.tail(5))
    

elif st.session_state.page == "Add Transactions":
    st.title("Add Transaction")
    st.markdown("<h2>Add Expense</h2>",unsafe_allow_html=True)
    expense_date=st.date_input("Date" ,key="expense_date")
    expense_category=st.selectbox("Category",["Food and Lifestyle","Rent","Groceries","Internet and Mobile Bills","Transportation","Health and Wellness","Entertainment","Miscellaneous"])
    expense_description=st.text_input("Description", key="expense_description")
    expense_amount=st.number_input("Amount",min_value=0.0,format="%.2f", key="expense_amount")
    if st.button("Add Expense"):
        balance-=expense_amount
        date_str = expense_date.strftime("%Y-%m-%d")
        new_expense=pd.DataFrame([[date_str,"Expenditure",expense_category,expense_description,expense_amount,balance]],columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
        expenses=pd.concat([expenses,new_expense],ignore_index=True)
        save_balance(balance)
        save_data(expenses)
        st.success("Expense added!")



    st.markdown("<h2>Add Income</h2>",unsafe_allow_html=True)
    income_date=st.date_input("Date" ,key="income_date")
    income_description=st.text_input("Description", key="income_description")
    income_amount=st.number_input("Amount",min_value=0.0,format="%.2f",key="income_amount")
    if st.button("Add Income"):
        balance+=income_amount
        date_str = income_date.strftime("%Y-%m-%d")
        new_income=pd.DataFrame([[date_str,"Income",income_description,income_amount,balance]],columns=["Date","Transaction","Description","Amount","Bank Balance"])
        expenses=pd.concat([expenses,new_income],ignore_index=True)
        save_data(expenses)
        save_balance(balance)
        st.success("Income added!")

elif st.session_state.page=="View Transactions":
    st.title("View Transactions")
    col1, col2 = st.columns(2)
    view=load_data()

    with col1:
        from_date = st.date_input("From")

    with col2:
        to_date = st.date_input("To")

    if st.button("Show All Transactions"):
        st.dataframe(view)



        





