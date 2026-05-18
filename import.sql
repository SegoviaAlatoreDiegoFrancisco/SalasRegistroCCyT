create database ccyt_salas
go
use ccyt_salas
CREATE TABLE [dbo].[Alumnos](
	[matricula] [nvarchar](20) NOT NULL,
	[nombre] [nvarchar](100) NULL,
	[activo] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[matricula] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Asistencias]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Asistencias](
	[id_asistencia] [int] IDENTITY(1,1) NOT NULL,
	[id_clase] [int] NULL,
	[matricula] [nvarchar](20) NULL,
	[equipo] [nvarchar](50) NULL,
	[observaciones] [nvarchar](200) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_asistencia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Clases]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Clases](
	[id_clase] [int] IDENTITY(1,1) NOT NULL,
	[id_sala] [int] NULL,
	[id_materia] [int] NULL,
	[fecha] [date] NULL,
	[horario] [nvarchar](20) NULL,
	[grupo] [nvarchar](20) NULL,
	[clave_docente] [nvarchar](20) NULL,
	[cambio_sala] [bit] NULL,
	[prestamo_sala] [bit] NULL,
	[recurso] [nvarchar](50) NULL,
	[software] [nvarchar](100) NULL,
PRIMARY KEY CLUSTERED 
(
	[id_clase] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Docentes]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Docentes](
	[clave_docente] [nvarchar](20) NOT NULL,
	[nombre] [nvarchar](100) NULL,
	[correo] [nvarchar](100) NULL,
	[activo] [bit] NULL,
PRIMARY KEY CLUSTERED 
(
	[clave_docente] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Materias]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Materias](
	[id_materia] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](100) NULL,
	[division] [nvarchar](50) NULL,
 CONSTRAINT [PK__Materias__7E03FD39517EDBB6] PRIMARY KEY CLUSTERED 
(
	[id_materia] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Salas]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Salas](
	[id_sala] [int] IDENTITY(1,1) NOT NULL,
	[nombre] [nvarchar](50) NULL,
	[division] [nvarchar](50) NULL,
	[num_computadoras] [int] NULL,
 CONSTRAINT [PK__Salas__D18B015B89C6FB62] PRIMARY KEY CLUSTERED 
(
	[id_sala] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[Users]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Users](
	[id] [int] IDENTITY(1,1) NOT NULL,
	[name] [nvarchar](100) NULL,
	[email] [nvarchar](100) NULL,
	[password] [nvarchar](200) NULL,
	[rol] [nchar](10) NULL,
 CONSTRAINT [PK__Users__3213E83F19BF0728] PRIMARY KEY CLUSTERED 
(
	[id] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Alumnos] ADD  CONSTRAINT [DF_Alumnos_matricula]  DEFAULT ((1)) FOR [matricula]
GO
ALTER TABLE [dbo].[Alumnos] ADD  CONSTRAINT [DF_Alumnos_activo]  DEFAULT ((1)) FOR [activo]
GO
ALTER TABLE [dbo].[Docentes] ADD  CONSTRAINT [DF_Docentes_activo]  DEFAULT ((1)) FOR [activo]
GO
ALTER TABLE [dbo].[Asistencias]  WITH CHECK ADD FOREIGN KEY([id_clase])
REFERENCES [dbo].[Clases] ([id_clase])
GO
ALTER TABLE [dbo].[Asistencias]  WITH CHECK ADD FOREIGN KEY([matricula])
REFERENCES [dbo].[Alumnos] ([matricula])
GO
ALTER TABLE [dbo].[Clases]  WITH CHECK ADD FOREIGN KEY([clave_docente])
REFERENCES [dbo].[Docentes] ([clave_docente])
GO
ALTER TABLE [dbo].[Clases]  WITH CHECK ADD  CONSTRAINT [FK__Clases__id_mater__3D5E1FD2] FOREIGN KEY([id_materia])
REFERENCES [dbo].[Materias] ([id_materia])
GO
ALTER TABLE [dbo].[Clases] CHECK CONSTRAINT [FK__Clases__id_mater__3D5E1FD2]
GO
ALTER TABLE [dbo].[Clases]  WITH CHECK ADD  CONSTRAINT [FK__Clases__id_sala__3C69FB99] FOREIGN KEY([id_sala])
REFERENCES [dbo].[Salas] ([id_sala])
GO
ALTER TABLE [dbo].[Clases] CHECK CONSTRAINT [FK__Clases__id_sala__3C69FB99]
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNO_ACTIVAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[SP_ALUMNO_ACTIVAR]
	@MATRICULA AS NVARCHAR(100)
AS
BEGIN
UPDATE Alumnos
SET          activo = 1
WHERE  (matricula = @MATRICULA)
SELECT 'Alumno fue dado de baja' AS 'Resultado'
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNO_CONSULTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_ALUMNO_CONSULTAR]
	@MATRICULA AS NVARCHAR(100)
AS
BEGIN
SELECT matricula, nombre, activo
FROM     Alumnos
WHERE  (matricula = @MATRICULA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNO_ELIMINAR_BAJA_LOGICA]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_ALUMNO_ELIMINAR_BAJA_LOGICA]
	@MATRICULA AS NVARCHAR(100)
