-- =====================================================================
-- seed.sql  -  Data Manipulation Language (DML)
-- Pharmacy Management System  (SQLite)
--
-- Inserts at least 20 records into every table.  Parent tables are
-- filled before child tables so all foreign keys stay valid.
-- =====================================================================

PRAGMA foreign_keys = ON;

-- ---------------------------------------------------------------------
-- Category  (20 records)
-- ---------------------------------------------------------------------
INSERT INTO Category (category_name, description) VALUES
('Antibiotics','Medicines that fight bacterial infections'),
('Analgesics','Pain relieving medicines'),
('Antipyretics','Fever reducing medicines'),
('Antihistamines','Allergy relief medicines'),
('Antacids','Medicines that reduce stomach acidity'),
('Vitamins & Supplements','Nutritional supplements and vitamins'),
('Antidiabetics','Medicines that control blood sugar'),
('Antihypertensives','Medicines that control blood pressure'),
('Cardiac','Heart related medicines'),
('Dermatological','Skin care and topical medicines'),
('Ophthalmic','Eye care medicines'),
('Respiratory','Asthma and breathing medicines'),
('Gastrointestinal','Digestive system medicines'),
('Antifungal','Medicines that treat fungal infections'),
('Antiviral','Medicines that treat viral infections'),
('Cough & Cold','Cough and cold relief medicines'),
('Sedatives','Sleep and anxiety relief medicines'),
('Hormonal','Hormone related medicines'),
('Vaccines','Preventive immunization products'),
('First Aid','Wound care and first aid items');

-- ---------------------------------------------------------------------
-- Supplier  (20 records)
-- ---------------------------------------------------------------------
INSERT INTO Supplier (supplier_name, contact_person, phone, email, address) VALUES
('Square Pharmaceuticals','Rahim Uddin','01711000001','info@squarepharma.com','Pabna'),
('Beximco Pharma','Karim Hossain','01711000002','contact@beximco.com','Dhaka'),
('Incepta Pharmaceuticals','Sadia Akter','01711000003','sales@incepta.com','Dhaka'),
('Renata Limited','Tanvir Ahmed','01711000004','info@renata.com','Mirpur'),
('ACI Pharma','Nadia Islam','01711000005','support@acipharma.com','Narayanganj'),
('ACME Laboratories','Faisal Karim','01711000006','info@acmelab.com','Dhamrai'),
('Aristopharma','Mitu Rahman','01711000007','sales@aristopharma.com','Dhaka'),
('Eskayef Pharma','Jamil Hasan','01711000008','info@skf.com','Tongi'),
('Opsonin Pharma','Rumana Begum','01711000009','contact@opsonin.com','Barishal'),
('Healthcare Pharma','Sabbir Alam','01711000010','info@healthcarepharma.com','Gazipur'),
('Drug International','Kamal Uddin','01711000011','sales@druginternational.com','Bogura'),
('General Pharma','Shahin Mia','01711000012','info@generalpharma.com','Dhaka'),
('Popular Pharma','Lima Khatun','01711000013','info@popularpharma.com','Dhaka'),
('Orion Pharma','Robiul Islam','01711000014','sales@orionpharma.com','Siddhirganj'),
('Globe Pharma','Anwar Hossain','01711000015','info@globepharma.com','Dhaka'),
('Navana Pharma','Sumi Akter','01711000016','contact@navanapharma.com','Dhaka'),
('Sharif Pharma','Delwar Hossain','01711000017','info@sharifpharma.com','Cumilla'),
('Ziska Pharma','Nazmul Huda','01711000018','sales@ziskapharma.com','Dhaka'),
('UniMed UniHealth','Parvez Khan','01711000019','info@unimed.com','Dhaka'),
('Beacon Pharma','Rita Das','01711000020','contact@beaconpharma.com','Bhaluka');

