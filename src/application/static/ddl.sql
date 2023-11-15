-- Table Definitions (DDL)

CREATE TABLE users (
    id serial PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    active BOOLEAN NOT NULL
);

-- Add comments to describe tables and columns
COMMENT ON TABLE users IS 'Table to store user information';
COMMENT ON COLUMN users.id IS 'Unique user ID';
COMMENT ON COLUMN users.username IS 'User''s username';
COMMENT ON COLUMN users.password IS 'Hashed user password';
COMMENT ON COLUMN users.email IS 'User''s email address';
COMMENT ON COLUMN users.active IS 'User''s active status';

CREATE TABLE roles (
    id serial PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    identifier VARCHAR(50) NOT NULL
);

-- Add comments to describe tables and columns
COMMENT ON TABLE roles IS 'Table to store user roles';
COMMENT ON COLUMN roles.id IS 'Unique role ID';
COMMENT ON COLUMN roles.name IS 'Role name';
COMMENT ON COLUMN roles.identifier IS 'Role identifier (short name or slug)';

CREATE TABLE user_roles (
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER REFERENCES roles(id) ON DELETE CASCADE,
    PRIMARY KEY (user_id, role_id)
);

-- Add comments to describe tables and columns
COMMENT ON TABLE user_roles IS 'Table to establish relationships between users and roles';
COMMENT ON COLUMN user_roles.user_id IS 'User ID';
COMMENT ON COLUMN user_roles.role_id IS 'Role ID';

CREATE TABLE providers (
    id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country_codes VARCHAR(2)[]
);

-- Add comments to describe tables and columns
COMMENT ON TABLE providers IS 'Table to store information about risk providers';
COMMENT ON COLUMN providers.id IS 'Unique provider ID';
COMMENT ON COLUMN providers.name IS 'Provider name';
COMMENT ON COLUMN providers.country_codes IS 'Array of country codes associated with the provider';

-- Sample Data Insertion (DML)
-- Insert user roles, and other data as needed

CREATE TABLE risks (
    id serial PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    impact INTEGER,
    probability INTEGER,
    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
    provider_id INTEGER REFERENCES providers(id) ON DELETE CASCADE,
    country_code VARCHAR(2) NOT NULL
);

-- Add comments to describe tables and columns
COMMENT ON TABLE risks IS 'Table to store information about cybersecurity risks';
COMMENT ON COLUMN risks.id IS 'Unique risk ID';
COMMENT ON COLUMN risks.title IS 'Risk title';
COMMENT ON COLUMN risks.description IS 'Risk description';
COMMENT ON COLUMN risks.impact IS 'Risk impact';
COMMENT ON COLUMN risks.probability IS 'Risk probability';
COMMENT ON COLUMN risks.user_id IS 'User who created the risk';
COMMENT ON COLUMN risks.country_code IS 'Country code associated with the risk';

CREATE TABLE risk_treatments (
    id serial PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description VARCHAR(500) NOT NULL,
    constraints VARCHAR(200) NOT NULL,
    start_date TIMESTAMP,
    final_date TIMESTAMP,
    risk_id INTEGER REFERENCES risks(id) ON DELETE CASCADE
);

-- Add comments to describe tables and columns
COMMENT ON TABLE risk_treatments IS 'Table to store information about the treatment of cybersecurity risks';
COMMENT ON COLUMN risk_treatments.id IS 'Unique risk treatment ID';
COMMENT ON COLUMN risk_treatments.name IS 'Name of the risk treatment';
COMMENT ON COLUMN risk_treatments.description IS 'Detailed description of the risk treatment';
COMMENT ON COLUMN risk_treatments.constraints IS 'Constraints or limitations associated with the risk treatment';
COMMENT ON COLUMN risk_treatments.start_date IS 'Start date of the risk treatment implementation';
COMMENT ON COLUMN risk_treatments.final_date IS 'End date of the risk treatment implementation';
COMMENT ON COLUMN risk_treatments.risk_id IS 'ID of the associated risk in the risks table';
