-- Create database
CREATE DATABASE IF NOT EXISTS me_api_playground;
USE me_api_playground;

-- Profiles table
CREATE TABLE profiles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    education TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Skills table
CREATE TABLE skills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    name VARCHAR(100) NOT NULL,
    level VARCHAR(20) DEFAULT 'beginner',
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Projects table
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    technologies TEXT,
    github_url VARCHAR(500),
    demo_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Work experiences table
CREATE TABLE work_experiences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    company VARCHAR(200) NOT NULL,
    position VARCHAR(200) NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    is_current BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Links table
CREATE TABLE links (
    id INT AUTO_INCREMENT PRIMARY KEY,
    profile_id INT NOT NULL,
    link_type VARCHAR(50) NOT NULL,
    url VARCHAR(500) NOT NULL,
    FOREIGN KEY (profile_id) REFERENCES profiles(id) ON DELETE CASCADE
);

-- Insert sample data
INSERT INTO profiles (name, email, education) VALUES 
('Manomay Mali', 'manomay2702@gmail.com', 'M.Sc. in Computer Science,Savitribai Phule Pune University');

SET @profile_id = LAST_INSERT_ID();

INSERT INTO skills (profile_id, name, level) VALUES 
(@profile_id, 'C', 'advanced'),
(@profile_id, 'C++', 'intermediate'),
(@profile_id, 'Java', 'intermediate'),
(@profile_id, 'Python', 'advanced'),
(@profile_id, 'JavaScript', 'intermediate'),
(@profile_id, 'Postgresql', 'intermediate'),
(@profile_id, 'MySQL', 'intermediate');

INSERT INTO projects (profile_id, title, description, technologies, github_url, demo_url) VALUES 
(@profile_id, 'Me-API Playground', 'Personal API playground for managing profile information', '["Python", "Flask", "MySQL", "JavaScript"]', 'https://github.com/johndoe/me-api', 'https://me-api.example.com');

INSERT INTO links (profile_id, link_type, url) VALUES 
(@profile_id, 'github', 'https://github.com/Manomay3447'),
(@profile_id, 'linkedin', 'https://www.linkedin.com/in/manomay-mali-35ba71251');