AS
BEGIN
UPDATE Alumnos
SET          activo = 0
WHERE  (matricula = @MATRICULA)
SELECT 'Alumno fue dado de baja' AS 'Resultado'
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNO_INSERTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_ALUMNO_INSERTAR]
	@NOMBRE AS NVARCHAR(100)
	,@MATRICULA AS NVARCHAR(100)
AS
BEGIN
--INICIO Validación de que no exista el mismo usuario con matricula y nombre duplicados
if exists (SELECT matricula, nombre
FROM     Alumnos
WHERE  (matricula = @MATRICULA) AND (nombre = @NOMBRE))

	BEGIN
		select 'El usuario con esos datos ya existe, verifica los campos' AS 'Resultado'
		return (-1)
	END
--FIN Validación de que no exista el mismo usuario con matricula y nombre duplicados
--INICIO Validacion de un usuario con registrado con la matricula dada
if exists (SELECT matricula
FROM     Alumnos
WHERE  (matricula = @MATRICULA))
	BEGIN
		select 'El usuario con esa matricula ya existe, verifica los campos' AS 'Resultado'
		return (-1)
	END
--FIN Validacion de un usuario con registrado con la matricula dada
INSERT INTO Alumnos
                  (matricula, nombre)
VALUES (@MATRICULA,@NOMBRE)
SELECT 'Alumno registrado correctamente' AS 'Resultado'
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNO_MODIFICAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_ALUMNO_MODIFICAR]
	@MATRICULA AS NVARCHAR(100)
	,@NOMBRE AS NVARCHAR(100)
	,@ACTIVO AS BIT
AS
BEGIN
	UPDATE Alumnos
SET          nombre = @NOMBRE, activo = @ACTIVO
WHERE  (matricula = @MATRICULA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNOS_LISTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_ALUMNOS_LISTAR]

AS
BEGIN
SELECT matricula, nombre
FROM     Alumnos
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNOS_LISTAR_ACTIVOS]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[SP_ALUMNOS_LISTAR_ACTIVOS]

AS
BEGIN
SELECT matricula, nombre
FROM     Alumnos
WHERE  (activo = 1)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_ALUMNOS_LISTAR_INACTIVOS]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO


CREATE     PROCEDURE [dbo].[SP_ALUMNOS_LISTAR_INACTIVOS]

AS
BEGIN
SELECT matricula, nombre
FROM     Alumnos
WHERE  (activo = 0)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTE_ACTIVAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTE_ACTIVAR]
	@CLAVE_DOCENTE AS NVARCHAR(20)
AS
BEGIN
UPDATE Docentes
SET          activo = 1
WHERE  (clave_docente = @CLAVE_DOCENTE)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTE_CONSULTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTE_CONSULTAR]
	@CLAVE_DOCENTE AS NVARCHAR(20)
AS
BEGIN
SELECT nombre, correo, clave_docente, activo
FROM     Docentes
WHERE  (clave_docente = @CLAVE_DOCENTE)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTE_ELIMINAR_BAJA_LOGICA]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTE_ELIMINAR_BAJA_LOGICA]
	@CLAVE_DOCENTE AS NVARCHAR(20)
AS
BEGIN
UPDATE Docentes
SET          activo = 0
WHERE  (clave_docente = @CLAVE_DOCENTE)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTE_INSERTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTE_INSERTAR]
	@CLAVE_DOCENTE AS NVARCHAR(20)
	,@NOMBRE AS NVARCHAR(100)
	,@CORREO AS NVARCHAR(100)
AS
BEGIN
IF EXISTS (SELECT clave_docente, nombre, correo
			FROM     Docentes
			WHERE  (clave_docente = @CLAVE_DOCENTE) AND (nombre = @NOMBRE) AND (correo = @CORREO)
			)
BEGIN
	SELECT 'El docente con esos datos ya existe, favor de verificar los campos' as 'Result'
	RETURN (-1)
END
IF EXISTS (SELECT correo
			FROM     Docentes
			WHERE  (correo = @CORREO)
			)
BEGIN
	SELECT 'El correo ya está ligado a un docente, favor de verfivar los datos'
	RETURN (-1)
END
INSERT INTO Docentes(clave_docente, nombre, correo)
		VALUES (@CLAVE_DOCENTE,@NOMBRE,@CORREO)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTE_MODIFICAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTE_MODIFICAR]
	@CLAVE_DOCENTE AS NVARCHAR(20)
	,@NOMBRE AS NVARCHAR(100)
	,@CORREO AS NVARCHAR(100)
	,@ESTADO AS BIT
