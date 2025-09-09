import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
filepath = "expenses.csv"
balancefile = "balance.csv"
loans_and_debts = "loans_and_debts.csv"

# --- Load & Save Functions ---
def load_data():
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])

def save_data(df):
    df.to_csv(filepath, index=False)

def load_balance():
    if os.path.exists(balancefile):
        return pd.read_csv(balancefile).iloc[0,0]
    else:
        return 10000

def save_balance(balance):
    pd.DataFrame([{"Balance": balance}]).to_csv(balancefile, index=False)

def calculate_expenses(csv_file):
    if "Transaction" in csv_file.columns and "Amount" in csv_file.columns:
        return csv_file[csv_file["Transaction"] == "Expenditure"]["Amount"].sum()

def load_loans():
    if os.path.exists(loans_and_debts):
        return pd.read_csv(loans_and_debts)
    else:
        return pd.DataFrame(columns=["Date","Transaction","To","Description","Amount","Status"])

def save_loans(df):
    df.to_csv(loans_and_debts, index=False)

def add_expense(expenses,date,category,description,amount,balance):
    if not isinstance(date, str):
        date_str = date.strftime("%Y-%m-%d")
    else:
        date_str = date
    balance -= amount
    
    new_expense = pd.DataFrame([[date_str,"Expenditure",category,description,amount,balance]],
                                       columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
    expenses = pd.concat([expenses,new_expense], ignore_index=True)
    save_balance(balance)
    save_data(expenses)
    return expenses,balance
def add_income(expenses,category,date,description,amount,balance):
    if not isinstance(date, str):
        date_str = date.strftime("%Y-%m-%d")
    else:
        date_str = date
    balance += amount
    new_income = pd.DataFrame([[date_str,"Income",category,description,amount,balance]],
                                      columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])
    expenses = pd.concat([expenses,new_income], ignore_index=True)
    save_data(expenses)
    save_balance(balance)

def net_expenditure(csv_file):
    expenditure=csv_file[csv_file["Transaction"] == "Expenditure"]["Amount"].sum()
    income=csv_file[csv_file["Transaction"]=="Income"]["Amount"].sum()
    return income-expenditure


# --- Load Data ---
expenses = load_data()
balance = load_balance()
loans = load_loans()

# --- Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.header("Menu")
if st.sidebar.button("Home"): st.session_state.page = "Home"
if st.sidebar.button("Add Transactions"): st.session_state.page = "Add Transactions"
if st.sidebar.button("View Transactions"): st.session_state.page = "View Transactions"
if st.sidebar.button("Analytics and Report"): st.session_state.page = "Analytics"
if st.sidebar.button("Loans and Debts"): st.session_state.page = "Loans and Debts"
if st.sidebar.button("Settings"): st.session_state.page = "Settings"

# --- Home Page ---
if st.session_state.page == "Home":
    if not os.path.exists(balancefile):
        initial_balance = st.number_input("Enter your bank balance:", value=10000)
        if st.button("Save Balance"):
            save_balance(initial_balance)
            st.rerun()

    st.title("Dashboard")
    recent = load_data()
    total_expense = calculate_expenses(recent)
    col1, col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"<h4>Current Balance: ₹{balance}</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4>Total Expenditure: ₹{total_expense}</h4>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h4>Net Savings: ₹{net_expenditure(recent)}</h4>", unsafe_allow_html=True)


    st.subheader("Recent Transactions")
    st.table(recent.tail(5))

