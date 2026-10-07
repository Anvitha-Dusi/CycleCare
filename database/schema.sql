-- ============================================================================
-- CycleCare Database Schema
-- Database: MySQL 8.0+
-- Description: Stores user accounts and menstrual cycle records with 
--              relational integrity and indexed lookups.
-- ============================================================================

CREATE DATABASE IF NOT EXISTS cyclecare_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;

USE cyclecare_db;

-- ----------------------------------------------------------------------------
-- Table: users
-- Purpose: Stores registered user credentials and profile metadata.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email)
) ENGINE=InnoDB;

-- ----------------------------------------------------------------------------
-- Table: cycles
-- Purpose: Stores individual menstrual cycle records per user.
-- Foreign Key: user_id references users(id) with CASCADE on delete.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS cycles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NULL,
    period_duration INT NOT NULL,
    cycle_length INT NOT NULL,
    notes TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_cycles_user
        FOREIGN KEY (user_id) REFERENCES users(id)
        ON DELETE CASCADE,
    INDEX idx_user_start_date (user_id, start_date DESC)
) ENGINE=InnoDB;
