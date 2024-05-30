CREATE DATABASE Interns;
CREATE TABLE Biodata
    (
        Matric_Number VARCHAR(25) NOT NULL,
        First_Name VARCHAR(80),
        Last_Name VARCHAR(80) NOT NULL,
        Gender VARCHAR(7) NOT NULL DEFAULT 'Male',
        Institution TEXT NOT NULL,
        Course_of_Study VARCHAR(150) NOT NULL DEFAULT 'Computer Science',
        Email VARCHAR(80) NOT NULL UNIQUE KEY,
        Phone_Number VARCHAR(9) NOT NULL UNIQUE KEY,
        PRIMARY KEY(Matric_Number)
    );