# --- Add Transactions ---
elif st.session_state.page == "Add Transactions":
    st.title("Add Transaction")

    # --- Add Expense ---
    st.markdown("<h2>Add Expense</h2>", unsafe_allow_html=True)
    expense_date = st.date_input("Date", key="expense_date")
    expense_category = st.selectbox("Category", 
                                    ["Select...", "Food and Lifestyle","Rent","Groceries",
                                     "Internet and Mobile Bills","Transportation","Health and Wellness",
                                     "Entertainment","Miscellaneous"])
    expense_description = st.text_input("Description (Optional)", key="expense_description")
    expense_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="expense_amount")

    if st.button("Add Expense"):
        if expense_date and expense_category != "Select..." and expense_amount > 0:
            add_expense(expenses,expense_date,expense_category,expense_description,expense_amount,balance)
            st.success("Expense added!")
        else:
            st.error("⚠ Please fill in Date, Category, and Amount to add an expense.")

    # --- Add Income ---
    st.markdown("<h2>Add Income</h2>", unsafe_allow_html=True)
    income_date = st.date_input("Date", key="income_date")
    income_description = st.text_input("Description (Optional)", key="income_description")
    income_amount = st.number_input("Amount", min_value=0.0, format="%.2f", key="income_amount")

    if st.button("Add Income"):
        if income_date and income_amount > 0:
            add_income(expenses,"",income_date,income_description,income_amount,balance)
            st.success("Income Added!")
        else:
            st.error("⚠ Please fill in Date and Amount to add income.")

elif st.session_state.page == "View Transactions":
    st.title("View Transactions")
    
    view = load_data()
    col1, col2,col3 = st.columns(3)
    total_expense = calculate_expenses(view)
    col1, col2,col3 = st.columns(3)
    with col1:
        st.markdown(f"<h4>Current Balance: ₹{balance}</h4>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<h4>Total Expenditure: ₹{total_expense}</h4>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<h4>Net Savings: ₹{net_expenditure(view)}</h4>", unsafe_allow_html=True)
    st.subheader("Filter")
    view["Date"] = pd.to_datetime(view["Date"])

    if not view.empty and view["Date"].notna().any():
        min_date = view["Date"].min().date()
        max_date = view["Date"].max().date()
    else:
    # Fallback to today's date if no valid data
        import datetime
        min_date = datetime.date.today()
        max_date = datetime.date.today()

    col1, col2 = st.columns(2)
    with col1:
        from_date = st.date_input("From", min_date)
    with col2:
        to_date = st.date_input("To", max_date)


    categories = st.multiselect("Select Category", view["Category"].unique())
    transaction_type = st.multiselect("Transaction Type", view["Transaction"].unique())

    # Filter by date
    filtered = view[
        (view["Date"].dt.date >= from_date) &
        (view["Date"].dt.date <= to_date)
    ]

    # Filter by category
    if categories:
        filtered = filtered[filtered["Category"].isin(categories)]

    # Filter by transaction type
    if transaction_type:
        filtered = filtered[filtered["Transaction"].isin(transaction_type)]

    if st.button("Show"):
        st.dataframe(filtered)
        st.markdown(f"Total expense: {calculate_expenses(filtered)}")

    # Filter by Month
    st.subheader("Filter by Month")
    month = st.selectbox(
        "Select Month",
        ["January", "February", "March", "April", "May", "June",
         "July", "August", "September", "October", "November", "December"]
    )

    if st.button(f"Show transactions for {month}"):
        if not view.empty:
            # Ensure Date column is datetime
            view["Date"] = pd.to_datetime(view["Date"])
            # Extract month name from Date
            view["Month"] = view["Date"].dt.month_name()
            # Filter by selected month
            filtered = view[view["Month"] == month]

            if not filtered.empty:
                st.subheader(f"Transactions for {month}")
                st.dataframe(filtered)
                st.markdown(f"Total expense for {month}: {calculate_expenses(filtered)}")
            else:
                st.warning(f"No transactions found for {month}.")
        else:
            st.info("No transactions recorded yet.")

    # Show all transactions
    st.subheader("Show all Transactions")
    if st.button("Show All Transactions"):
        st.dataframe(view)
        st.markdown(f"Total expenses: {calculate_expenses(view)}")