AS
BEGIN
UPDATE Docentes
SET          nombre = @NOMBRE, correo = @CORREO, activo = @ESTADO
WHERE  (clave_docente = @CLAVE_DOCENTE)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTES_ACTIVOS_LISTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_DOCENTES_ACTIVOS_LISTAR]

AS
BEGIN
SELECT clave_docente, nombre, correo
FROM     Docentes
WHERE  (activo = 1)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_DOCENTES_INACTIVOS_LISTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO

CREATE   PROCEDURE [dbo].[SP_DOCENTES_INACTIVOS_LISTAR]

AS
BEGIN
SELECT clave_docente, nombre, correo
FROM     Docentes
WHERE  (activo = 0)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_MATERIA_CONSULTA]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_MATERIA_CONSULTA]
	@ID_MATERIA as NVARCHAR(100)
AS
BEGIN
SELECT        id_materia, nombre, division
FROM            Materias
WHERE        (id_materia = @ID_MATERIA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_MATERIA_ELIMINAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_MATERIA_ELIMINAR]
	@ID_MATERIA AS NVARCHAR(20)
AS
BEGIN
	DELETE FROM Materias
WHERE        (id_materia = @ID_MATERIA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_MATERIA_INSERTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_MATERIA_INSERTAR]
	@NOMBRE AS NVARCHAR(100)
	,@DIVISION AS NVARCHAR(50)
AS
BEGIN
IF EXISTS (SELECT        nombre, division
			FROM            Materias
			WHERE        (nombre = @NOMBRE) AND (division = @DIVISION))
BEGIN
	select 'Materia registrada con el mismo nombre y la misma division'
	return (-1)
	
END

INSERT INTO Materias
                         (nombre, division)
VALUES        (@NOMBRE,@DIVISION)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_MATERIAS_LISTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_MATERIAS_LISTAR]
AS
BEGIN
SELECT        id_materia, nombre, division
FROM            Materias
END
GO
/****** Object:  StoredProcedure [dbo].[SP_SALA_CONSULTA]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_SALA_CONSULTA]
	@ID_SALA AS INT 
AS
BEGIN
SELECT        id_sala, nombre, division, num_computadoras
FROM            Salas
WHERE        (id_sala = @ID_SALA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_SALA_MODIFICAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_SALA_MODIFICAR]
	@ID_SALA AS INT
	,@NOMBRE AS NVARCHAR(100)
	,@DIVISION AS NVARCHAR(100)
	,@NUM_COMPUTADORAS AS NVARCHAR(100)

AS
BEGIN
UPDATE       Salas
SET                nombre = @NOMBRE, division = @DIVISION, num_computadoras = num_computadoras
WHERE        (id_sala = @ID_SALA)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_SALAS_INSERTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_SALAS_INSERTAR] 
	@NOMBRE AS NVARCHAR(50)
	,@DIVISION AS NVARCHAR(50)
	,@NUM_COMPUTADORAS AS INT
AS
BEGIN
IF EXISTS(SELECT        nombre, division
			FROM            Salas	
			WHERE        (nombre = @NOMBRE) AND (division = @DIVISION))
	BEGIN
	SELECT 'Sala ya está registrada, por favor verifique los datos'
	RETURN(-1)
	END
INSERT INTO Salas
                         (nombre, division, num_computadoras)
VALUES        (@NOMBRE,@DIVISION,@NUM_COMPUTADORAS)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_SALAS_LISTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_SALAS_LISTAR]
	
AS
BEGIN
SELECT        id_sala, nombre, division, num_computadoras
FROM            Salas
END
GO
/****** Object:  StoredProcedure [dbo].[SP_USUARIO_AUTENTICAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_USUARIO_AUTENTICAR]
	@EMAIL AS NVARCHAR(100)
AS
BEGIN
SELECT        email, password, rol, name
FROM            Users
WHERE        (email = @EMAIL)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_USUARIO_INSERTAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_USUARIO_INSERTAR]
	@NAME AS NVARCHAR(100)
	,@EMAIL AS NVARCHAR(100)
	,@PASSWORD AS NVARCHAR(200)
	,@ROL AS NVARCHAR(100)
AS
BEGIN
IF exists (SELECT name, email
	FROM     Users
	WHERE  (name = @NAME) AND (email = @EMAIL)
	)
	BEGIN
	SELECT 'El usuaio ya fue ingresado en la base de datos' as resultado
	RETURN (-1)
	END
INSERT INTO Users
                         (name, email, password, rol)
VALUES        (@NAME,@EMAIL,@PASSWORD,@ROL)
END
GO
/****** Object:  StoredProcedure [dbo].[SP_USUARIOS_BUSCAR]    Script Date: 16/05/2026 12:48:12 p. m. ******/
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE PROCEDURE [dbo].[SP_USUARIOS_BUSCAR]
AS
BEGIN
SELECT id, name, email
FROM     Users
END
GO
USE [master]
GO
ALTER DATABASE [ccyt_salas] SET  READ_WRITE 
GO
