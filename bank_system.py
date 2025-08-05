"""
AwesomeGIC Bank - Simple Banking System
"""

from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, List
import re

class Transaction:
    """Represent a bank transaction"""
    
    def __init__(self, date: str, account: str, txn_type: str, amount: Decimal, txn_id: str =""):
        self.date = date
        self.account = account
        self.txn_type = txn_type.upper()
        self.amount = amount
        self.txn_id = txn_id
        
    def __str__(self):
        txn_id_display = self.txn_id if self.txn_id else ""
        return f"| {self.date} | {txn_id_display:11} | {self.txn_type:2} | {self.amount:7.2f} |"


class InterestRule:
    """Represent an interest rule"""
    
    def __init__(self, date: str, rule_id: str, rate: Decimal):
        self.date = date
        self.rule_id = rule_id
        self.rate = rate
        
    def __str__(self):
        return f"| {self.date} | {self.rule_id:6} | {self.rate:8.2f} |"


class Account:
    """Rpresent an bank account"""
    def __init__(self, account_id: str):
        self.account_id = account_id
        self.transactions: List[Transaction] = []
        self.balance = Decimal('0')
        
    def add_transaction(self, transaction: Transaction):
        """Add a transaction to the account"""
        if transaction.txn_type == 'W':
            if self.balance < transaction.amount:
                raise ValueError("Insufficient balance for withdrawal")
            self.balance -= transaction.amount
        elif transaction.txn_type in ['D', 'I']:
            self.balance += transaction.amount
        
        self.transactions.append(transaction)
        
    def get_balance_at_date(self, target_date: str) -> Decimal:
        """Get account balance at end of specific date"""
        balance = Decimal('0')
        for transaction in self.transactions:
            if transaction.date <= target_date:
                if transaction.txn_type == 'W':
                    balance -= transaction.amount
                else:
                    balance += transaction.amount
        return balance


