import tkinter as tk
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import simpledialog, messagebox, ttk
from abc import ABC, abstractmethod
from collections import defaultdict
# -------------------------
# Bank logic 
# -------------------------
class Account(ABC):
    def __init__(self, account_number, customer_id, balance=0.0):
        self._account_number = account_number
        self._customer_id = customer_id
        self._balance = balance
    @property
    def account_number(self):
        return self._account_number
    @property
    def balance(self):
        return self._balance
    @property
    def customer_id(self):
        return self._customer_id
    @abstractmethod
    def deposit(self, amount):
        pass
    @abstractmethod
    def withdraw(self, amount):
        pass

    def display_details(self):
        return f"Account No: {self.account_number}, Balance: ₹{self.balance:.2f}"
class SavingsAccount(Account):
    def __init__(self, account_number, customer_id, balance=0.0, interest_rate=0.01):
        super().__init__(account_number, customer_id, balance)
        self._interest_rate = interest_rate
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    def withdraw(self, amount):
        if 0 < amount <= self._balance:
            self._balance -= amount
            return True
        return False
    def apply_interest(self):
        self._balance += self._balance * self._interest_rate
    def display_details(self):
        return f"{self.account_number} | {self.customer_id} | ₹{self.balance:.2f} | Savings | {self._interest_rate*100:.1f}% interest"
class CheckingAccount(Account):
    def __init__(self, account_number, customer_id, balance=0.0, overdraft_limit=0.0):
        super().__init__(account_number, customer_id, balance)
        self._overdraft_limit = overdraft_limit
    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            return True
        return False
    def withdraw(self, amount):
        if amount > 0 and (self._balance - amount) >= -self._overdraft_limit:
            self._balance -= amount
            return True
        return False
    def display_details(self):
        return f"{self.account_number} | {self.customer_id} | ₹{self.balance:.2f} | Checking | Overdraft ₹{self._overdraft_limit:.2f}"
class Customer:
    def __init__(self, customer_id, name, address):
        self._customer_id = customer_id
        self._name = name
        self._address = address
        self._accounts = []
    def add_account(self, account):
        self._accounts.append(account)
    def remove_account(self, account_number):
        for acc in self._accounts:
            if acc.account_number == account_number:
                self._accounts.remove(acc)
                return True
        return False
    def get_accounts(self):
        return self._accounts
    def display_details(self):
        return f"{self._customer_id} | {self._name} | {self._address} | Accounts: {len(self._accounts)}"
class Bank:
    def __init__(self):
        self.customers = {}
        self.accounts = {}
        self.loans = defaultdict(float) 
    def add_customer(self, customer):
        if customer._customer_id not in self.customers:
            self.customers[customer._customer_id] = customer
            return True
        return False
    def create_account(self, customer_id, account_type, account_number, initial_balance, extra):
        if customer_id not in self.customers or account_number in self.accounts:
            return False
        if account_type == "savings":
            acc = SavingsAccount(account_number, customer_id, initial_balance, extra)
        elif account_type == "checking":
            acc = CheckingAccount(account_number, customer_id, initial_balance, extra)
        else:
            return False
        self.accounts[account_number] = acc
        self.customers[customer_id].add_account(acc)
        return True
    def deposit(self, account_number, amount):
        if account_number in self.accounts:
            return self.accounts[account_number].deposit(amount)
        return False
    def withdraw(self, account_number, amount):
        if account_number in self.accounts:
            return self.accounts[account_number].withdraw(amount)
        return False
    def transfer(self, from_acc, to_acc, amount):
        if from_acc in self.accounts and to_acc in self.accounts:
            if self.accounts[from_acc].withdraw(amount):
                self.accounts[to_acc].deposit(amount)
                return True
        return False
    def remove_account(self, customer_id, account_number):
        if customer_id in self.customers:
            if self.customers[customer_id].remove_account(account_number):
                del self.accounts[account_number]
                return True
        return False
    def apply_interest_all(self):
        for acc in self.accounts.values():
            if isinstance(acc, SavingsAccount):
                acc.apply_interest()
    def get_account_list(self):
        data = []
        for acc in self.accounts.values():
            if isinstance(acc, SavingsAccount):
                data.append((acc.account_number, acc.customer_id, f"₹{acc.balance:.2f}", "Savings", f"{acc._interest_rate*100:.1f}%"))
            elif isinstance(acc, CheckingAccount):
                data.append((acc.account_number, acc.customer_id, f"₹{acc.balance:.2f}", "Checking", f"Overdraft ₹{acc._overdraft_limit:.2f}"))
        return data
    def get_customer_list(self):
        return [cust.display_details() for cust in self.customers.values()]
    def request_loan(self, account_number, amount):
        if account_number in self.accounts and amount > 0:
            self.loans[account_number] += amount
            self.accounts[account_number]._balance += amount
            return True
        return False
    def repay_loan(self, account_number, amount):
        if account_number in self.loans and amount > 0:
            if self.accounts[account_number]._balance >= amount:
                repay_amount = min(self.loans[account_number], amount)
                self.accounts[account_number]._balance -= repay_amount
                self.loans[account_number] -= repay_amount
                if self.loans[account_number] <= 0:
                    del self.loans[account_number]
                return True
        return False
    def get_loan_list(self):
        return [(acc, f"₹{amt:.2f}") for acc, amt in self.loans.items()]
