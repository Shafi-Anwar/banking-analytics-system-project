CREATE DATABASE IF NOT EXISTS banking;
USE banking;

CREATE TABLE Customers (
    customer_id INT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(50),
    address VARCHAR(255),
    date_of_birth DATE,
    account_open_date DATE
);

CREATE TABLE Accounts (
    account_id INT PRIMARY KEY,
    customer_id INT,
    account_type VARCHAR(20),
    balance DECIMAL(12,2),
    currency VARCHAR(10),
    created_at DATE,
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE Transactions (
    transaction_id INT PRIMARY KEY,
    account_id INT,
    timestamp DATETIME,
    amount DECIMAL(12,2),
    transaction_type VARCHAR(20),
    merchant VARCHAR(100),
    status VARCHAR(20),
    FOREIGN KEY (account_id) REFERENCES Accounts(account_id)
);

CREATE TABLE Loans (
    loan_id INT PRIMARY KEY,
    customer_id INT,
    loan_type VARCHAR(20),
    amount DECIMAL(12,2),
    interest_rate DECIMAL(5,2),
    start_date DATE,
    end_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);

CREATE TABLE CreditCards (
    card_id INT PRIMARY KEY,
    customer_id INT,
    card_type VARCHAR(20),
credit_limit DECIMAL(12,2),
    balance DECIMAL(12,2),
    expiry_date DATE,
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
);
SELECT c.name,c.email,a.balance,a.account_type FROM customers AS c
JOIN accounts AS a ON c.customer_id = a.customer_id
ORDER BY a.balance DESC;

SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM accounts;
SELECT COUNT(*) FROM transactions;
SELECT COUNT(*) FROM loans;
SELECT COUNT(*) FROM creditcards;

-- Which customer have most balance in their accutn
SELECT c.customer_id, c.name, SUM(a.balance) AS total_balance
FROM Customers c
JOIN Accounts a ON c.customer_id = a.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_balance DESC;
-- Average amount by customer_id
SELECT account_id, AVG(amount) AS avg_amount
FROM Transactions
GROUP BY account_id
ORDER BY avg_amount DESC;

-- Show each customer’s name, their account balance, and loan status.
SELECT loan_type, COUNT(*) AS loan_count
FROM Loans
GROUP BY loan_type
ORDER BY loan_count DESC;

SELECT card_id, customer_id, credit_limit, balance,
       (balance/credit_limit)*100 AS usage_percent
FROM CreditCards
WHERE balance/credit_limit > 0.9
ORDER BY usage_percent DESC;

--  Find customers who are using more than 80% of their credit limit AND have high transaction volumes.
SELECT c.name, cc.card_type, cc.credit_limit, cc.balance,
       SUM(t.amount) AS total_transactions,
       ROUND((cc.balance / cc.credit_limit) * 100, 2) AS usage_percent
FROM Customers c
JOIN CreditCards cc ON c.customer_id = cc.customer_id
JOIN Accounts a ON c.customer_id = a.customer_id
JOIN Transactions t ON a.account_id = t.account_id
GROUP BY c.name, cc.card_type, cc.credit_limit, cc.balance
HAVING usage_percent > 80
ORDER BY total_transactions DESC;

-- Detect customers with high balances but pending/rejected loans.

SELECT c.name, SUM(a.balance) AS total_balance, l.loan_type, l.amount,l.status
FROM customers AS c
JOIN accounts AS a ON c.customer_id = a.customer_id
JOIN loans AS l ON c.customer_id= l.customer_id
JOIN transactions t ON a.account_id = t.account_id
WHERE l.status IN ("Pending", "Rejected")
GROUP BY c.name,l.loan_type,l.amount,l.status
ORDER BY total_balance DESC;

-- Full customer profile: account balance, loan info, credit card usage, and total transaction volume.

SELECT c.customer_id,c.name,  SUM(a.balance) AS total_balance,
	COUNT(DISTINCT t.transaction_id) AS total_transactions,
    COALESCE(COUNT(l.loan_id), 0) AS total_loans,
    COALESCE(SUM(cc.balance),0) AS credit_card_balance,
    COALESCE(SUM(cc.credit_limit),0 ) AS credit_limit
FROM customers AS c
LEFT JOIN accounts AS a ON c.customer_id = a.customer_id
LEFT JOIN transactions AS t ON a.account_id = t.account_id
LEFT JOIN loans AS l ON c.customer_id = l.customer_id
LEFT JOIN creditcards AS cc ON c.customer_id = cc.customer_id
GROUP BY c.customer_id, c.name
ORDER BY total_loans DESC;