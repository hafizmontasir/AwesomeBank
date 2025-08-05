"""Unit tests for the AwesomeGIC Banking System"""

import unittest
from decimal import Decimal
from bank_system import BankingSystem, Account, Transaction, InterestRule

class TestTransaction(unittest.TestCase):
    """Test Transaction class"""
    
    def test_transaction_creation(self):
        """Test transaction object creation"""
        txn = Transaction("20230626", "AC001", "D", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn.date, "20230626")
        self.assertEqual(txn.account, "AC001")
        self.assertEqual(txn.txn_type, "D")
        self.assertEqual(txn.amount, Decimal("100.00"))
        self.assertEqual(txn.txn_id, "20230626-01")
    
    def test_transaction_type_case_insensitive(self):
        """Test Transaction type is converted to uppercase"""
        txn = Transaction("20230626", "AC001", "d", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn.txn_type, "D")
        
        txn2 = Transaction("20230626", "AC001", "w", Decimal('100.00'), "20230626-01")
        self.assertEqual(txn2.txn_type, "W")
        
    
class TestInterestRule(unittest.TestCase):
    """Test InterestRule class"""
    
    def test_interest_rule_creation(self):
        rule = InterestRule("20230615", "RULE03", Decimal('2.20'))
        self.assertEqual(rule.date, "20230615")
        self.assertEqual(rule.rule_id, "RULE03")
        self.assertEqual(rule.rate, Decimal('2.20'))
        

class TestAccount(unittest.TestCase):
    """Test Account class"""
    def setUp(self):
        """setup test account"""
        self.account = Account("AC001")

    def test_account_creation(self):
        """Test account object creation"""
        self.assertEqual(self.account.account_id, "AC001")
        self.assertEqual(len(self.account.transactions), 0)
        self.assertEqual(self.account.balance, Decimal('0'))
        
    def test_withdrawal_transaction(self):
        """Test adding withdrawl transaction"""
        deposit = Transaction("20230626", "AC001", "D", Decimal('100.00'))
        self.account.add_transaction(deposit)
        
        withdrawal = Transaction("20230627", "AC001", "W", Decimal('50.00'))
        self.account.add_transaction(withdrawal)
        
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.balance, Decimal('50.00'))
        
    def test_insufficient_balance_withdrawal(self):
        """Test withdrawal with insufficient balance"""
        withdrawal = Transaction("20230626", "AC001", "W", Decimal('100.00'))

        with self.assertRaises(ValueError):
            self.account.add_transaction(withdrawal)

    def test_interest_transaction(self):
        """Test adding interest transaction"""
        deposit = Transaction("20230626", "AC001", "D", Decimal('100.00'))
        self.account.add_transaction(deposit)
        
        interest = Transaction("20230630", "AC001", "I", Decimal('0.39'))
        self.account.add_transaction(interest)
        
        self.assertEqual(len(self.account.transactions), 2)
        self.assertEqual(self.account.balance, Decimal('100.39'))
        
    def test_get_balance_at_date(self):
        """Test getting balance at specific date"""
        txn1 = Transaction("20230601", "AC001", "D", Decimal('100.00'))
        txn2 = Transaction("20230615", "AC001", "D", Decimal('50.00'))
        txn3 = Transaction("20230620", "AC001", "W", Decimal('30.00'))

        self.account.add_transaction(txn1)
        self.account.add_transaction(txn2)
        self.account.add_transaction(txn3)

        self.assertEqual(self.account.get_balance_at_date('20230531'), Decimal('0'))
        self.assertEqual(self.account.get_balance_at_date('20230601'), Decimal('100.00'))
        self.assertEqual(self.account.get_balance_at_date('20230615'), Decimal('150.00'))
        self.assertEqual(self.account.get_balance_at_date('20230620'), Decimal('120.00'))


