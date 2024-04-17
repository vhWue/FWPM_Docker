-- Create a new database (if it doesn't exist already)
CREATE DATABASE IF NOT EXISTS fuba;

-- Switch to use the newly created database
USE fuba;

-- Table for Football Clubs
CREATE TABLE clubs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Table for Players
CREATE TABLE players (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES clubs(id)
);

-- Example Data Insertion (Optional)
INSERT INTO clubs (name) VALUES
    ('Manchester United'),
    ('Real Madrid'),
    ('FC Barcelona');

INSERT INTO players (name, id) VALUES
    ('Cristiano Ronaldo', 2), -- Ronaldo plays for Real Madrid
    ('Lionel Messi', 3),       -- Messi plays for FC Barcelona
    ('Paul Pogba', 1);         -- Pogba plays for Manchester United