-- ---------------------------------------------------------------------
-- Medicine  (20 records)
--   category_id and supplier_id both reference the tables above (1-20).
-- ---------------------------------------------------------------------
INSERT INTO Medicine (medicine_name, category_id, supplier_id, unit_price, stock_quantity, expiry_date, batch_no) VALUES
('Amoxicillin 500mg',1,1,8.50,250,'2027-03-31','BATCH-AMX-01'),
('Paracetamol 500mg',3,2,1.20,800,'2027-06-30','BATCH-PCM-02'),
('Ibuprofen 400mg',2,3,3.00,400,'2026-09-30','BATCH-IBU-03'),
('Cetirizine 10mg',4,4,2.50,300,'2027-01-31','BATCH-CTZ-04'),
('Omeprazole 20mg',5,5,5.00,220,'2026-08-31','BATCH-OMP-05'),
('Vitamin C 1000mg',6,6,4.00,500,'2028-02-28','BATCH-VTC-06'),
('Metformin 500mg',7,7,3.75,180,'2027-05-31','BATCH-MET-07'),
('Amlodipine 5mg',8,8,4.25,160,'2027-04-30','BATCH-AML-08'),
('Atorvastatin 10mg',9,9,6.00,140,'2027-07-31','BATCH-ATR-09'),
('Hydrocortisone Cream 1%',10,10,7.50,90,'2026-10-31','BATCH-HYD-10'),
('Ciprofloxacin Eye Drops',11,11,9.00,70,'2026-07-31','BATCH-CIP-11'),
('Salbutamol Inhaler',12,12,12.00,60,'2027-02-28','BATCH-SAL-12'),
('Loperamide 2mg',13,13,2.20,350,'2027-09-30','BATCH-LOP-13'),
('Fluconazole 150mg',14,14,10.00,45,'2026-08-15','BATCH-FLU-14'),
('Acyclovir 400mg',15,15,11.50,80,'2027-11-30','BATCH-ACY-15'),
('Cough Syrup 100ml',16,16,3.50,280,'2026-09-15','BATCH-CGH-16'),
('Diazepam 5mg',17,17,5.50,30,'2027-08-31','BATCH-DZP-17'),
('Levothyroxine 50mcg',18,18,6.75,120,'2027-12-31','BATCH-LVT-18'),
('Hepatitis B Vaccine',19,19,250.00,25,'2026-12-31','BATCH-HBV-19'),
('Antiseptic Solution 100ml',20,20,2.80,600,'2028-05-31','BATCH-ANT-20');

-- ---------------------------------------------------------------------
-- Customer  (20 records)
-- ---------------------------------------------------------------------
INSERT INTO Customer (customer_name, phone, email, address) VALUES
('Aarav Sharma','01811000001','aarav.sharma@example.com','Dhanmondi, Dhaka'),
('Sophia Rahman','01811000002','sophia.rahman@example.com','Gulshan, Dhaka'),
('Mohammed Ali','01811000003','mohammed.ali@example.com','Banani, Dhaka'),
('Fatima Begum','01811000004','fatima.begum@example.com','Mirpur, Dhaka'),
('Rohan Das','01811000005','rohan.das@example.com','Uttara, Dhaka'),
('Ayesha Siddiqua','01811000006','ayesha.s@example.com','Mohakhali, Dhaka'),
('David Gomes','01811000007','david.gomes@example.com','Tejgaon, Dhaka'),
('Priya Saha','01811000008','priya.saha@example.com','Bashundhara, Dhaka'),
('Hasan Mahmud','01811000009','hasan.mahmud@example.com','Badda, Dhaka'),
('Nabila Karim','01811000010','nabila.karim@example.com','Khilgaon, Dhaka'),
('Tariq Aziz','01811000011','tariq.aziz@example.com','Motijheel, Dhaka'),
('Lamia Chowdhury','01811000012','lamia.c@example.com','Wari, Dhaka'),
('Sajid Khan','01811000013','sajid.khan@example.com','Rampura, Dhaka'),
('Mehnaz Sultana','01811000014','mehnaz.s@example.com','Shyamoli, Dhaka'),
('Arif Hossain','01811000015','arif.hossain@example.com','Farmgate, Dhaka'),
('Tania Akter','01811000016','tania.akter@example.com','Malibagh, Dhaka'),
('Kabir Ahmed','01811000017','kabir.ahmed@example.com','Jatrabari, Dhaka'),
('Sumaiya Islam','01811000018','sumaiya.i@example.com','Mohammadpur, Dhaka'),
('Rafiq Mia','01811000019','rafiq.mia@example.com','Gabtoli, Dhaka'),
('Jannat Ferdous','01811000020','jannat.f@example.com','Savar, Dhaka');

