-- Colleges table
CREATE TABLE IF NOT EXISTS Colleges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    location TEXT NOT NULL,
    overall_score REAL,
    naac_grade TEXT
);

-- Departments table
CREATE TABLE IF NOT EXISTS Departments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    department_name TEXT NOT NULL,
    head TEXT,
    description TEXT,
    FOREIGN KEY (college_id) REFERENCES Colleges(id) ON DELETE CASCADE
);

-- Inspections table
CREATE TABLE IF NOT EXISTS Inspections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    college_id INTEGER NOT NULL,
    inspection_date TEXT,
    inspector TEXT,
    remarks TEXT,
    FOREIGN KEY (college_id) REFERENCES Colleges(id) ON DELETE CASCADE
);

-- Criteria table
CREATE TABLE IF NOT EXISTS Criteria (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    criterion_name TEXT NOT NULL,
    max_score REAL,
    description TEXT
);

-- Inspection_Ratings table
CREATE TABLE IF NOT EXISTS Inspection_Ratings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    inspection_id INTEGER NOT NULL,
    criterion_id INTEGER NOT NULL,
    score REAL,
    remarks TEXT,
    FOREIGN KEY (inspection_id) REFERENCES Inspections(id) ON DELETE CASCADE,
    FOREIGN KEY (criterion_id) REFERENCES Criteria(id) ON DELETE CASCADE
);