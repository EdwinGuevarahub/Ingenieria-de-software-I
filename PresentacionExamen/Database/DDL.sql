-- Tabla Estudiantes
CREATE TABLE Estudiantes (
    cod_estudiante BIGINT PRIMARY KEY,           -- Código único del estudiante (clave primaria)
    nom_estudiante VARCHAR(50) NOT NULL,      -- Nombre del estudiante
    dir_estudiante VARCHAR(50) NOT NULL,      -- Dirección del estudiante
    tel_estudiante CHAR(10) NOT NULL,         -- Teléfono del estudiante
    cod_carrera INT NOT NULL,                 -- Código de la carrera
    fecha_nacimiento DATE NOT NULL            -- Fecha de nacimiento
);

-- Tabla Asignaturas
CREATE TABLE Asignaturas (
    cod_asignatura INT PRIMARY KEY,           -- Código único de la asignatura (clave primaria)
    nom_asignatura VARCHAR(50) NOT NULL,      -- Nombre de la asignatura
    inten_horaria SMALLINT NOT NULL CHECK (inten_horaria > 0),  -- Intensidad horaria
    credit_asignatura SMALLINT NOT NULL CHECK (credit_asignatura > 0)  -- Créditos de la asignatura
);

-- Tabla Profesores
CREATE TABLE Profesores (
    cod_profesor INT PRIMARY KEY,             -- Código único del profesor (clave primaria)
    nom_profesor VARCHAR(50) NOT NULL,        -- Nombre del profesor
    profesion VARCHAR(50) NOT NULL,           -- Profesión
    niv_escolaridad VARCHAR(50) NOT NULL      -- Nivel de escolaridad
);

-- Tabla Salones
CREATE TABLE Salones (
    id_salon SERIAL PRIMARY KEY,              -- Identificador del salón
    capacidad SMALLINT NOT NULL CHECK (capacidad BETWEEN 10 AND 40)  -- Capacidad entre 10 y 40
);

-- Tabla Tipos de Preguntas
CREATE TABLE TiposPreguntas (
    id_tipo_pregunta INT PRIMARY KEY,      -- Identificador del tipo de pregunta
    nombre_tipo VARCHAR(50) NOT NULL UNIQUE   -- Nombre del tipo de pregunta
);

-- Tabla Preguntas
CREATE TABLE Preguntas (
    id_pregunta SERIAL PRIMARY KEY,                       -- Identificador de la pregunta
    desc_pregunta TEXT NOT NULL CHECK (LENGTH(desc_pregunta) <= 500),  -- Descripción
    tipo_pregunta INT NOT NULL REFERENCES TiposPreguntas(id_tipo_pregunta)  -- Tipo de pregunta
);

-- Tabla Respuestas
CREATE TABLE Respuestas (
    id_respuesta SERIAL PRIMARY KEY,
    desc_respuesta VARCHAR(150) NOT NULL  -- Descripción de la respuesta
);

-- Relaciones
-- Relación Cursa (Relación Estudiantes - Asignaturas)
CREATE TABLE Cursa (
    cod_estudiante BIGINT NOT NULL REFERENCES Estudiantes(cod_estudiante),
    cod_asignatura INT NOT NULL REFERENCES Asignaturas(cod_asignatura),
    PRIMARY KEY (cod_estudiante, cod_asignatura)  -- Llave compuesta
);

-- Relación Imparte (Profesores - Asignaturas - Grupo)
CREATE TABLE Imparte (
    cod_profesor INT NOT NULL,
    cod_asignatura INT NOT NULL,
    grupo SMALLINT NOT NULL, -- Grupo específico de la asignatura
    horario VARCHAR(50) NOT NULL, -- Horario en texto, máximo 50 caracteres
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo),
    FOREIGN KEY (cod_profesor) REFERENCES Profesores(cod_profesor),
    FOREIGN KEY (cod_asignatura) REFERENCES Asignaturas(cod_asignatura)
);

-- Tabla Corresponde (Relación Preguntas - Respuestas)
CREATE TABLE Corresponde (
    id_pregunta INT NOT NULL REFERENCES Preguntas(id_pregunta),
    id_respuesta INT NOT NULL REFERENCES Respuestas(id_respuesta),
    correcta BOOLEAN NOT NULL,  -- Indica si la respuesta es correcta para la pregunta
    PRIMARY KEY (id_pregunta, id_respuesta)
);

-- Relación Evalua (Estudiantes - Asignaturas - Profesores - Preguntas - Respuestas)
CREATE TABLE Evalua (
    cod_estudiante BIGINT NOT NULL, -- Clave primaria de Estudiantes
    cod_asignatura INT NOT NULL, -- Clave primaria de Asignaturas
    grupo SMALLINT NOT NULL, -- Grupo específico de la asignatura
    cod_profesor INT NOT NULL, -- Profesor que imparte la asignatura
    id_pregunta INT NOT NULL, -- Clave primaria de Preguntas
    id_respuesta INT NOT NULL, -- Clave primaria de Respuestas
    --nota DECIMAL(5, 2) NOT NULL, -- Nota asignada
    PRIMARY KEY (cod_estudiante, cod_asignatura, grupo, cod_profesor, id_pregunta, id_respuesta),
    FOREIGN KEY (cod_estudiante, cod_asignatura) REFERENCES Cursa(cod_estudiante, cod_asignatura),
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo) REFERENCES Imparte(cod_profesor, cod_asignatura, grupo),
    FOREIGN KEY (id_pregunta, id_respuesta) REFERENCES Corresponde(id_pregunta, id_respuesta)
);

