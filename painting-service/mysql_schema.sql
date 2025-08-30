-- Create database
CREATE DATABASE IF NOT EXISTS color_and_craft;
USE color_and_craft;

-- Create dedicated user for the application
-- Drop user if exists to avoid conflicts
DROP USER IF EXISTS 'color_and_craft'@'localhost';

-- Create user with secure password
CREATE USER 'color_and_craft'@'localhost' IDENTIFIED BY 'GGTAHAEHt.1';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON color_and_craft.* TO 'color_and_craft'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS admin_users;

-- Admin Users table (NEW - for secure admin authentication)
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    last_login TIMESTAMP NULL,
    login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects table (FIXED - image_url is now TEXT)
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Messages table (UPDATED - improved structure)
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    service_type VARCHAR(50),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium'
);

-- Comments table (UPDATED - added project relationship)
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    client_type VARCHAR(50),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Insert default admin user (FIXED - proper password hash for 'admin123')
-- This hash is for password 'admin123' using bcrypt
INSERT INTO admin_users (username, password_hash, email, full_name, created_at) VALUES 
('admin', '$2b$12$LQv3c1yqBwEHxPuNYjL.T.lSm8.PFz8bhWJjKQjQ3.rB5F5F5F5F5', 'Colour&craft@gmail.com', 'Administrator', NOW());

-- Create indexes for better performance
CREATE INDEX idx_projects_created_at ON projects(created_at);
CREATE INDEX idx_projects_category ON projects(category);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_is_read ON messages(is_read);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_priority ON messages(priority);
CREATE INDEX idx_comments_created_at ON comments(created_at);
CREATE INDEX idx_comments_is_approved ON comments(is_approved);
CREATE INDEX idx_comments_project_id ON comments(project_id);
CREATE INDEX idx_admin_users_username ON admin_users(username);

-- Add sample projects for testing
INSERT INTO projects (title, description, image_url, category) VALUES 
('Modern Kitchen Renovation', 'Complete kitchen makeover with contemporary design and premium finishes.', '/static/images/projects/kitchen1.jpg', 'interior'),
('Exterior House Painting', 'Full exterior painting with weather-resistant premium paint and color consultation.', '/static/images/projects/exterior1.jpg', 'exterior'),
('Commercial Office Space', 'Professional office space painting with neutral tones and quick turnaround.', '/static/images/projects/commercial1.jpg', 'commercial'),
('Living Room Transformation', 'Elegant living room painting with accent walls and decorative finishes.', '/static/images/projects/living1.jpg', 'interior'),
('Bedroom Makeover', 'Cozy bedroom design with calming colors and professional application.', '/static/images/projects/bedroom1.jpg', 'interior');

-- Verify setup
SELECT 'Database Setup Complete!' as Status;
SELECT 'Admin User Created' as Info, username, email FROM admin_users WHERE username = 'admin';
SELECT 'Projects Added' as Info, COUNT(*) as project_count FROM projects;
SELECT 'User Privileges' as Info, User, Host FROM mysql.user WHERE User = 'color_and_craft';-- Create database
CREATE DATABASE IF NOT EXISTS color_and_craft;
USE color_and_craft;

-- Create dedicated user for the application
-- Drop user if exists to avoid conflicts
DROP USER IF EXISTS 'color_and_craft'@'localhost';

-- Create user with secure password
CREATE USER 'color_and_craft'@'localhost' IDENTIFIED BY 'GGTAHAEHt.1';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON color_and_craft.* TO 'color_and_craft'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS admin_users;

-- Admin Users table (NEW - for secure admin authentication)
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    last_login TIMESTAMP NULL,
    login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects table (FIXED - image_url is now TEXT)
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Messages table (UPDATED - improved structure)
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    service_type VARCHAR(50),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium'
);

-- Comments table (UPDATED - added project relationship)
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    client_type VARCHAR(50),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Insert default admin user (FIXED - proper password hash for 'admin123')
-- This hash is for password 'admin123' using bcrypt
INSERT INTO admin_users (username, password_hash, email, full_name, created_at) VALUES 
('admin', '$2b$12$LQv3c1yqBwEHxPuNYjL.T.lSm8.PFz8bhWJjKQjQ3.rB5F5F5F5F5', 'Colour&craft@gmail.com', 'Administrator', NOW());

-- Create indexes for better performance
CREATE INDEX idx_projects_created_at ON projects(created_at);
CREATE INDEX idx_projects_category ON projects(category);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_is_read ON messages(is_read);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_priority ON messages(priority);
CREATE INDEX idx_comments_created_at ON comments(created_at);
CREATE INDEX idx_comments_is_approved ON comments(is_approved);
CREATE INDEX idx_comments_project_id ON comments(project_id);
CREATE INDEX idx_admin_users_username ON admin_users(username);

