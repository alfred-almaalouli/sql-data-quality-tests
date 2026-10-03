-- Rows with typical data quality problems.
-- The tests load this file on top of seed.sql and expect every problem to be found.

INSERT INTO customers VALUES
 (6, 'Duplicate Anna', 'anna.schmidt@example.com', 'Essen', '2025-08-01'),   -- duplicate e-mail
 (7, 'No Mail',        NULL,                        'Bochum', '2025-08-02'),  -- missing e-mail
 (8, 'Bad Mail',       'bad-mail.example.com',      'Essen', '2025-08-03');   -- invalid e-mail

INSERT INTO products VALUES
 (7, 'Broken Price', 'Electronics', -5.00);                                   -- negative price

INSERT INTO orders VALUES
 (107, 99, '2025-08-05', 'DELIVERED',  29.90),                                -- unknown customer
 (108, 5,  '2099-01-01', 'SHIPPED',     4.50),                                -- order date in the future
 (109, 5,  '2025-08-10', 'LOST',       39.90),                                -- unknown status
 (110, 5,  '2025-08-12', 'DELIVERED', 100.00);                                -- total does not match items

INSERT INTO order_items VALUES
 (107, 4, 1, 29.90),
 (108, 6, 1,  4.50),
 (109, 5, 1, 39.90),
 (110, 5, 1, 39.90),
 (110, 42, 1, 9.99),                                                          -- unknown product
 (110, 6, 0,  4.50);                                                          -- quantity 0
