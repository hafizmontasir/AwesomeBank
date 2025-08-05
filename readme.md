# AwesomeGIC Banking System

A simple console-based banking system that handles transactions, interest calculations, and account statements.

## Features

- **Transaction Management**: Deposit and withdrawal operations with automatic balance tracking
- **Interest Calculation**: Configurable interest rules with daily compounding
- **Account Statements**: Detailed monthly statements with transaction history and interest
- **Input Validation**: Comprehensive validation for dates, amounts, and transaction types
- **Unique Transaction IDs**: Automatic generation of unique transaction identifiers

## Requirements

- Python 3.6 or higher
- No external dependencies (uses only Python standard library)

## File Structure

```
bank_system.py    # Main application code
test_bank_system.py    # Comprehensive unit tests
README.md           # This file
```

## How to Run

### Running the Application

1. Make sure you have Python 3.6+ installed
2. Save the `bank_system.py` file to your desired directory
3. Open a terminal/command prompt and navigate to that directory
4. Run the application:

```bash
python3 bank_system.py
```

or on Windows:

```bash
python bank_system.py
```

### Running the Tests

To run the comprehensive unit tests:

```bash
python3 test_bank_system.py
```

or on Windows:

```bash
python test_bank_system.py
```

For verbose test output:

```bash
python3 test_bank_system.py -v
```

## Usage Guide

### Main Menu Options

When you start the application, you'll see:

```
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
>
```

### Input Transactions (T)

Enter transaction details in the format: `<Date> <Account> <Type> <Amount>`

**Example:**

```
> T
Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230626 AC001 D 100.00
```

**Format Rules:**

- **Date**: YYYYMMDD format (e.g., 20230626)
- **Account**: Any string identifier (e.g., AC001)
- **Type**: D for deposit, W for withdrawal (case insensitive)
- **Amount**: Positive number with max 2 decimal places

**Validation Rules:**

- First transaction on an account cannot be a withdrawal
- Withdrawals cannot exceed account balance
- All amounts must be positive
- Each transaction gets a unique ID in format YYYYMMDD-XX

### Define Interest Rules (I)

Enter interest rule details in the format: `<Date> <RuleId> <Rate in %>`

**Example:**

```
> I
Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 20230615 RULE03 2.20
```

**Format Rules:**

- **Date**: YYYYMMDD format - when the rule becomes effective
- **RuleId**: Any string identifier for the rule
- **Rate**: Interest rate percentage (between 0 and 100)

**Behavior:**

- If multiple rules exist for the same date, the latest one is kept
- Rules are applied from their effective date until a new rule takes effect
- Interest is calculated daily and compounded

### Print Statement (P)

Generate monthly account statements with interest calculations.

**Example:**

```
> P
Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
> AC001 202306
```

**Format Rules:**

- **Account**: The account identifier
- **Year/Month**: YYYYMM format (e.g., 202306 for June 2023)

**Statement Features:**

- Shows all transactions for the specified month
- Displays running balance after each transaction
- Calculates and applies interest on the last day of the month
- Interest is based on end-of-day balances and applicable rates

### Quit (Q)

Exit the application:

```
> Q
Thank you for banking with AwesomeGIC Bank.
Have a nice day!
```

## Interest Calculation Logic

Interest is calculated using the following method:

1. **Daily Calculation**: Interest is calculated on the end-of-day balance for each day
2. **Rate Application**: The interest rate in effect on each day is used
3. **Formula**: `Daily Interest = EOD Balance × Rate% × 1/365`
4. **Accumulation**: Daily interest amounts are summed for the entire month
5. **Rounding**: Final interest is rounded to 2 decimal places
6. **Credit Date**: Interest is credited on the last day of the month

**Example Calculation:**

```
Period: June 1-14, 2023
EOD Balance: $250.00
Rate: 1.90% (RULE02)
Days: 14
Interest: 250 × 1.90% × 14/365 = $0.182

Period: June 15-25, 2023
EOD Balance: $250.00
Rate: 2.20% (RULE03)
Days: 11
Interest: 250 × 2.20% × 11/365 = $0.166

Period: June 26-30, 2023
EOD Balance: $130.00
Rate: 2.20% (RULE03)
Days: 5
Interest: 130 × 2.20% × 5/365 = $0.039

Total Monthly Interest: $0.182 + $0.166 + $0.039 = $0.387 ≈ $0.39
```

## Test Coverage

The test suite includes:

- **Unit Tests**: Individual class and method testing
- **Integration Tests**: End-to-end workflow testing
- **Edge Case Tests**: Boundary conditions and error scenarios
- **Validation Tests**: Input validation and error handling

**Test Categories:**

- Transaction class functionality
- Interest rule management
- Account balance calculations
- Input validation
- Interest calculation accuracy
- Statement generation
- Error handling
- Full workflow scenarios

## Architecture Design

The system follows object-oriented principles with clear separation of concerns:

- **Transaction**: Represents individual bank transactions
- **InterestRule**: Manages interest rate rules and effective dates
- **Account**: Handles account-specific operations and balance tracking
- **BankingSystem**: Main controller coordinating all operations

**Key Design Decisions:**

- **Decimal Precision**: Uses Python's `Decimal` class for accurate financial calculations
- **In-Memory Storage**: No database required, suitable for demonstration purposes
- **Input Validation**: Comprehensive validation at multiple levels
- **Error Handling**: Graceful handling of invalid inputs with clear error messages
- **Modular Design**: Easy to extend and maintain

## Example Session

```
Welcome to AwesomeGIC Bank! What would you like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> T

Please enter transaction details in <Date> <Account> <Type> <Amount> format
(or enter blank to go back to main menu):
> 20230505 AC001 D 100.00

Account: AC001
| Date     | Txn Id      | Type | Amount |
| 20230505 | 20230505-01 | D    | 100.00 |

Is there anything else you'd like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> I

Please enter interest rules details in <Date> <RuleId> <Rate in %> format
(or enter blank to go back to main menu):
> 20230520 RULE02 1.90

Interest rules:
| Date     | RuleId | Rate (%) |
| 20230520 | RULE02 |     1.90 |

Is there anything else you'd like to do?
[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> P

Please enter account and month to generate the statement <Account> <Year><Month>
(or enter blank to go back to main menu):
> AC001 202305

Account: AC001
| Date     | Txn Id      | Type | Amount | Balance |
| 20230505 | 20230505-01 | D    | 100.00 |   100.00 |
| 20230531 |             | I    |   0.06 |   100.06 |

[T] Input transactions
[I] Define interest rules
[P] Print statement
[Q] Quit
> Q

Thank you for banking with AwesomeGIC Bank.
Have a nice day!
```
