class BankAccount:
    def __init__(self, account_holder, account_type, balance=0):
        self.account_holder = account_holder
        self.account_type = account_type
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"Deposited {amount}. New balance: {self.balance}")
        else:
            print("Deposit amount must be greater than zero.")

    def withdraw(self, amount):
        if amount > 0 and amount <= self.balance:
            self.balance -= amount
            print(f"Withdrew {amount}. New balance: {self.balance}")
        elif amount <= 0:
            print("Withdrawal amount must be greater than zero.")
        else:
            print("Insufficient balance!")

    def transfer(self, amount, target_account):
        if isinstance(target_account, BankAccount):
            if amount <= self.balance:
                self.balance -= amount
                target_account.balance += amount
                print(f"Transferred {amount} to {target_account.account_holder}. Your new balance: {self.balance}")
            else:
                print("Insufficient balance to transfer.")
        else:
            print("Target account is not valid.")

    def compare_balance(self, other_account):
        if isinstance(other_account, BankAccount):
            if self.balance > other_account.balance:
                return "larger"
            elif self.balance < other_account.balance:
                return "smaller"
            else:
                return "equal"
        else:
            print("Comparison account is not valid.")

    def display_account_details(self):
        print(f"Account Holder: {self.account_holder}")
        print(f"Account Type: {self.account_type}")
        print(f"Balance: {self.balance}")

# Sample CLI Application
def banking_app():
    accounts = []
    while True:
        print("\n--- Banking System ---")
        print("1. Create Account")
        print("2. View Account Details")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Transfer Money")
        print("6. Compare Accounts")
        print("7. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == '1':
            holder = input("Enter Account Holder Name: ")
            acc_type = input("Enter Account Type (e.g., Savings, Checking): ")
            account = BankAccount(holder, acc_type)
            accounts.append(account)
            print(f"Account created for {holder} with balance {account.balance}")
        
        elif choice == '2':
            if not accounts:
                print("No accounts available.")
            else:
                for i, account in enumerate(accounts):
                    print(f"\nAccount {i + 1}")
                    account.display_account_details()
        
        elif choice == '3':
            if not accounts:
                print("No accounts available.")
            else:
                account_index = int(input("Enter account index (1 to N): ")) - 1
                if 0 <= account_index < len(accounts):
                    amount = float(input("Enter amount to deposit: "))
                    accounts[account_index].deposit(amount)
                else:
                    print("Invalid account index.")
        
        elif choice == '4':
            if not accounts:
                print("No accounts available.")
            else:
                account_index = int(input("Enter account index (1 to N): ")) - 1
                if 0 <= account_index < len(accounts):
                    amount = float(input("Enter amount to withdraw: "))
                    accounts[account_index].withdraw(amount)
                else:
                    print("Invalid account index.")
        
        elif choice == '5':
            if len(accounts) < 2:
                print("At least two accounts are required for a transfer.")
            else:
                account_index_from = int(input("Enter the index of the source account (1 to N): ")) - 1
                account_index_to = int(input("Enter the index of the target account (1 to N): ")) - 1
                if (0 <= account_index_from < len(accounts)) and (0 <= account_index_to < len(accounts)):
                    amount = float(input("Enter amount to transfer: "))
                    accounts[account_index_from].transfer(amount, accounts[account_index_to])
                else:
                    print("Invalid account indexes.")
        
        elif choice == '6':
            if len(accounts) < 2:
                print("At least two accounts are required for comparison.")
            else:
                account_index_1 = int(input("Enter the index of the first account (1 to N): ")) - 1
                account_index_2 = int(input("Enter the index of the second account (1 to N): ")) - 1
                if (0 <= account_index_1 < len(accounts)) and (0 <= account_index_2 < len(accounts)):
                    comparison_result = accounts[account_index_1].compare_balance(accounts[account_index_2])
                    print(f"The first account is {comparison_result} than the second account.")
                else:
                    print("Invalid account indexes.")
        
        elif choice == '7':
            print("Exiting the Banking System.")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    banking_app()
