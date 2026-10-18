
"""
Program: Encapsulated Banking System with Inheritance Models
Author: Saurav 241492

Description:
Implements a banking system using OOP principles.
Includes a base BankAccount class and derived SavingsAccount
and CurrentAccount classes with transaction method overriding.

Input: Account details, deposit amounts, and withdrawal amounts.
Output: Transaction results and updated account balances.
"""

class BankAccount:
    def __init__(self, account_holder, balance=0):
        self.account_holder = account_holder
        self.__balance = balance  # Private attribute

    def deposit(self, amount):
        if amount <= 0:
            print("Deposit amount must be positive.")
            return

        self.__balance += amount
        print(f"Deposited: Rs. {amount:.2f}")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False

        if amount > self.__balance:
            print("Insufficient balance.")
            return False

        self.__balance -= amount
        print(f"Withdrawn: Rs. {amount:.2f}")
        return True

    def get_balance(self):
        return self.__balance

    def display_details(self):
        print(f"Account Holder: {self.account_holder}")
        print(f"Balance: Rs. {self.get_balance():.2f}")


class SavingsAccount(BankAccount):
    def __init__(self, account_holder, balance=0, interest_rate=4):
        super().__init__(account_holder, balance)
        self.interest_rate = interest_rate

    # Method overriding
    def withdraw(self, amount):
        print("Savings Account Withdrawal:")
        return super().withdraw(amount)

    def add_interest(self):
        interest = self.get_balance() * self.interest_rate / 100
        super().deposit(interest)
        print(f"Interest added: Rs. {interest:.2f}")


class CurrentAccount(BankAccount):
    def __init__(self, account_holder, balance=0, overdraft_limit=5000):
        super().__init__(account_holder, balance)
        self.overdraft_limit = overdraft_limit

    # Method overriding
    def withdraw(self, amount):
        print("Current Account Withdrawal:")

        if amount <= 0:
            print("Withdrawal amount must be positive.")
            return False

        if amount > self.get_balance() + self.overdraft_limit:
            print("Overdraft limit exceeded.")
            return False

        if amount > self.get_balance():
            overdraft_used = amount - self.get_balance()
            # Withdraw the available balance first.
            super().withdraw(self.get_balance())
            # Represent the remaining overdraft as a negative balance.
            # This account model allows the balance to become negative.
            self._BankAccount__balance = -overdraft_used
            print(f"Overdraft used: Rs. {overdraft_used:.2f}")
            return True

        return super().withdraw(amount)


def show_account(account):
    """Polymorphic interface: works with either account type."""
    account.display_details()


# Main program
if __name__ == "__main__":
    savings = SavingsAccount("Rahul", 10000, 4)
    current = CurrentAccount("Amit", 3000, 5000)

    print("===== SAVINGS ACCOUNT =====")
    show_account(savings)
    savings.deposit(2000)
    savings.withdraw(1500)
    savings.add_interest()
    show_account(savings)

    print("\n===== CURRENT ACCOUNT =====")
    show_account(current)
    current.deposit(1000)
    current.withdraw(6000)
    show_account(current)
