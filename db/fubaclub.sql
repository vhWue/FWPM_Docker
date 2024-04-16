-- Create a new database (if it doesn't exist already)
CREATE DATABASE IF NOT EXISTS football_club_db;

-- Switch to use the newly created database
USE football_club_db;

-- Table for Football Clubs
CREATE TABLE clubs (
    club_id INT AUTO_INCREMENT PRIMARY KEY,
    club_name VARCHAR(255) NOT NULL
);

-- Table for Players
CREATE TABLE players (
    player_id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(255) NOT NULL,
    club_id INT,
    FOREIGN KEY (club_id) REFERENCES clubs(club_id)
);

-- Example Data Insertion (Optional)
INSERT INTO clubs (club_name) VALUES
    ('Manchester United'),
    ('Real Madrid'),
    ('FC Barcelona');

INSERT INTO players (player_name, club_id) VALUES
    ('Cristiano Ronaldo', 2), -- Ronaldo plays for Real Madrid
    ('Lionel Messi', 3),       -- Messi plays for FC Barcelona
    ('Paul Pogba', 1);         -- Pogba plays for Manchester United