class TestBankingSystem(unittest.TestCase):
    """Test BankingSystem class"""
    
    def setUp(self):
        """Set up test banking system"""
        self.banking_system = BankingSystem()

    def test_validate_date(self):
        """Test date validation"""
        self.assertTrue(self.banking_system.validate_date("20230626"))
        self.assertFalse(self.banking_system.validate_date("2023626"))
        self.assertFalse(self.banking_system.validate_date("20230631"))
        self.assertFalse(self.banking_system.validate_date("abcd1234"))
            
    def test_validate_amount(self):
        """Test amount validation"""
        self.assertTrue(self.banking_system.validate_amount("100.00"))
        self.assertTrue(self.banking_system.validate_amount("100.5"))
        self.assertTrue(self.banking_system.validate_amount("100"))
        self.assertFalse(self.banking_system.validate_amount("0"))
        self.assertFalse(self.banking_system.validate_amount("-100"))
        self.assertFalse(self.banking_system.validate_amount("100.123")) 
        self.assertFalse(self.banking_system.validate_amount("abc"))

    def test_generate_transaction_id(self):
        """Test transaction ID generation"""
        id1 = self.banking_system.generate_transaction_id("20230626")
        id2 = self.banking_system.generate_transaction_id("20230626")
        id3 = self.banking_system.generate_transaction_id("20230627")
        
        self.assertEqual(id1, "20230626-01")
        self.assertEqual(id2, "20230626-02")
        self.assertEqual(id3, "20230627-01")
        
    def test_input_transaction_deposit(self):
        """Test input transaction for deposit"""
        result = self.banking_system.input_transaction("20230626 AC001 D 100.00")
        
        self.assertIn("Account: AC001", result)
        self.assertIn("D", result)
        self.assertIn("100.00", result)
        self.assertIn("AC001", self.banking_system.accounts)
        
    def test_input_transaction_withdrawal(self):
        """Test input transaction for withdrawal"""
        # First deposit
        self.banking_system.input_transaction("20230626 AC001 D 200.00")
        
        result = self.banking_system.input_transaction("20230627 AC001 W 100.00")
        
        self.assertIn("Account: AC001", result)
        self.assertIn("W", result)
        self.assertIn("100.00", result)
        
    def test_input_transaction_invalid_format(self):
        """Test input transaction with invalid format"""
        result = self.banking_system.input_transaction("20230626 AC001 D")
        self.assertIn("Invalid format", result)
        
    def test_input_transaction_withdrawal_from_new_account(self):
        """Test withdrawal from new account"""
        result = self.banking_system.input_transaction("20230626 AC001 W 100.00")
        self.assertIn("Cannot withdraw from new account", result)
    
    def test_input_transaction_insufficient_balance(self):
        """Test withdrawal with insufficient balance"""
        self.banking_system.input_transaction("20230626 AC001 D 50.00")
        
        # Try to withdraw more
        result = self.banking_system.input_transaction("20230627 AC001 W 100.00")
        self.assertIn("Insufficient balance", result)
    
    def test_define_interest_rule(self):
        """Test defining interest rule"""
        result = self.banking_system.define_interest_rule("20230615 RULE03 2.20")
        
        self.assertIn("Interest rules:", result)
        self.assertIn("RULE03", result)
        self.assertIn("2.20", result)
        self.assertEqual(len(self.banking_system.interest_rules), 1)
    
    def test_define_interest_rule_replace_same_date(self):
        """Test replacing interest rule for same date"""
        # Add first rule
        self.banking_system.define_interest_rule("20230615 RULE03 2.20")
        # Add second rule for same date
        result = self.banking_system.define_interest_rule("20230615 RULE04 2.50")
        
        self.assertEqual(len(self.banking_system.interest_rules), 1)
        self.assertIn("RULE04", result)
        self.assertIn("2.50", result)
    
    def test_define_interest_rule_invalid_date(self):
        """Test defining interest rule with invalid date"""
        result = self.banking_system.define_interest_rule("2023615 RULE03 2.20")
        self.assertIn("Invalid date format", result)
    
    def test_define_interest_rule_invalid_rate(self):
        """Test defining interest rule with invalid rate"""
        result = self.banking_system.define_interest_rule("20230615 RULE03 0")
        self.assertIn("Interest rate must be between 0 and 100", result)
        
        result = self.banking_system.define_interest_rule("20230615 RULE03 100")
        self.assertIn("Interest rate must be between 0 and 100", result)
    
    def test_calculate_interest(self):
        """Test interest calculation"""
        self.banking_system.input_transaction("20230601 AC001 D 150.00")
        self.banking_system.input_transaction("20230626 AC001 W 20.00")
        self.banking_system.input_transaction("20230626 AC001 W 100.00")
        
        self.banking_system.define_interest_rule("20230520 RULE02 1.90")
        self.banking_system.define_interest_rule("20230615 RULE03 2.20")
        
        # Calculate interest for June 2023
        interest = self.banking_system.calculate_interest("AC001", "202306")
        
        # Expected calculation:
        # 20230601-20230614: 150 * 1.90% * 14 / 365 = 0.109
        # 20230615-20230625: 150 * 2.20% * 11 / 365 = 0.099
        # 20230626-20230630: 30 * 2.20% * 5 / 365 = 0.009
        # Total = 0.217, rounded to 0.22
        
        self.assertAlmostEqual(float(interest), 0.22, places=2)
    
    def test_print_statement(self):
        """Test printing statement"""
        self.banking_system.input_transaction("20230505 AC001 D 100.00")
        self.banking_system.input_transaction("20230601 AC001 D 150.00")
        self.banking_system.input_transaction("20230626 AC001 W 20.00")
        self.banking_system.input_transaction("20230626 AC001 W 100.00")
        
        self.banking_system.define_interest_rule("20230520 RULE02 1.90")
        self.banking_system.define_interest_rule("20230615 RULE03 2.20")
        
        # Print statement for June 2023
        result = self.banking_system.print_statement("AC001 202306")
        
        self.assertIn("Account: AC001", result)
        self.assertIn("20230601", result)
        self.assertIn("250.00", result) 
        self.assertIn("130.00", result)
        self.assertIn("I", result)
        self.assertIn("0.39", result)
    
    def test_print_statement_invalid_format(self):
        """Test printing statement with invalid format"""
        result = self.banking_system.print_statement("AC001")
        self.assertIn("Invalid format", result)
    
    def test_print_statement_invalid_year_month(self):
        """Test printing statement with invalid year-month"""
        result = self.banking_system.print_statement("AC001 20236")
        self.assertIn("Invalid year-month format", result)
    
    def test_print_statement_invalid_month(self):
        """Test printing statement with invalid month"""
        # First create an account
        self.banking_system.input_transaction("20230601 AC001 D 100.00")
        
        result = self.banking_system.print_statement("AC001 202300")
        self.assertIn("Invalid month. Month must be between 01 and 12", result)
        
        result = self.banking_system.print_statement("AC001 202313")
        self.assertIn("Invalid month. Month must be between 01 and 12", result)
    
    def test_print_statement_account_not_found(self):
        """Test printing statement for non-existent account"""
        result = self.banking_system.print_statement("AC999 202306")
        self.assertIn("Account AC999 not found", result)
    
    def test_get_account_statement(self):
        """Test getting account statement"""
        self.banking_system.input_transaction("20230626 AC001 D 100.00")
        self.banking_system.input_transaction("20230627 AC001 W 50.00")
        
        result = self.banking_system.get_account_statement("AC001")
        
        self.assertIn("Account: AC001", result)
        self.assertIn("20230626", result)
        self.assertIn("D", result)
        self.assertIn("100.00", result)
        self.assertIn("W", result)
        self.assertIn("50.00", result)
    
    def test_get_account_statement_not_found(self):
        """Test getting statement for non-existent account"""
        result = self.banking_system.get_account_statement("AC999")
        self.assertIn("Account AC999 not found", result)


