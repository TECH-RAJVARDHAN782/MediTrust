create database MEDITRUST;
USE MEDITRUST;
CREATE TABLE medicines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    barcode VARCHAR(20) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    composition VARCHAR(255),
    manufacturer VARCHAR(100),
    med_use VARCHAR(255),
    expiry DATE,
    isVerified VARCHAR(255)
);

INSERT INTO medicines (barcode, name, composition, manufacturer, med_use, expiry, isVerified) VALUES
('8901000000001','Dolo 650','Paracetamol 650mg','Micro Labs','Fever and pain relief','2026-12-01',true),
('8901000000002','Crocin','Paracetamol 500mg','GSK','Fever and mild pain','2026-10-01',true),
('8901000000003','Calpol','Paracetamol 500mg','GSK','Fever and headache','2027-01-01',true),
('8901000000004','Combiflam','Ibuprofen + Paracetamol','Sanofi','Pain relief and inflammation','2026-09-01',true),
('8901000000005','Augmentin 625','Amoxicillin + Clavulanic Acid','GSK','Bacterial infections','2026-11-01',true),
('8901000000006','Azithromycin','Azithromycin 500mg','Cipla','Bacterial infections','2026-08-01',true),
('8901000000007','Amoxicillin','Amoxicillin 500mg','Sun Pharma','Bacterial infections','2027-02-01',true),
('8901000000008','Cetirizine','Cetirizine 10mg','Dr. Reddy''s','Allergy relief','2026-07-01',true),
('8901000000009','Levocetirizine','Levocetirizine 5mg','Cipla','Allergic rhinitis','2026-06-01',true),
('8901000000010','Benadryl','Diphenhydramine','Johnson & Johnson','Cough and allergy','2026-05-01',true),
('8901000000011','Pantoprazole','Pantoprazole 40mg','Sun Pharma','Acidity and GERD','2027-03-01',true),
('8901000000012','Digene','Magnesium Hydroxide + Aluminium Hydroxide','Abbott','Acidity relief','2026-09-01',true),
('8901000000013','Rantac','Ranitidine','JB Chemicals','Acidity and ulcers','2026-04-01',true),
('8901000000014','ORS','Oral Rehydration Salts','Dabur','Dehydration treatment','2027-01-01',true),
('8901000000015','Vitamin D3','Cholecalciferol','Uprise','Bone health','2027-05-01',true),
('8901000000016','Zinc Tablets','Zinc Sulphate','Himalaya','Immunity support','2026-08-01',true),
('8901000000017','Metformin','Metformin 500mg','Sun Pharma','Diabetes management','2027-06-01',true),
('8901000000018','Amlodipine','Amlodipine 5mg','Cipla','Blood pressure control','2027-02-01',true),
('8901000000019','Atorvastatin','Atorvastatin 10mg','Dr. Reddy''s','Cholesterol control','2027-04-01',true),
('8901000000020','Insulin','Human Insulin','Novo Nordisk','Diabetes treatment','2026-12-01',true),
('8901000000021','Paracetamol Syrup','Paracetamol 250mg/5ml','Cipla','Fever in children','2026-10-01',true),
('8901000000022','Ibuprofen','Ibuprofen 400mg','Abbott','Pain and inflammation','2026-11-01',true),
('8901000000023','Omeprazole','Omeprazole 20mg','Dr. Reddy''s','Acidity and ulcers','2027-03-01',true),
('8901000000024','Cough Syrup','Dextromethorphan','Benadryl','Dry cough relief','2026-06-01',true);



SELECT * FROM MEDICINES;


