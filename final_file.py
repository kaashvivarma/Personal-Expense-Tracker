import streamlit as st
import pandas as pd
import os
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Personal Expense Tracker", layout="wide")
filepath = "expenses.csv"
balancefile = "balance.csv"
loans_and_debts = "loans_and_debts.csv"
autopay_file="autopay.csv"


# --- Load & Save Functions ---

#Load main expenses csv file
def load_data():
    if os.path.exists(filepath):
        return pd.read_csv(filepath)
    else:
        return pd.DataFrame(columns=["Date","Transaction","Category","Description","Amount","Bank Balance"])

#save changes to the expenses csv file
def save_data(df):
    df.to_csv(filepath, index=False)

#Load and Save the current balance
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

#Load and save current loans and debts
def load_loans():
    if os.path.exists(loans_and_debts):
        return pd.read_csv(loans_and_debts)
    else:
        return pd.DataFrame(columns=["Date","Transaction","To","Description","Amount","Status"])

def save_loans(df):
    df.to_csv(loans_and_debts, index=False)

#function to add expenses
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

#function to add income
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

#Load and save current working autopay
def load_autopay():
    if os.path.exists(autopay_file):
        return pd.read_csv(autopay_file)
    else:
        return pd.DataFrame(columns=["Start Date","Transaction","Category","Description","Amount","Frequency","Next Due"])
def save_autopay(df):
    df.to_csv(autopay_file,index=False)


# --- Load Data ---
expenses = load_data()
balance = load_balance()
loans = load_loans()
autopay=load_autopay()


# --- Navigation ---
if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.header("Menu")
if st.sidebar.button("Home"): st.session_state.page = "Home"
if st.sidebar.button("Add Transactions"): st.session_state.page = "Add Transactions"
if st.sidebar.button("View Transactions"): st.session_state.page = "View Transactions"
if st.sidebar.button("Analytics and Report"): st.session_state.page = "Analytics and Report"
if st.sidebar.button("Loans and Debts"): st.session_state.page = "Loans and Debts"
if st.sidebar.button("AutoPay"): st.session_state.page = "AutoPay"

# --- Home Page ---
if st.session_state.page == "Home":
    #if no balance has been set, user is asked to input balance
    if not os.path.exists(balancefile):
        initial_balance = st.number_input("Enter your bank balance:", value=10000)
        if st.button("Save Balance"):
            save_balance(initial_balance)
            st.rerun()

    
    st.title("Dashboard")
    recent = load_data()
    loans=load_loans()
    auto=load_autopay()
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
    st.subheader("Recent Loans and Debts")
    st.table(loans.tail(5))
    st.subheader("Working Autopay")
    st.table(auto)

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
    loans=load_loans()
    auto=load_autopay()
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
    st.subheader("All Transactions")
    if st.button("Show All Transactions"):
        st.dataframe(view)
        st.markdown(f"Total expenses: {calculate_expenses(view)}")
    #Show all loans and debts
    st.subheader("All Loans and Debts")
    if st.button("Show All Loans and Debts"):
        st.dataframe(loans)
        if "Transaction" in loans.columns and "Amount" in loans.columns:
            ex= loans[loans["Transaction"] == "Debt"]["Amount"].sum()
        st.markdown(f"Total debt to pay: {ex}")
    #Show all Autopay
    st.subheader("All Working Autopay")
    if st.button("Show All Working Autopay"):
        st.dataframe(autopay)




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

#---AutoPay---
elif st.session_state.page=="AutoPay":
    st.header("Setup Autopay")
    autopay = load_autopay()
    st.dataframe(autopay)

    auto_date = st.date_input("Start Date")
    auto_category = "AutoPay"
    auto_description = st.text_input("AutoPay Description", "AutoPay")
    auto_amount = st.number_input("Amount", min_value=0.0, format="%.2f")
    auto_freq = st.selectbox("Frequency", ["Daily","Weekly","Monthly","Yearly"])

    if st.button("Add AutoPay"):
        if auto_description and auto_amount > 0:
            new_autopay = pd.DataFrame([[
                auto_date.strftime("%Y-%m-%d"), "Expenditure", auto_category, auto_description,
                auto_amount, auto_freq, auto_date.strftime("%Y-%m-%d")
            ]], columns=["Start Date","Transaction","Category","Description","Amount","Frequency","Next Due"])
            
            autopay = pd.concat([autopay, new_autopay], ignore_index=True)
            save_autopay(autopay)
            st.success("AutoPay Registered!")
        else:
            st.error("Please provide a description and amount.")
    
    if not autopay.empty:
    # Add a selection column for deletion
        autopay["Select"] = False  

        edited = st.data_editor(
        autopay,
        use_container_width=True,
        num_rows="fixed",  # prevent adding new rows
        column_config={
            "Select": st.column_config.CheckboxColumn("Select Row"),
            "Frequency": st.column_config.SelectboxColumn(
                "Frequency",
                options=["Daily", "Weekly", "Monthly", "Yearly"],  # allowed values
            ),
        },
        disabled=[col for col in autopay.columns if col not in ["Frequency", "Select"]]
        )

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Save Changes"):
                updated = edited.drop(columns=["Select"])
                save_autopay(updated)
                st.rerun()
                st.success("Changes saved to autopay!")

        with col2:
            if st.button("Delete Selected"):
                updated = edited[edited["Select"] == False].drop(columns=["Select"])
                save_autopay(updated)
                st.rerun()
                st.success("Selected autopay entries deleted!")
    else:
        st.info("No autopay entries found.")

    


