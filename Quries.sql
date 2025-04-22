--  Create Database
CREATE DATABASE Cloud_Storages_Management;
USE Cloud_Storages_Management;

-- 1. Users Table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT ,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Admin', 'user') NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Folders Table
CREATE TABLE Folders (
    folder_id INT PRIMARY KEY AUTO_INCREMENT,
    folder_name VARCHAR(100) NOT NULL,
    parent_folder_id INT,
    created_by INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (parent_folder_id) REFERENCES Folders(folder_id) ON DELETE SET NULL,
    FOREIGN KEY (created_by) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 3. Files Table
CREATE TABLE Files (
    file_id INT PRIMARY KEY AUTO_INCREMENT,
    file_name VARCHAR(100) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size BIGINT NOT NULL,
    file_url TEXT NOT NULL,
    uploaded_by INT NOT NULL,
    parent_folder_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_deleted BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (uploaded_by) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_folder_id) REFERENCES Folders(folder_id) ON DELETE SET NULL
);

-- 4. FileSharing Table
CREATE TABLE FileSharing (
    share_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    shared_with INT NOT NULL,
    access_level ENUM('View', 'Edit', 'Download') NOT NULL,
    shared_by INT NOT NULL,
    shared_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES Files(file_id) ON DELETE CASCADE,
    FOREIGN KEY (shared_with) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (shared_by) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 5. FileVersions Table
CREATE TABLE FileVersions (
    version_id INT PRIMARY KEY AUTO_INCREMENT,
    file_id INT NOT NULL,
    version_number INT NOT NULL,
    file_url TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (file_id) REFERENCES Files(file_id) ON DELETE CASCADE
);

-- Insert into Users Table
INSERT INTO Users (user_id, username, email, password, role) VALUES
(100,'abdul_rahman', 'abdul_rahman@gmail.com', '1112Abdulawan', 'Admin'),
(101,'khiyam', 'khiyam_bin_khalid@gmail.com', 'khiyam_012', 'user'),
(102,'muzzamal', 'muzzamal_kiyani@gmail.com', 'muzzamal_006', 'Admin'),
(103,'ehtsham', 'ehtsham_shami@gmail.com', 'shami_001', 'user'),
(104,'usman_ghani', 'usman_chishti@gmail.com', 'chishti_010', 'user');

-- Insert into Folders Table
INSERT INTO Folders (folder_id, folder_name, parent_folder_id, created_by) VALUES
(10,'Root _Folder', NULL, 1),           -- Root folder by abdul
(11,'Course', 10, 2),                     -- Course folder by khiyam 
(12,'Assignments', 10, 2),                -- Assignments folder by muzzamil 
(13,'Student_Projects', 10, 3),           -- Project folder by ehtsham
(14,'Research',10, 5);                    -- Research folder by usman 

-- Insert into Files Table
INSERT INTO Files (file_id, file_name, file_type, file_size, file_url, uploaded_by, parent_folder_id, is_deleted) VALUES
(20,'syllabus.pdf', 'PDF', 524288, 'https://cloud_storage.com/files/syllabus.pdf', 101, 10, FALSE),
(21,'homework1.docx', 'DOCX', 1048576, 'https://cloud_storage.com/files/homework1.docx', 101, 11, FALSE),
(22,'project_proposal.pdf', 'PDF', 2097152, 'https://cloud_storage.com/files/proposal.pdf', 103, 12, FALSE),
(23,'lecture_notes.pptx', 'PPTX', 5242880, 'https://cloud_storage.com/files/notes.pptx', 103, 13, FALSE),
(24,'old_exam.pdf', 'PDF', 3145728, 'https://cloud_storage.com/files/old_exam.pdf', 104, 14, TRUE);

-- Insert into FileSharing Table
INSERT INTO FileSharing (file_id, shared_with, access_level, shared_by) VALUES
(20, 102, 'View', 2),        -- Syllabus shared with  muzzamal (View)
(20, 103, 'View', 2),        -- Syllabus shared with ehtsham (View)
(21, 101, 'Edit', 3),        -- Homework shared with khiyam (Edit)
(22, 103, 'Download', 3),    -- Project proposal shared with ehtsham (Download)
(23, 100, 'View', 5);        -- Lecture notes shared with abdul (View)

-- Insert into FileVersions Table
INSERT INTO FileVersions (file_id, version_number, file_url, created_at) VALUES
(10, 1, 'https://cloud.university.edu/files/syllabus_v1.pdf', '2025-01-10 10:00:00'),
(10, 2, 'https://cloud.university.edu/files/syllabus_v2.pdf', '2025-02-15 12:00:00'),
(11, 1, 'https://cloud.university.edu/files/homework1_v1.docx', '2025-03-01 09:00:00'),
(12, 1, 'https://cloud.university.edu/files/proposal_v1.pdf', '2025-03-10 14:00:00'),
(14, 1, 'https://cloud.university.edu/files/notes_v1.pptx', '2025-04-01 16:00:00');
  
USE Cloud_Storages_Management; 
select*from users;
USE Cloud_Storages_Management;
DELETE from users where user_id=104;