-- Relación Crea (Imparte - Evalua)
CREATE TABLE Crea (
    cod_profesor INT NOT NULL, -- Clave primaria de Imparte
    cod_asignatura INT NOT NULL, -- Clave primaria de Imparte
    grupo SMALLINT NOT NULL, -- Clave primaria de Imparte
    cod_estudiante BIGINT NOT NULL, -- Clave primaria de Evalua
    id_pregunta INT NOT NULL, -- Clave primaria de Evalua
    id_respuesta INT NOT NULL, -- Clave primaria de Evalua
    id_examen INT NOT NULL, -- Identificador único del examen creado
    examen_finalizado BOOLEAN NOT NULL, -- Indica si el examen está finalizado
    id_salon INT, -- Relación con el salón donde se desarrolla el examen (de Desarrolla)
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen),
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo) REFERENCES Imparte(cod_profesor, cod_asignatura, grupo),
    FOREIGN KEY (cod_estudiante, cod_asignatura, grupo, cod_profesor, id_pregunta, id_respuesta) REFERENCES Evalua(cod_estudiante, cod_asignatura, grupo, cod_profesor, id_pregunta, id_respuesta)
);

-- Relación Ingresa (Imparte - Corresponde)
CREATE TABLE Ingresa (
    cod_profesor INT NOT NULL, -- Clave primaria de Imparte
    cod_asignatura INT NOT NULL, -- Clave primaria de Imparte
    grupo SMALLINT NOT NULL, -- Clave primaria de Imparte
    id_pregunta INT NOT NULL, -- Clave primaria de Corresponde
    id_respuesta INT NOT NULL, -- Clave primaria de Corresponde
    tiempo_pregunta SMALLINT NOT NULL CHECK (tiempo_pregunta BETWEEN 1 AND 60), -- Tiempo asignado por el profesor
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo, id_pregunta, id_respuesta), -- Clave primaria compuesta
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo) REFERENCES Imparte(cod_profesor, cod_asignatura, grupo), -- Relación con Imparte
    FOREIGN KEY (id_pregunta, id_respuesta) REFERENCES Corresponde(id_pregunta, id_respuesta) -- Relación con Corresponde
);

-- Relación Programa (Imparte - Crea - Evalua)
CREATE TABLE Programa (
    cod_profesor INT NOT NULL, -- Clave primaria de Imparte
    cod_asignatura INT NOT NULL, -- Clave primaria de Imparte
    grupo SMALLINT NOT NULL, -- Clave primaria de Imparte
    cod_estudiante BIGINT NOT NULL, -- Clave primaria de Evalua
    id_pregunta INT NOT NULL, -- Clave primaria de Evalua
    id_respuesta INT NOT NULL, -- Clave primaria de Evalua
    id_examen INT NOT NULL, -- Identificador único del examen creado
    fecha_examen DATE NOT NULL, -- Fecha programada para el examen
    hora_examen TIME NOT NULL, -- Hora específica del examen
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen), -- Clave primaria compuesta
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen) REFERENCES Crea(cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen) -- Conexión con Crea
);

-- Relación Responde (Crea - Corresponde)
CREATE TABLE Responde (
    cod_profesor INT NOT NULL, -- Clave primaria de Crea
    cod_asignatura INT NOT NULL, -- Clave primaria de Crea
    grupo SMALLINT NOT NULL, -- Clave primaria de Crea
    cod_estudiante BIGINT NOT NULL, -- Clave primaria de Crea
    id_pregunta INT NOT NULL, -- Clave primaria de Corresponde y Crea
    id_respuesta INT NOT NULL, -- Clave primaria de Corresponde y Crea
    id_examen INT NOT NULL, -- Clave primaria de Crea
    fecha_envio_examen DATE NOT NULL, -- Fecha en la que el estudiante envía la respuesta
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen), -- Clave primaria compuesta
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen) REFERENCES Crea(cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen), -- Conexión con Crea
    FOREIGN KEY (id_pregunta, id_respuesta) REFERENCES Corresponde(id_pregunta, id_respuesta) -- Conexión con Corresponde
);

-- Relación Selecciona (Crea - Corresponde)
CREATE TABLE Selecciona (
    cod_profesor INT NOT NULL, -- Clave primaria de Crea
    cod_asignatura INT NOT NULL, -- Clave primaria de Crea
    grupo SMALLINT NOT NULL, -- Clave primaria de Crea
    cod_estudiante BIGINT NOT NULL, -- Clave primaria de Crea
    id_pregunta INT NOT NULL, -- Clave primaria de Corresponde y Crea
    id_examen INT NOT NULL, -- Clave primaria de Crea
    id_respuesta INT NOT NULL, -- Clave primaria de Corresponde
    resp_seleccionada INT NOT NULL, -- Identificador de la respuesta seleccionada (parte de la clave primaria)
    fecha_seleccion TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha y hora de la selección
    PRIMARY KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_examen, resp_seleccionada), -- Clave primaria compuesta
    FOREIGN KEY (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen) REFERENCES Crea(cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen), -- Conexión con Crea
    FOREIGN KEY (id_pregunta, id_respuesta) REFERENCES Corresponde(id_pregunta, id_respuesta) -- Conexión con Corresponde
);
