create database ccyt_salas
go
use ccyt_salas
go
CREATE TABLE Salas (
    id_sala INT PRIMARY KEY,
    nombre NVARCHAR(50),
    division NVARCHAR(50),
    num_computadoras INT
);

CREATE TABLE Docentes (
    clave_docente NVARCHAR(20) PRIMARY KEY,
    nombre NVARCHAR(100),
    correo NVARCHAR(100)
);

CREATE TABLE Materias (
    id_materia INT PRIMARY KEY,
    nombre NVARCHAR(100),
    division NVARCHAR(50)
);

CREATE TABLE Clases (
    id_clase INT PRIMARY KEY IDENTITY,
    id_sala INT FOREIGN KEY REFERENCES Salas(id_sala),
    id_materia INT FOREIGN KEY REFERENCES Materias(id_materia),
    fecha DATE,
    horario NVARCHAR(20),
    grupo NVARCHAR(20),
    clave_docente NVARCHAR(20) FOREIGN KEY REFERENCES Docentes(clave_docente),
    cambio_sala BIT,
    prestamo_sala BIT,
    recurso NVARCHAR(50),
    software NVARCHAR(100)
);

CREATE TABLE Alumnos (
    matricula NVARCHAR(20) PRIMARY KEY,
    nombre NVARCHAR(100)
);

CREATE TABLE Asistencias (
    id_asistencia INT PRIMARY KEY IDENTITY,
    id_clase INT FOREIGN KEY REFERENCES Clases(id_clase),
    matricula NVARCHAR(20) FOREIGN KEY REFERENCES Alumnos(matricula),
    equipo NVARCHAR(50),
    observaciones NVARCHAR(200)
);