# --- Analytics and Reports ---
elif st.session_state.page == "Analytics and Report":
    st.header("Analytics and Reports")
    view = load_data()
    
    if view is None or view.shape[0] == 0:
        st.warning("No transactions available for analytics.")

    else:
        # Convert Date once
        view["Date"] = pd.to_datetime(view["Date"], errors="coerce")

        # --- Total Metrics ---
        total_income = view[view["Transaction"] == "Income"]["Amount"].sum()
        total_expense = view[view["Transaction"] == "Expenditure"]["Amount"].sum()
        net_savings = total_income - total_expense

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Total Income", f"₹{total_income:.2f}")
        metric_col2.metric("Total Expenditure", f"₹{total_expense:.2f}")
        metric_col3.metric("Net Savings", f"₹{net_savings:.2f}")

        # --- Category-wise Expenses Pie Chart ---
        category_expenses = view[view["Transaction"] == "Expenditure"].groupby("Category")["Amount"].sum()
        pie_col, line_col = st.columns(2)
        if not category_expenses.empty and category_expenses.sum() > 0:
            fig1, ax1 = plt.subplots()
            ax1.pie(category_expenses, labels=category_expenses.index, autopct='%1.1f%%', startangle=90)
            ax1.axis("equal")
            ax1.set_title("Category-wise Expenses")
            pie_col.pyplot(fig1)
        else:
            pie_col.warning("No expenditure data for category-wise chart.")

        # --- Monthly Expenses Line Chart ---
        monthly_expenses = (
            view[view["Transaction"] == "Expenditure"]
            .groupby(view["Date"].dt.to_period("M"))["Amount"]
            .sum()
        )

        if not monthly_expenses.empty and monthly_expenses.sum() > 0:
            fig2, ax2 = plt.subplots()
            monthly_expenses.index = monthly_expenses.index.astype(str)  # ✅ Fix: convert PeriodIndex to string
            ax2.plot(monthly_expenses.index, monthly_expenses.values, marker="o")
            ax2.set_title("Monthly Expenses")
            ax2.set_xlabel("Month")
            ax2.set_ylabel("Amount (₹)")
            plt.xticks(rotation=45)
            line_col.pyplot(fig2)
        else:
            line_col.warning("No expenditure data for monthly chart.")

        # --- Income vs Expenditure Over Time ---
        daily = view.groupby(["Date", "Transaction"])["Amount"].sum().unstack(fill_value=0)
        if not daily.empty:
            fig3, ax3 = plt.subplots()
            if "Income" in daily.columns and daily["Income"].sum() > 0:
                ax3.plot(daily.index, daily["Income"], label="Income", color="green", marker="o")
            if "Expenditure" in daily.columns and daily["Expenditure"].sum() > 0:
                ax3.plot(daily.index, daily["Expenditure"], label="Expenditure", color="red", marker="o")
            ax3.set_title("Income vs Expenditure Over Time")
            ax3.set_xlabel("Date")
            ax3.set_ylabel("Amount")
            ax3.legend()
            metric_col1.pyplot(fig3)
        else:
            metric_col1.warning("No daily transaction data for income vs expenditure chart.")

        # --- Monthly Expenses Bar Chart ---
        if not monthly_expenses.empty and monthly_expenses.sum() > 0:
            fig4, ax4 = plt.subplots()
            ax4.bar(monthly_expenses.index.astype(str), monthly_expenses.values, color="red")  # ✅ Fix applied here
            ax4.set_title("Monthly Expenses")
            ax4.set_xlabel("Month")
            ax4.set_ylabel("Total Expenses")
            plt.xticks(rotation=45)
            line_col.pyplot(fig4)
        else:
            line_col.warning("No expenditure data for monthly bar chart.")

        # --- Top 5 Biggest Expenses ---
        top_expenses = view[view["Transaction"] == "Expenditure"].nlargest(5, "Amount")
        if not top_expenses.empty:
            st.subheader("Top 5 Biggest Expenses")
            st.table(top_expenses[["Date","Category","Description","Amount"]])
        else:
            st.warning("No expenditure data to display top expenses.")


#Check if autopay needs to be paid today or if the due date has been exceeded  
today=datetime.date.today()
for idx, row in autopay.iterrows():
    next_due_date = pd.to_datetime(row["Next Due"]).date()
    if next_due_date<=today:
        expenses, balance = add_expense(expenses, today.strftime("%Y-%m-%d"), row["Category"], row["Description"], row["Amount"], balance)

        if row["Frequency"] == "Daily":
            next_due = next_due_date + pd.Timedelta(days=1)
        elif row["Frequency"] == "Weekly":
            next_due = next_due_date + pd.Timedelta(weeks=1)
        elif row["Frequency"] == "Monthly":
            next_due = next_due_date + pd.DateOffset(months=1)
        elif row["Frequency"] == "Yearly":
            next_due = next_due_date + pd.DateOffset(years=1)
        
        autopay.at[idx, "Next Due"] = next_due.strftime("%Y-%m-%d")
    save_autopay(autopay)



