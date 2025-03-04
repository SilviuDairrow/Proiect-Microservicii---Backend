CREATE TABLE PROFESORI (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(40) NOT NULL,
    prenume VARCHAR(70) NOT NULL,
    email VARCHAR(140) UNIQUE NOT NULL,
    grad_didactic ENUM('asist', 'sef_lucr', 'conf', 'prof'),
    tip_asociere ENUM('titular', 'asociat', 'extern') NOT NULL,
    afiliere VARCHAR(70)
);

CREATE TABLE DISCIPLINE (
    COD VARCHAR(10) PRIMARY KEY,
    ID_titular INT NOT NULL,
    nume_disciplina VARCHAR(100) NOT NULL,
    an_studiu INT NOT NULL,
    tip_disciplina ENUM('impusa', 'optionala', 'liber_aleasa') NOT NULL,
    categorie_disciplina ENUM('domeniu', 'specialitate', 'adiacenta') NOT NULL,
    tip_examinare ENUM('examen', 'colocviu') NOT NULL,
    FOREIGN KEY (ID_titular) REFERENCES PROFESORI(ID)
);

CREATE TABLE STUDENTI (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    nume VARCHAR(40) NOT NULL,
    prenume VARCHAR(70) NOT NULL,
    email VARCHAR(140) UNIQUE NOT NULL,
    ciclu_studii ENUM('licenta', 'master') NOT NULL,
    an_studiu INT NOT NULL,
    grupa INT NOT NULL
);

CREATE TABLE JOIN_DS (
    DisciplinaID VARCHAR(10),
    StudentID INT,
    PRIMARY KEY (DisciplinaID, StudentID),
    FOREIGN KEY (DisciplinaID) REFERENCES DISCIPLINE(COD),
    FOREIGN KEY (StudentID) REFERENCES STUDENTI(ID)
);