class BankingSystem:
    """main banking system class"""
    def __init__(self):
        self.accounts: Dict[str, Account] = {}
        self.interest_rules: List[InterestRule] = []
        self.transaction_counters: Dict[str, int] = {}
    
    def validate_date(self, date_str: str) -> bool:
        """Validate date format YYYYMMDD"""
        if not re.match(r'^\d{8}$', date_str):
            return False
        try:
            datetime.strptime(date_str, '%Y%m%d')
            return True
        except ValueError:
            return False
    
    def validate_amount(self, amount_str: str) -> bool:
        """validate amount format"""
        try:
            amount = Decimal(amount_str)
            if amount <= 0:
                return False
            if amount.as_tuple().exponent < -2:
                return False
            return True
        except:
            return False
    
    def generate_transaction_id(self, date: str) -> str:
        """Generate unique transaction ID"""
        if date not in self.transaction_counters:
            self.transaction_counters[date] = 0
        self.transaction_counters[date] += 1
        return f"{date}-{self.transaction_counters[date]:02d}"

    def input_transaction(self, input_line: str) -> str:
        """Process transaction input"""
        parts = input_line.strip().split()
        if len(parts) != 4:
            return "Invalid format. Expected: <Date> <Account> <Type> <Amount>"
        date, account, txn_type, amount_str = parts
        
        if not self.validate_date(date):
            return "Invalid format. Use YYYYMMDD"
        
        if txn_type.upper() not in ['D','W']:
            return "Invalid transaction type. Use D for depositt or W for withdrawal"
        
        if not self.validate_amount(amount_str):
            return "Invalid amount, Must be positive with max 2 decimal places"    
        
        amount = Decimal(amount_str)
        txn_type = txn_type.upper()

        if account not in self.accounts:
            if txn_type == 'W':
                return "Cannot withdraw from new account with zero balance"
            self.accounts[account] = Account(account)
        
        if txn_type == 'W' and self.accounts[account].balance < amount:
            return "Insufficient balance for withdrawal"
        
        txn_id = self.generate_transaction_id(date)
        transaction = Transaction(date, account, txn_type, amount, txn_id)
        
        self.accounts[account].add_transaction(transaction)
        return self.get_account_statement(account)
    
    def define_interest_rule(self, input_line: str) -> str:
        """Process interest rule input"""
        parts  = input_line.strip().split()
        if len(parts) != 3:
            return "Invalid format. Expected: <Date> <RuleId> <Rate in %>"
        
        date, rule_id, rate_str = parts
        
        if not self.validate_date(date):
            return "Invalid date format. Use YYYYMMDD"
        try:
            rate = Decimal(rate_str)
            if rate <= 0 or rate >= 100:
                return "Interest rate must be between 0 and 100"
        except:
            return "Invalid rate format"
        
        self.interest_rules = [rule for rule in self.interest_rules if rule.date != date]

        new_rule = InterestRule(date, rule_id, rate)
        self.interest_rules.append(new_rule)

        self.interest_rules.sort(key=lambda x: x.date)
        return self.get_interest_rules_display()
    
    def get_account_statement(self, account: str) -> str:
        """Get account statement without interest"""
        if account not in self.accounts:
            return f"Account {account} not found"
        
        acc = self.accounts[account]
        result = [f"Account: {account}"]
        result.append("| Date     | Txn Id      |Type| Amount  |")
        
        for transaction in acc.transactions:
            result.append(str(transaction))

        return "\n".join(result)
    
    def get_interest_rules_display(self) -> str:
        """Get formatted interest rules display"""
        result = ["Interest rules:"]
        result.append("| Date     | RuleId | Rate (%) |")
        
        for rule in self.interest_rules:
            result.append(str(rule))

        return "\n".join(result)
    
    def calculate_interest(self, account: str, year_month: str) -> Decimal:
        """Calculate interest for an account for a specific month"""
        if account not in self.accounts:
            return Decimal('0')
        
        year = int(year_month[:4])
        month = int(year_month[4:])

        first_day = datetime(year, month, 1)
        if month == 12:
            last_day = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = datetime(year, month + 1, 1) - timedelta(days=1)

        total_interest = Decimal('0')
        current_date = first_day
        
        while current_date <= last_day:
            date_str = current_date.strftime('%Y%m%d')

            eod_balance = self.accounts[account].get_balance_at_date(date_str)
            
            if eod_balance > 0:
                applicable_rate = Decimal('0')
                for rule in self.interest_rules:
                    if rule.date <= date_str:
                        applicable_rate = rule.rate
                        
                if applicable_rate > 0:
                    daily_interest = eod_balance * applicable_rate / Decimal('100') / Decimal('365')
                    total_interest += daily_interest
            
            current_date += timedelta(days=1)

        return total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    def print_statement(self, input_line: str) ->str:
        """Generate and print account statement with interest"""
        parts = input_line.strip().split()
        if len(parts) != 2:
            return "Invalid format. Expected: <Account> <Year><Month>"

        account, year_month = parts
        
        if len(year_month) != 6 or not year_month.isdigit():
            return "Invalid year-month format. Use YYYYMM"
        
        if account not in self.accounts:
            return f"Account {account} not found"
        
        year = int(year_month[:4])
        month = int(year_month[4:])

        acc = self.accounts[account]
        month_transactions = []
        running_balance = Decimal('0')

        for transaction in acc.transactions:
            if transaction.date < f"{year:04d}{month:02d}01":
                if transaction.txn_type == 'W':
                    running_balance -= transaction.amount
                else:
                    running_balance += transaction.amount
        
        for transaction in acc.transactions:
            if transaction.date.startswith(year_month):
                if transaction.txn_type == 'W':
                    running_balance -= transaction.amount
                else:
                    running_balance += transaction.amount
                month_transactions.append((transaction, running_balance))

        interest = self.calculate_interest(account, year_month)

        result = [f"Account: {account}"]
        result.append("| Date     | Txn Id      | Type | Amount  | Balance  |")

        for transaction, balance in month_transactions:
            txn_id_display = transaction.txn_id if transaction.txn_id else " " * 11
            result.append(f"| {transaction.date} | {txn_id_display:11} | {transaction.txn_type:4} | {transaction.amount:7.2f} | {balance:8.2f} |")

        if interest > 0:
            final_balance = running_balance + interest
            last_day = datetime(year, month, 1)
            if month == 12:
                last_day = datetime(year +1, 1, 1) - timedelta(days=1)
            else:
                last_day = datetime(year, month + 1, 1) - timedelta(days=1)
            
            last_day_str = last_day.strftime('%Y%m%d')
            result.append(f"| {last_day_str} | {' ':11} | I    | {interest:7.2f} | {final_balance:8.2f} |")

            interest_txn = Transaction(last_day_str, account, "I", interest)
            self.accounts[account].add_transaction (interest_txn)
        
        return "\n".join(result)

def main():
    """Main application loop"""
    banking_system = BankingSystem()

    print("Welcome to AwesomeGIC Bank! What would you like to do?")

    while True:
        print("[T] Input transactions")
        print("[I] Define interest rules")
        print("[P] Print statement")
        print("[Q] Quit")
        
        choice = input("> ").strip().upper()

        if choice == 'T':
            print("Please enter transaction details in <Date> <Account> <Type> <Amount> format")
            print("(or enter blank to go back to main menu):")
            transaction_input = input("> ").strip()
            if not transaction_input:
                continue
            result = banking_system.input_transaction(transaction_input)
            print(result)
            print("\nIs there anything else you'd like to do?")
            
        elif choice == "I":
            print("Please enter interest rules details in <Date> <RuleId> <Rate in %> format")
            print("(or enter blank to go back to main menu):")
            rule_input = input("> ").strip()
            if not rule_input:
                continue
            result = banking_system.define_interest_rule(rule_input)
            print(result)
            print("\nIs there anything else you'd like to do?")

        elif choice == 'P':
            print("Please enter account details in <Account> <Year><Month> format")
            print("(or enter blank to go back to main menu):")
            statement_input = input("> ").strip()
            if not statement_input:
                continue
            result = banking_system.print_statement(statement_input)
            print(result)
            print("\nIs there anything else you'd like to do?")
            
        elif choice == "Q":
            print("Thank you for banking with AwesomeGIC Bank")
            print("Have a nice day!")
            break
            
        else:
            print("Invalid option. Please try again.")
            print()

if __name__ == "__main__":
    main()