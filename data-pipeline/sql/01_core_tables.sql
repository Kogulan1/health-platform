USE health_platform_dev;
GO

-- USERS TABLE
CREATE TABLE users (
    user_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    full_name NVARCHAR(100),
    email NVARCHAR(150) UNIQUE,
    date_of_birth DATE,
    gender VARCHAR(10),
    country VARCHAR(50),
    registration_date DATETIME DEFAULT GETDATE(),
    consent_to_data BIT DEFAULT 0,
    consent_to_trials BIT DEFAULT 0,
    is_active BIT DEFAULT 1
);

-- AUTH PROVIDERS
CREATE TABLE auth_providers (
    provider_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES users(user_id),
    provider_type VARCHAR(30),
    provider_user_id VARCHAR(255),
    email NVARCHAR(150),
    is_primary BIT DEFAULT 0,
    linked_at DATETIME DEFAULT GETDATE()
);

-- USER DEVICES
CREATE TABLE user_devices (
    device_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES users(user_id),
    platform VARCHAR(10),
    model VARCHAR(100),
    os_version VARCHAR(50),
    app_version VARCHAR(20),
    last_sync_time DATETIME
);

-- USER PREFERENCES
CREATE TABLE user_preferences (
    user_id UNIQUEIDENTIFIER PRIMARY KEY FOREIGN KEY REFERENCES users(user_id),
    prefers_notifications BIT DEFAULT 1,
    language VARCHAR(10) DEFAULT 'en',
    dark_mode_enabled BIT DEFAULT 0,
    marketing_opt_in BIT DEFAULT 0
);

-- RAW HEALTH EVENTS
CREATE TABLE raw_health_events (
    event_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES users(user_id),
    platform VARCHAR(10),
    device_model VARCHAR(100),
    timestamp DATETIME,
    data_type VARCHAR(50),
    value_numeric FLOAT,
    value_string VARCHAR(100),
    unit VARCHAR(20),
    metadata NVARCHAR(MAX),
    ingestion_time DATETIME DEFAULT GETDATE()
);

-- CONSENT LOGS
CREATE TABLE consent_logs (
    log_id UNIQUEIDENTIFIER PRIMARY KEY DEFAULT NEWID(),
    user_id UNIQUEIDENTIFIER FOREIGN KEY REFERENCES users(user_id),
    consent_type VARCHAR(30),
    status BIT,
    timestamp DATETIME DEFAULT GETDATE(),
    source VARCHAR(30)
);
