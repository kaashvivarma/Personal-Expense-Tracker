# 💰 Personal Expense Tracker

A **Streamlit-based web application** designed to help you take full control of your personal finances.  
This tracker makes it easy to record, manage, and analyze your expenses and income with simple interactive features.  

---

## 🚀 Project Description
The **Personal Expense Tracker** allows users to keep track of daily transactions, loans, debts, and recurring payments in one place.  
It also generates **visual reports** (pie charts, bar graphs, and line charts) to help identify spending patterns and trends.  

All data is stored in **CSV files**, ensuring simplicity and portability. While this approach is lightweight and easy to set up, it can become less scalable when handling very large datasets compared to a traditional database system.

---

## ✨ Features
- **Add Transactions**  
  Record both expenses and income with details such as amount, category, and date.

- **View Transactions with Filters**  
  - Category-wise view  
  - Month-wise view  
  - Custom filters for easier tracking  

- **Loan & Debt Management**  
  - Keep track of loans given and debts taken.  
  - Option to settle them with automatic adjustments to the expense file.  

- **Auto-Pay Feature**  
  Set up **recurring payments** (daily, weekly, monthly, yearly).  
  Amounts are automatically deducted at the defined intervals.  

- **Analytics & Reports**  
  Generate **pie charts, bar graphs, and line charts** for:  
  - Spending categories  
  - Monthly trends  
  - Income vs. Expense comparisons  

- **Simple & Interactive UI**  
  Built with **Streamlit**, making it user-friendly and accessible via any browser.  

---
## 📊Data Handling
- Transactions, loans, debts, and auto-pay details are stored in CSV files.
- This keeps the project lightweight and beginner-friendly.
- ⚠️ However, note that using CSVs may introduce limitations in speed and data consistency for very large-scale usage.

## 🛠️ Tech Stack
- **Python**
- **Streamlit for UI**
- **Pandas & Matplotlib for data handling and visualization**
- **CSV for data storage**

## ⚙️ Installation

1. Clone this repository:
    ```bash
   git clone https://github.com/kaashvivarma/Personal-Expense-Tracker.git
   cd Personal-Expense-Tracker
2. Install required dependencies:
    ```bash
    pip install -r requirements.txt
3. Run the Streamlit app:
    ```bash
    streamlit run tracker.py

OR
- **Use this link to access the app directly through Streamlit Cloud**:
    https://budgetly.streamlit.app/