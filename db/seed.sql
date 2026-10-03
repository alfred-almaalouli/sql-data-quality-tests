-- Clean test data: every data quality check must pass on this data

INSERT INTO customers VALUES
 (1, 'Anna Schmidt',  'anna.schmidt@example.com',  'Essen',      '2025-01-10'),
 (2, 'Omar Haddad',   'omar.haddad@example.com',   'Dortmund',   '2025-02-03'),
 (3, 'Lena Fischer',  'lena.fischer@example.com',  'Düsseldorf', '2025-03-15'),
 (4, 'Marco Rossi',   'marco.rossi@example.com',   'Essen',      '2025-04-20'),
 (5, 'Sara Klein',    'sara.klein@example.com',    'Koblenz',    '2025-05-05');

INSERT INTO products VALUES
 (1, 'Laptop',          'Electronics', 899.00),
 (2, 'Headphones',      'Electronics',  79.90),
 (3, 'Office Chair',    'Furniture',   149.00),
 (4, 'Desk Lamp',       'Furniture',    29.90),
 (5, 'Python Book',     'Books',        39.90),
 (6, 'Notebook (A5)',   'Books',         4.50);

INSERT INTO orders VALUES
 (101, 1, '2025-06-01', 'DELIVERED',  978.90),
 (102, 2, '2025-06-03', 'DELIVERED',  149.00),
 (103, 1, '2025-06-15', 'SHIPPED',     48.90),
 (104, 3, '2025-07-02', 'DELIVERED',  159.80),
 (105, 4, '2025-07-10', 'CANCELLED',   29.90),
 (106, 2, '2025-07-21', 'DELIVERED',  938.90);

INSERT INTO order_items VALUES
 (101, 1, 1, 899.00),
 (101, 2, 1,  79.90),
 (102, 3, 1, 149.00),
 (103, 5, 1,  39.90),
 (103, 6, 2,   4.50),
 (104, 2, 2,  79.90),
 (105, 4, 1,  29.90),
 (106, 1, 1, 899.00),
 (106, 5, 1,  39.90);
