-- Διαγραφή views
DROP VIEW IF EXISTS attendance_summary;
DROP VIEW IF EXISTS active_members_today;

-- Διαγραφή πινάκων με εξαρτήσεις
DROP TABLE IF EXISTS attendance CASCADE;
DROP TABLE IF EXISTS member_subscription CASCADE;
DROP TABLE IF EXISTS member CASCADE;
DROP TABLE IF EXISTS subscription CASCADE;

-- Δημιουργία πινάκων
CREATE TABLE Subscription (
    subscription_id SERIAL PRIMARY KEY,
    type VARCHAR(50) NOT NULL,
    price NUMERIC(6,2) NOT NULL,
    duration_months INT NOT NULL
);

CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(50),
    surname VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(15)
);

CREATE TABLE Member_Subscription (
    member_subscription_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id) ON DELETE CASCADE,
    subscription_id INT REFERENCES Subscription(subscription_id),
    start_date DATE,
    end_date DATE
);

CREATE TABLE Attendance (
    attendance_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id) ON DELETE CASCADE,
    date DATE NOT NULL
);

-- Συνδρομές
INSERT INTO Subscription (type, price, duration_months) VALUES
('Μηνιαία', 30.0, 1),
('Τρίμηνη', 80.0, 3),
('Εξαμηνιαία', 150.0, 6),
('Ετήσια', 280.0, 12);

-- Μέλη
INSERT INTO Member (name, surname, email, phone) VALUES
('Νίκος', 'Παπαδόπουλος', 'user1@example.com', '6900000001'),
('Μαρία', 'Ιωάννου', 'user2@example.com', '6900000002'),
('Γιώργος', 'Κωνσταντίνου', 'user3@example.com', '6900000003'),
('Ελένη', 'Γεωργίου', 'user4@example.com', '6900000004'),
('Δημήτρης', 'Νικολάου', 'user5@example.com', '6900000005'),
('Κατερίνα', 'Σταμάτη', 'user6@example.com', '6900000006'),
('Αντώνης', 'Αλεξίου', 'user7@example.com', '6900000007'),
('Σοφία', 'Χατζηδάκη', 'user8@example.com', '6900000008'),
('Θανάσης', 'Λαμπρόπουλος', 'user9@example.com', '6900000009'),
('Ιωάννα', 'Διαμαντή', 'user10@example.com', '6900000010'),
('Παναγιώτης', 'Κουρής', 'user11@example.com', '6900000011'),
('Αναστασία', 'Βλαχάκης', 'user12@example.com', '6900000012'),
('Κώστας', 'Στεργίου', 'user13@example.com', '6900000013'),
('Χριστίνα', 'Καρρά', 'user14@example.com', '6900000014'),
('Βασίλης', 'Αντωνίου', 'user15@example.com', '6900000015'),
('Αργυρώ', 'Παπαστεργίου', 'user16@example.com', '6900000016'),
('Μιχάλης', 'Σιδηρόπουλος', 'user17@example.com', '6900000017'),
('Ράνια', 'Λυμπεροπούλου', 'user18@example.com', '6900000018'),
('Αλέξανδρος', 'Μακρής', 'user19@example.com', '6900000019'),
('Ζωή', 'Καραγιάννη', 'user20@example.com', '6900000020');

-- Συνδρομές Μελών
INSERT INTO Member_Subscription (member_id, subscription_id, start_date, end_date) VALUES
(17, 3, '2025-06-16', '2025-12-13'),
(4, 2, '2025-04-06', '2025-07-05'),
(8, 3, '2025-06-06', '2025-12-03'),
(11, 2, '2025-05-27', '2025-08-25'),
(13, 2, '2025-02-20', '2025-05-21'),
(9, 2, '2025-02-20', '2025-05-21'),
(5, 2, '2025-02-02', '2025-05-03'),
(3, 2, '2025-04-17', '2025-07-16'),
(16, 2, '2025-02-17', '2025-05-18'),
(15, 3, '2025-02-01', '2025-07-31'),
(7, 4, '2025-01-01', '2025-12-27'),
(18, 4, '2025-04-01', '2026-03-27'),
(6, 1, '2025-01-08', '2025-02-07'),
(10, 3, '2025-03-17', '2025-09-13'),
(20, 1, '2025-06-01', '2025-07-01');

-- Παρουσίες Ιουνίου 2025
INSERT INTO Attendance (member_id, date) VALUES
(16, '2025-06-12'),
(14, '2025-06-13'),
(16, '2025-06-11'),
(12, '2025-06-15'),
(8, '2025-06-18'),
(17, '2025-06-15'),
(16, '2025-06-05'),
(2, '2025-06-21'),
(5, '2025-06-19'),
(3, '2025-06-01'),
(8, '2025-06-14'),
(8, '2025-06-05'),
(18, '2025-06-21'),
(19, '2025-06-15'),
(6, '2025-06-17'),
(7, '2025-06-14'),
(7, '2025-06-05'),
(4, '2025-06-16'),
(6, '2025-06-19'),
(19, '2025-06-06'),
(18, '2025-06-03'),
(18, '2025-06-12'),
(20, '2025-06-19'),
(13, '2025-06-20'),
(18, '2025-06-15'),
(12, '2025-06-10'),
(10, '2025-06-07'),
(19, '2025-06-15'),
(1, '2025-06-02');

-- Όψεις
CREATE VIEW attendance_summary AS
SELECT 
    m.member_id, 
    m.name, 
    m.surname, 
    COUNT(a.attendance_id) AS total_visits
FROM Member m
LEFT JOIN Attendance a 
    ON m.member_id = a.member_id
GROUP BY m.member_id;

CREATE VIEW active_members_today AS
SELECT 
    m.member_id, 
    m.name, 
    m.surname, 
    s.type
FROM Member m
JOIN Member_Subscription ms 
    ON m.member_id = ms.member_id
JOIN Subscription s 
    ON ms.subscription_id = s.subscription_id
WHERE CURRENT_DATE BETWEEN ms.start_date AND ms.end_date;
