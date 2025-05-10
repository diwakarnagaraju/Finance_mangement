
import pandas as pd
from datetime import datetime
import csv
from data_entry import get_date, get_amount, get_category, get_description
import matplotlib.pyplot as plt

class financecsv:
    csv_file = "finance_data.csv"
    COLUMNS = ["date", "amount", "category", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initialize_csv(self):
        try:
            pd.read_csv(self.csv_file)
        except FileNotFoundError:
            df  = pd.DataFrame(columns=self.COLUMNS)
            df.to_csv(self.csv_file, index = False)
    
    @classmethod
    def add_entry(self, date, amount, category, description):
        new_entry = {
            "date" : date,
            "amount" : amount,
            "category" : category,
            "description" : description,
        }
        with open (self.csv_file, 'a', newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames =self.COLUMNS)
            writer.writerow(new_entry)
        print("new entry added successfully")
    
    @classmethod
    def transaction_range(self, start_date, end_date):
        df = pd.read_csv(self.csv_file)
        df["date"] = pd.to_datetime(df["date"], format=financecsv.FORMAT)
        start_date = datetime.strptime(start_date, financecsv.FORMAT)
        end_date = datetime.strptime(end_date, financecsv.FORMAT)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transaction found on this date.")
        else:
            print(f"Transaction from {start_date.strftime(financecsv.FORMAT)} to {end_date.strftime(financecsv.FORMAT)}")
            print(filtered_df.to_string(
                index = False, formatters ={"date": lambda x:x.strftime(financecsv.FORMAT)}))

            total_income = filtered_df[filtered_df["category"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["category"] == "Expense"]["amount"].sum()
            print("\nSummary: ")
            print(f"Total Income: {total_income:.2f}")
            print(f"Total Expenses: {total_expense:.2f}")
            print(f"Net Saving: {(total_income - total_expense):.2f}")
        return filtered_df


def add():
    financecsv.initialize_csv()
    date = get_date("Enter the date of the transaction (dd-mm-yyyy) or enter for today's date: ", allow_default=True)
    amount = get_amount()
    category = get_category()
    description = get_description()
    financecsv.add_entry(date, amount, category, description)

def plot_transaction(df):
    df.set_index("date", inplace = True)

    income_df = (df[df["category"] == "Income"].resample("D").sum().reindex(df.index, fill_value = 0))
    expense_df = (df[df["category"] == "Expense"].resample("D").sum().reindex(df.index, fill_value = 0))

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label = "Income", color = "g")
    plt.plot(expense_df.index, expense_df["amount"], label = "Expense", color = "r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income & Expenses over Time.")
    plt.legend()
    plt.grid(True)
    plt.show()

def main():
    while True:
        print("\n1. Add new Trasanction.")
        print("2.View Transaction and summary within a date range.")
        print("3. Exit")
        choice = input("Enter the Your Choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            star_date = get_date("Enter the start date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end date (dd-mm-yyyy): ")
            df = financecsv.transaction_range(star_date, end_date)
            if input("Do you wnat to see a plot? ").lower() == "y":
                plot_transaction(df)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid Choice please enter either 1 or 2 or 3!")

if __name__ == "__main__":
    main()