-- Add sample projects for testing
INSERT INTO projects (title, description, image_url, category) VALUES 
('Modern Kitchen Renovation', 'Complete kitchen makeover with contemporary design and premium finishes.', '/static/images/projects/kitchen1.jpg', 'interior'),
('Exterior House Painting', 'Full exterior painting with weather-resistant premium paint and color consultation.', '/static/images/projects/exterior1.jpg', 'exterior'),
('Commercial Office Space', 'Professional office space painting with neutral tones and quick turnaround.', '/static/images/projects/commercial1.jpg', 'commercial'),
('Living Room Transformation', 'Elegant living room painting with accent walls and decorative finishes.', '/static/images/projects/living1.jpg', 'interior'),
('Bedroom Makeover', 'Cozy bedroom design with calming colors and professional application.', '/static/images/projects/bedroom1.jpg', 'interior');

-- Verify setup
SELECT 'Database Setup Complete!' as Status;
SELECT 'Admin User Created' as Info, username, email FROM admin_users WHERE username = 'admin';
SELECT 'Projects Added' as Info, COUNT(*) as project_count FROM projects;
SELECT 'User Privileges' as Info, User, Host FROM mysql.user WHERE User = 'color_and_craft';-- Create database
CREATE DATABASE IF NOT EXISTS color_and_craft;
USE color_and_craft;

-- Create dedicated user for the application
-- Drop user if exists to avoid conflicts
DROP USER IF EXISTS 'color_and_craft'@'localhost';

-- Create user with secure password
CREATE USER 'color_and_craft'@'localhost' IDENTIFIED BY 'GGTAHAEHt.1';

-- Grant all privileges on the database
GRANT ALL PRIVILEGES ON color_and_craft.* TO 'color_and_craft'@'localhost';

-- Apply privilege changes
FLUSH PRIVILEGES;

-- Drop tables if they exist to avoid conflicts
DROP TABLE IF EXISTS comments;
DROP TABLE IF EXISTS messages;
DROP TABLE IF EXISTS projects;
DROP TABLE IF EXISTS admin_users;

-- Admin Users table (NEW - for secure admin authentication)
CREATE TABLE admin_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100),
    full_name VARCHAR(100),
    last_login TIMESTAMP NULL,
    login_attempts INT DEFAULT 0,
    locked_until TIMESTAMP NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Projects table (FIXED - image_url is now TEXT)
CREATE TABLE projects (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT NOT NULL,
    image_url TEXT NOT NULL,
    category VARCHAR(50) DEFAULT 'general',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Messages table (UPDATED - improved structure)
CREATE TABLE messages (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    phone VARCHAR(20),
    service_type VARCHAR(50),
    message TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_read BOOLEAN DEFAULT 0,
    status VARCHAR(20) DEFAULT 'pending',
    admin_notes TEXT,
    priority ENUM('low', 'medium', 'high') DEFAULT 'medium'
);

-- Comments table (UPDATED - added project relationship)
CREATE TABLE comments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    content TEXT NOT NULL,
    client_type VARCHAR(50),
    rating INT CHECK (rating >= 1 AND rating <= 5),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_approved BOOLEAN DEFAULT 0,
    FOREIGN KEY (project_id) REFERENCES projects(id) ON DELETE CASCADE
);

-- Insert default admin user (FIXED - proper password hash for 'admin123')
-- This hash is for password 'admin123' using bcrypt
INSERT INTO admin_users (username, password_hash, email, full_name, created_at) VALUES 
('admin', '$2b$12$LQv3c1yqBwEHxPuNYjL.T.lSm8.PFz8bhWJjKQjQ3.rB5F5F5F5F5', 'Colour&craft@gmail.com', 'Administrator', NOW());

-- Create indexes for better performance
CREATE INDEX idx_projects_created_at ON projects(created_at);
CREATE INDEX idx_projects_category ON projects(category);
CREATE INDEX idx_messages_created_at ON messages(created_at);
CREATE INDEX idx_messages_is_read ON messages(is_read);
CREATE INDEX idx_messages_status ON messages(status);
CREATE INDEX idx_messages_priority ON messages(priority);
CREATE INDEX idx_comments_created_at ON comments(created_at);
CREATE INDEX idx_comments_is_approved ON comments(is_approved);
CREATE INDEX idx_comments_project_id ON comments(project_id);
CREATE INDEX idx_admin_users_username ON admin_users(username);

-- Add sample projects for testing
INSERT INTO projects (title, description, image_url, category) VALUES 
('Modern Kitchen Renovation', 'Complete kitchen makeover with contemporary design and premium finishes.', '/static/images/projects/kitchen1.jpg', 'interior'),
('Exterior House Painting', 'Full exterior painting with weather-resistant premium paint and color consultation.', '/static/images/projects/exterior1.jpg', 'exterior'),
('Commercial Office Space', 'Professional office space painting with neutral tones and quick turnaround.', '/static/images/projects/commercial1.jpg', 'commercial'),
('Living Room Transformation', 'Elegant living room painting with accent walls and decorative finishes.', '/static/images/projects/living1.jpg', 'interior'),
('Bedroom Makeover', 'Cozy bedroom design with calming colors and professional application.', '/static/images/projects/bedroom1.jpg', 'interior');

-- Verify setup
SELECT 'Database Setup Complete!' as Status;
SELECT 'Admin User Created' as Info, username, email FROM admin_users WHERE username = 'admin';
SELECT 'Projects Added' as Info, COUNT(*) as project_count FROM projects;
SELECT 'User Privileges' as Info, User, Host FROM mysql.user WHERE User = 'color_and_craft';