-- ---------------------------------------------------------------------
-- Employee  (20 records)
-- ---------------------------------------------------------------------
INSERT INTO Employee (employee_name, role, phone, salary, hire_date) VALUES
('Dr. Imran Hossain','Pharmacist','01911000001',45000,'2019-03-15'),
('Nusrat Jahan','Cashier','01911000002',22000,'2021-06-01'),
('Mahbub Alam','Manager','01911000003',60000,'2017-01-10'),
('Shreya Roy','Pharmacist','01911000004',43000,'2020-08-20'),
('Farhan Kabir','Sales Assistant','01911000005',20000,'2022-02-14'),
('Dr. Sadia Noor','Senior Pharmacist','01911000006',55000,'2016-09-05'),
('Rezaul Karim','Inventory Clerk','01911000007',25000,'2021-11-11'),
('Mim Akter','Cashier','01911000008',21500,'2023-03-01'),
('Tanjid Hasan','Sales Assistant','01911000009',19500,'2023-07-19'),
('Dr. Nayeem Islam','Pharmacist','01911000010',44000,'2019-12-02'),
('Sabrina Haque','Accountant','01911000011',38000,'2018-04-25'),
('Jahidul Islam','Inventory Clerk','01911000012',24000,'2022-10-30'),
('Promi Das','Cashier','01911000013',22000,'2021-05-17'),
('Asif Mahmood','Sales Assistant','01911000014',20500,'2023-01-09'),
('Dr. Rubaiya Zaman','Senior Pharmacist','01911000015',56000,'2015-06-21'),
('Habibur Rahman','Security','01911000016',18000,'2020-03-12'),
('Maliha Tasnim','Pharmacist','01911000017',42000,'2021-09-28'),
('Sohel Rana','Cleaner','01911000018',15000,'2019-07-07'),
('Nafisa Anjum','Assistant Manager','01911000019',48000,'2018-11-15'),
('Riyad Hasan','Sales Assistant','01911000020',20000,'2023-08-23');

-- ---------------------------------------------------------------------
-- Sale  (20 records)
--   customer_id and employee_id reference the tables above (1-20).
--   total_amount is left at 0 here and computed at the end from the
--   Sale_Item rows (a derived value), which avoids any data anomaly.
-- ---------------------------------------------------------------------
INSERT INTO Sale (customer_id, employee_id, sale_date, payment_method) VALUES
(1,1,'2026-06-01','Cash'),
(3,2,'2026-06-02','Card'),
(5,4,'2026-06-03','Mobile Banking'),
(2,5,'2026-06-05','Cash'),
(7,1,'2026-06-07','Card'),
(9,6,'2026-06-09','Cash'),
(4,8,'2026-06-10','Mobile Banking'),
(11,10,'2026-06-11','Card'),
(6,2,'2026-06-12','Cash'),
(13,9,'2026-06-13','Cash'),
(8,5,'2026-06-15','Mobile Banking'),
(15,1,'2026-06-16','Card'),
(10,13,'2026-06-18','Cash'),
(17,14,'2026-06-19','Cash'),
(12,4,'2026-06-20','Card'),
(19,10,'2026-06-21','Mobile Banking'),
(14,6,'2026-06-23','Card'),
(20,17,'2026-06-24','Cash'),
(16,8,'2026-06-26','Mobile Banking'),
(18,2,'2026-06-28','Cash');

-- ---------------------------------------------------------------------
-- Sale_Item  (22 records)
--   sale_id references Sale (1-20), medicine_id references Medicine
--   (1-20).  Sales 1 and 2 have two line items each, demonstrating the
--   many-to-many relationship between sales and medicines.
--   subtotal is computed below.
-- ---------------------------------------------------------------------
INSERT INTO Sale_Item (sale_id, medicine_id, quantity, unit_price) VALUES
(1,2,10,1.20),
(2,1,2,8.50),
(3,6,3,4.00),
(4,3,5,3.00),
(5,7,6,3.75),
(6,8,4,4.25),
(7,4,8,2.50),
(8,9,2,6.00),
(9,12,1,12.00),
(10,16,3,3.50),
(11,20,4,2.80),
(12,5,2,5.00),
(13,13,6,2.20),
(14,18,2,6.75),
(15,10,1,7.50),
(16,15,2,11.50),
(17,19,1,250.00),
(18,14,1,10.00),
(19,11,2,9.00),
(20,17,1,5.50),
(1,6,2,4.00),
(2,2,5,1.20);

-- ---------------------------------------------------------------------
-- Compute the derived values:
--   1) each line item's subtotal = quantity * unit_price
--   2) each sale's total_amount = sum of its line item subtotals
-- ---------------------------------------------------------------------
UPDATE Sale_Item
SET subtotal = ROUND(quantity * unit_price, 2);

UPDATE Sale
SET total_amount = ROUND((
    SELECT COALESCE(SUM(si.subtotal), 0)
    FROM Sale_Item si
    WHERE si.sale_id = Sale.sale_id
), 2);