class TestIntegration(unittest.TestCase):
    """Integration Tests"""
    def setUp(self):
        """Set up intergration test banking system"""
        self.banking_system = BankingSystem()
        
    def test_full_workflow(self):
        """Test complete banking workflow from requirements"""
        result1 = self.banking_system.input_transaction("20230505 AC001 D 100.00")
        self.assertIn("Account: AC001", result1) 

        self.banking_system.input_transaction("20230601 AC001 D 150.00")
        self.banking_system.input_transaction("20230626 AC001 W 20.00")
        result4 = self.banking_system.input_transaction("20230626 AC001 W 100.00")
        
        self.assertIn("20230505", result4)
        self.assertIn("20230601", result4)
        self.assertIn("20230626", result4)
        
        # Add interest rules
        self.banking_system.define_interest_rule("20230101 RULE01 1.95")
        self.banking_system.define_interest_rule("20230520 RULE02 1.90")
        result_rules = self.banking_system.define_interest_rule("20230615 RULE03 2.20")
        
        # Verify rules are sorted by date
        lines = result_rules.split('\n')
        rule_lines = [line for line in lines if 'RULE' in line]
        self.assertEqual(len(rule_lines), 3)
        self.assertIn("RULE01", rule_lines[0])
        self.assertIn("RULE02", rule_lines[1])  
        self.assertIn("RULE03", rule_lines[2])
        
        statement = self.banking_system.print_statement("AC001 202306")
        
        # Verify statement contains expected elements
        self.assertIn("Account: AC001", statement)
        self.assertIn("20230601", statement)
        self.assertIn("250.00", statement)  # Balance after June deposit
        self.assertIn("230.00", statement)  # Balance after first withdrawal
        self.assertIn("130.00", statement)  # Balance after second withdrawal
        self.assertIn("20230630", statement)  # Interest date
        self.assertIn("I", statement)  # Interest transaction type
        self.assertIn("0.39", statement)
        self.assertIn("130.39", statement)
    
    def test_edge_cases(self):
        """Test edge cases and boundary conditions"""
        # Test transaction on leap year
        self.banking_system.input_transaction("20240229 AC001 D 100.00")
        self.assertIn("AC001", self.banking_system.accounts)
        
        # Test very small amounts
        self.banking_system.input_transaction("20230626 AC002 D 0.01")
        self.assertEqual(self.banking_system.accounts["AC002"].balance, Decimal('0.01'))
        
        # Test maximum decimal precision
        self.banking_system.input_transaction("20230626 AC003 D 99.99")
        self.assertEqual(self.banking_system.accounts["AC003"].balance, Decimal('99.99'))
        
        # Test interest calculation with zero balance days
        self.banking_system.input_transaction("20230601 AC004 D 100.00")
        self.banking_system.input_transaction("20230602 AC004 W 100.00")
        self.banking_system.define_interest_rule("20230101 RULE01 2.00")
        
        interest = self.banking_system.calculate_interest("AC004", "202306")
        expected_interest = Decimal('100') * Decimal('2.00') / Decimal('100') / Decimal('365')
        self.assertAlmostEqual(float(interest), float(expected_interest.quantize(Decimal('0.01'))), places=2)
        
        # Test multiple transactions same day
        self.banking_system.input_transaction("20230626 AC005 D 100.00")
        self.banking_system.input_transaction("20230626 AC005 D 50.00")
        self.banking_system.input_transaction("20230626 AC005 W 30.00")
        
        self.assertEqual(self.banking_system.accounts["AC005"].balance, Decimal('120.00'))
        
        # Verify transaction IDs are unique
        statement = self.banking_system.get_account_statement("AC005")
        self.assertIn("20230626-03", statement)
        self.assertIn("20230626-04", statement)
        self.assertIn("20230626-05", statement)
  
if __name__=='__main__':
    unittest.main(verbosity=2)