# -------------------------
# GUI App
# -------------------------
class BankingApp:
    def __init__(self, master):
        self.bank = Bank()
        self.master = master
        master.title("🏦 Enhanced Banking System")
        master.geometry("700x500")
        master.configure(bg="#f0f8ff")
        tk.Label(master, text="🏦 Banking Dashboard", font=("Arial", 20, "bold"), fg="darkblue", bg="#f0f8ff").pack(pady=10)
        style = ttk.Style()
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        style.configure("Treeview.Heading", font=("Arial", 12, "bold"))
        button_frame = tk.Frame(master, bg="#f0f8ff")
        button_frame.pack()
        # Buttons
        tk.Button(button_frame, text="Add Customer", width=18, command=self.add_customer, bg="lightblue").grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Create Account", width=18, command=self.create_account, bg="lightgreen").grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Deposit", width=18, command=self.deposit, bg="lightyellow").grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Withdraw", width=18, command=self.withdraw, bg="lightpink").grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Transfer Funds", width=18, command=self.transfer, bg="orange").grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Remove Account", width=18, command=self.remove_account, bg="lightcoral").grid(row=2, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Apply Interest", width=18, command=self.apply_interest, bg="lightgray").grid(row=3, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Show Customers", width=18, command=self.show_customers, bg="#d0e0f0").grid(row=3, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Request Loan", width=18, command=self.request_loan, bg="#ffa07a").grid(row=4, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Repay Loan", width=18, command=self.repay_loan, bg="#98fb98").grid(row=4, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Show Loans", width=18, command=self.show_loans, bg="#e6e6fa").grid(row=5, column=0, columnspan=2, pady=5)
        tk.Button(button_frame, text="Balance Chart", width=18, command=self.show_balance_chart, bg="#c0ffee").grid(row=6, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Account Types", width=18, command=self.show_account_pie, bg="#fddde6").grid(row=6, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Loan Chart", width=18, command=self.show_loan_chart, bg="#fffacd").grid(row=7, column=0, columnspan=2, pady=5)
        tk.Button(button_frame, text="Exit", width=18, command=master.quit, bg="#ff6347").grid(row=9, column=0, columnspan=2, pady=5)
        # Treeview for account display
        columns = ("acc_no", "cust_id", "balance", "type", "extra")
        self.tree = ttk.Treeview(master, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=120)
        self.tree.pack(expand=True, fill="both")
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.tree, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
    def refresh_tree(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.bank.get_account_list():
            self.tree.insert("", "end", values=row)
    def add_customer(self):
        cid = simpledialog.askstring("Add Customer", "Customer ID:")
        name = simpledialog.askstring("Add Customer", "Name:")
        addr = simpledialog.askstring("Add Customer", "Address:")
        if cid and name and addr:
            if self.bank.add_customer(Customer(cid, name, addr)):
                messagebox.showinfo("Success", "Customer added!")
            else:
                messagebox.showerror("Error", "Customer already exists.")
    def create_account(self):
        cid = simpledialog.askstring("Create Account", "Customer ID:")
        acc_num = simpledialog.askstring("Create Account", "Account Number:")
        acc_type = simpledialog.askstring("Create Account", "Account Type (savings/checking):").lower()
        init_bal = simpledialog.askfloat("Create Account", "Initial Balance:")
        if acc_type == "savings":
            extra = simpledialog.askfloat("Savings", "Interest rate (e.g. 0.02):")
        elif acc_type == "checking":
            extra = simpledialog.askfloat("Checking", "Overdraft limit:")
        else:
            messagebox.showerror("Error", "Invalid account type.")
            return
        if self.bank.create_account(cid, acc_type, acc_num, init_bal, extra):
            messagebox.showinfo("Success", "Account created!")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Failed to create account.")
    def deposit(self):
        acc_num = simpledialog.askstring("Deposit", "Account Number:")
        amt = simpledialog.askfloat("Deposit", "Amount:")
        if self.bank.deposit(acc_num, amt):
            messagebox.showinfo("Success", "Deposit successful.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Deposit failed.")
    def withdraw(self):
        acc_num = simpledialog.askstring("Withdraw", "Account Number:")
        amt = simpledialog.askfloat("Withdraw", "Amount:")
        if self.bank.withdraw(acc_num, amt):
            messagebox.showinfo("Success", "Withdrawal successful.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Withdrawal failed.")
    def transfer(self):
        from_acc = simpledialog.askstring("Transfer", "From Account:")
        to_acc = simpledialog.askstring("Transfer", "To Account:")
        amt = simpledialog.askfloat("Transfer", "Amount:")
        if self.bank.transfer(from_acc, to_acc, amt):
            messagebox.showinfo("Success", "Transfer successful.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Transfer failed.")
    def remove_account(self):
        cid = simpledialog.askstring("Remove Account", "Customer ID:")
        acc_num = simpledialog.askstring("Remove Account", "Account Number:")
        if self.bank.remove_account(cid, acc_num):
            messagebox.showinfo("Success", "Account removed.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Remove failed.")
    def apply_interest(self):
        self.bank.apply_interest_all()
        messagebox.showinfo("Done", "Interest applied.")
        self.refresh_tree()
    def show_customers(self):
        customers = self.bank.get_customer_list()
        messagebox.showinfo("Customers", "\n".join(customers))
    def request_loan(self):
        acc_num = simpledialog.askstring("Loan", "Account Number:")
        amt = simpledialog.askfloat("Loan", "Loan Amount:")
        if self.bank.request_loan(acc_num, amt):
            messagebox.showinfo("Success", "Loan approved and added to balance.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Loan request failed.")
    def repay_loan(self):
        acc_num = simpledialog.askstring("Repay Loan", "Account Number:")
        amt = simpledialog.askfloat("Repay Loan", "Amount to Repay:")
        if self.bank.repay_loan(acc_num, amt):
            messagebox.showinfo("Success", "Loan repayment successful.")
            self.refresh_tree()
        else:
            messagebox.showerror("Error", "Loan repayment failed.")
    def show_loans(self):
        loans = self.bank.get_loan_list()
        if loans:
            msg = "\n".join([f"{acc} ➤ {amt}" for acc, amt in loans])
        else:
            msg = "No active loans."
        messagebox.showinfo("Loans", msg)
    def show_balance_chart(self):
        data = []
        for customer in self.bank.customers.values():
            total = sum([acc.balance for acc in customer.get_accounts()])
            data.append((customer._name, total))
        if data:
            df = pd.DataFrame(data, columns=["Customer", "Total Balance"])
            df.plot(kind='bar', x="Customer", y="Total Balance", legend=False, color="skyblue")
            plt.ylabel("₹ Balance")
            plt.title("Total Balance per Customer")
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No customer data to display.")
    def show_account_pie(self):
        types = {"Savings": 0, "Checking": 0}
        for acc in self.bank.accounts.values():
            if isinstance(acc, SavingsAccount):
                types["Savings"] += 1
            elif isinstance(acc, CheckingAccount):
                types["Checking"] += 1
        if sum(types.values()) == 0:
            messagebox.showinfo("No Data", "No accounts to visualize.")
            return
        labels = list(types.keys())
        sizes = list(types.values())
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["#add8e6", "#90ee90"])
        plt.title("Account Type Distribution")
        plt.axis("equal")
        plt.show()
    def show_loan_chart(self):
        loans = self.bank.get_loan_list()
        if not loans:
            messagebox.showinfo("No Loans", "No loan data to display.")
            return
        df = pd.DataFrame(loans, columns=["Account", "Loan"])
        df["Loan"] = df["Loan"].replace('[₹]', '', regex=True).astype(float)
        df.plot(kind='bar', x="Account", y="Loan", legend=False, color="salmon")
        plt.ylabel("₹ Loan Amount")
        plt.title("Loan Distribution by Account")
        plt.tight_layout()
        plt.show()
# Run app
def show_login_window():
    login = tk.Tk()
    login.title("Login")
    login.geometry("300x200")
    login.configure(bg="#f0f0f0")

    tk.Label(login, text="🔐 Admin Login", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

    tk.Label(login, text="Username:", bg="#f0f0f0").pack()
    username_entry = tk.Entry(login)
    username_entry.pack()

    tk.Label(login, text="Password:", bg="#f0f0f0").pack()
    password_entry = tk.Entry(login, show="*")
    password_entry.pack()

    def try_login():
        username = username_entry.get()
        password = password_entry.get()
        if username == "admin" and password == "admin123":
            login.destroy()
            root = tk.Tk()
            app = BankingApp(root)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials!")

    tk.Button(login, text="Login", command=try_login, bg="lightblue").pack(pady=10)

    login.mainloop()

if __name__ == "__main__":
    show_login_window()
   