# --- Loans and Debts ---
elif st.session_state.page == "Loans and Debts":
    st.header("Loans and Debts")

    # --- Initialize loans in session state ---
    if "loans" not in st.session_state:
        st.session_state.loans = loans.copy()

    # Ensure "Select" column exists
    if "Select" not in st.session_state.loans.columns:
        st.session_state.loans["Select"] = False  

    # --- Loans Given ---
    st.subheader("Loans Given")
    loan_date = st.date_input("Date", key="loan_date")
    given_to = st.text_input("Loan Given To")
    loan_amount = st.number_input("Loan Amount", min_value=0.0, format="%.2f", key="loan_amount")
    loan_description = st.text_input("Description (Optional)", key="loan_desc")
    if loan_description.strip() == "":
        loan_description = f"Loan given to {given_to}"

    if st.button("Register Loan", key="loan_register"):
        if loan_date and given_to.strip() != "" and loan_amount > 0:
            loan_date_str = loan_date.strftime("%Y-%m-%d")
            new_loan = pd.DataFrame(
                [[loan_date_str, "Loan", given_to, loan_description, loan_amount, "Unpaid", False]],
                columns=["Date", "Transaction", "To", "Description", "Amount", "Status", "Select"]
            )
            st.session_state.loans = pd.concat([st.session_state.loans, new_loan], ignore_index=True)
            save_loans(st.session_state.loans)
            st.success("Loan registered successfully!")
        else:
            st.error("⚠ Please enter Date, Loan Given To and Amount.")

    # --- Debts ---
    st.subheader("Debts")
    debt_date = st.date_input("Date", key="debt_date")
    indebted_to = st.text_input("Indebted To")
    debt_amount = st.number_input("Debt Amount", min_value=0.0, format="%.2f", key="debt_amount")
    debt_description = st.text_input("Description (Optional)", key="debt_desc")
    if debt_description.strip() == "":
        debt_description = f"Indebted to {indebted_to}"

    if st.button("Register Debt", key="debt_register"):
        if debt_date and indebted_to.strip() != "" and debt_amount > 0:
            debt_date_str = debt_date.strftime("%Y-%m-%d")
            new_debt = pd.DataFrame(
                [[debt_date_str, "Debt", indebted_to, debt_description, debt_amount, "Unpaid", False]],
                columns=["Date", "Transaction", "To", "Description", "Amount", "Status", "Select"]
            )
            st.session_state.loans = pd.concat([st.session_state.loans, new_debt], ignore_index=True)
            save_loans(st.session_state.loans)
            st.success("Debt registered successfully!")
        else:
            st.error("⚠ Please enter Date, Indebted To and Amount.")

    # --- Settle Up Section ---
    if not st.session_state.loans.empty:
        st.header("Settle Up Loans and Debts")

        # Editable DataFrame with checkboxes
        edited_df = st.data_editor(
            st.session_state.loans,
            use_container_width=True,
            num_rows="fixed",
            column_config={
                "Select": st.column_config.CheckboxColumn("Select Row")
            },
            disabled=["Transaction", "Amount", "Status"]  # prevent editing other columns
        )
        selected_rows = edited_df[edited_df["Select"]]

        # Button to update status of selected rows
        if st.button("Settle Up"):
            if not selected_rows.empty:
                for idx, row in st.session_state.loans.loc[selected_rows.index].iterrows():
                    if row["Status"] == "Settled":
                        st.warning(f'{row["Transaction"]} already settled')
                    elif row["Transaction"] == "Debt" and row["Status"] != "Settled":
                        st.session_state.loans.at[idx, "Status"] = "Settled"
                        expenses,balance=add_expense(
                            expenses, row["Date"], "Debt",
                            f"settled debt with {row['To']}", row["Amount"], balance
                        )

                        st.success("Expense added!")
                        
                    elif row["Transaction"] == "Loan" and row["Status"] != "Settled":
                        st.session_state.loans.at[idx, "Status"] = "Settled"
                        add_income(
                            expenses, "Loan", row["Date"],
                            f"Loan paid by {row['To']}", row["Amount"], balance
                        )
                        st.success("Income Added!")
                        

                save_loans(st.session_state.loans)
                st.success("✅ Selected loans/debts settled!")

            else:
                st.warning("No rows selected.")