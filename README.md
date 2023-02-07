# Automated Transaction Categorization and Budget Tracker

This program is a budget tracker that categorizes and tracks the user's spending. The user inputs a CSV file with their transaction history, and the program categorizes the transactions into different categories such as rent, groceries, restaurants, etc. The program then outputs a new CSV file with the categorized transactions and inputs the data into a google sheet.

## Prerequisites
- Python 3
- pandas library
- googleapiclient library
- google-oauth2 library

## How to use
1. Input your transaction history as a CSV file in the "data = pd.read_csv('your_csv_file_here.csv')" line.
2. Set the desired date range in the "DATE_RANGE_START" and "DATE_RANGE_END" variables.
3. Run the program, and a new CSV file "new_csv.csv" will be generated with your categorized transactions.

## Notes
The program currently categorizes transactions based on a predetermined list of categories, "CATEGORY_LIST."
If a transaction does not fit into any of the categories, it will be categorized as "misc." by default. Make sure you add you own google sheet id and google api keys.

This is the first Python project I worked on so its kind of rough but it works!
