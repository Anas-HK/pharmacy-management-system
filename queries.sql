-- =====================================================================
-- queries.sql  -  Sample DML / SELECT queries for demonstration & viva
-- Pharmacy Management System  (SQLite)
--
-- Build the database first (python init_db.py), then run any of these
-- in the SQLite shell, in "DB Browser for SQLite", or from the GUI.
-- =====================================================================

-- ---- 1. Basic SELECT : list every medicine ----
SELECT * FROM Medicine;

-- ---- 2. Projection + WHERE : medicines that cost more than 5.00 ----
SELECT medicine_name, unit_price, stock_quantity
FROM Medicine
WHERE unit_price > 5.00;

-- ---- 3. ORDER BY : medicines from most to least stock ----
SELECT medicine_name, stock_quantity
FROM Medicine
ORDER BY stock_quantity DESC;

-- ---- 4. LIKE search : find medicines whose name contains "cin" ----
SELECT * FROM Medicine
WHERE medicine_name LIKE '%cin%';

-- ---- 5. INNER JOIN : each medicine with its category and supplier ----
SELECT m.medicine_name, c.category_name, s.supplier_name, m.unit_price
FROM Medicine m
JOIN Category c ON m.category_id = c.category_id
JOIN Supplier s ON m.supplier_id = s.supplier_id;

-- ---- 6. Multi-table JOIN : full invoice lines ----
SELECT sl.sale_id, sl.sale_date, cu.customer_name, em.employee_name,
       m.medicine_name, si.quantity, si.unit_price, si.subtotal
FROM Sale sl
JOIN Customer  cu ON sl.customer_id = cu.customer_id
JOIN Employee  em ON sl.employee_id = em.employee_id
JOIN Sale_Item si ON si.sale_id     = sl.sale_id
JOIN Medicine  m  ON si.medicine_id = m.medicine_id
ORDER BY sl.sale_id;

-- ---- 7. Aggregate functions ----
SELECT COUNT(*)        AS total_medicines,
       AVG(unit_price) AS average_price,
       MAX(unit_price) AS most_expensive,
       MIN(unit_price) AS cheapest
FROM Medicine;

-- ---- 8. GROUP BY : how much each customer has spent ----
SELECT cu.customer_name,
       COUNT(sl.sale_id)     AS orders,
       SUM(sl.total_amount)  AS total_spent
FROM Customer cu
JOIN Sale sl ON cu.customer_id = sl.customer_id
GROUP BY cu.customer_id
ORDER BY total_spent DESC;

-- ---- 9. GROUP BY + HAVING : categories that have a medicine ----
SELECT c.category_name, COUNT(m.medicine_id) AS num_medicines
FROM Category c
JOIN Medicine m ON m.category_id = c.category_id
GROUP BY c.category_id
HAVING COUNT(m.medicine_id) >= 1;

-- ---- 10. Subquery : medicines priced above the average price ----
SELECT medicine_name, unit_price
FROM Medicine
WHERE unit_price > (SELECT AVG(unit_price) FROM Medicine);

-- ---- 11. Subquery / NOT IN : medicines that have never been sold ----
SELECT medicine_name
FROM Medicine
WHERE medicine_id NOT IN (SELECT DISTINCT medicine_id FROM Sale_Item);

-- ---- 12. Business report : low stock medicines (< 100 units) ----
SELECT medicine_name, stock_quantity
FROM Medicine
WHERE stock_quantity < 100
ORDER BY stock_quantity ASC;

-- ---- 13. Business report : medicines expiring on/before 2026-09-30 ----
SELECT medicine_name, expiry_date
FROM Medicine
WHERE expiry_date <= '2026-09-30'
ORDER BY expiry_date ASC;

-- ---- 14. Inventory valuation (stock value per medicine) ----
SELECT medicine_name, stock_quantity, unit_price,
       ROUND(stock_quantity * unit_price, 2) AS stock_value
FROM Medicine
ORDER BY stock_value DESC;

-- =====================================================================
-- DML that changes data (INSERT / UPDATE / DELETE / TRANSACTION)
-- =====================================================================

-- ---- 15. INSERT : add a new category ----
INSERT INTO Category (category_name, description)
VALUES ('Probiotics','Gut health supplements');

-- ---- 16. UPDATE : increase stock of Paracetamol by 100 units ----
UPDATE Medicine
SET stock_quantity = stock_quantity + 100
WHERE medicine_name = 'Paracetamol 500mg';

-- ---- 17. UPDATE : give every Pharmacist a 10% raise ----
UPDATE Employee
SET salary = salary * 1.10
WHERE role = 'Pharmacist';

-- ---- 18. DELETE : remove the category added in query 15 ----
DELETE FROM Category
WHERE category_name = 'Probiotics';

-- ---- 19. Recalculate one sale's total from its items (derived value) --
UPDATE Sale
SET total_amount = (
    SELECT COALESCE(SUM(subtotal), 0)
    FROM Sale_Item
    WHERE Sale_Item.sale_id = Sale.sale_id
)
WHERE sale_id = 1;

-- ---- 20. TRANSACTION : sell 5 units of Paracetamol atomically ----
BEGIN TRANSACTION;
    UPDATE Medicine SET stock_quantity = stock_quantity - 5 WHERE medicine_id = 2;
    INSERT INTO Sale (customer_id, employee_id, sale_date, payment_method, total_amount)
    VALUES (1, 1, '2026-06-29', 'Cash', 6.00);
COMMIT;
