-- Profesores
INSERT INTO Profesores (cod_profesor, nom_profesor, profesion, niv_escolaridad) VALUES
(30590, 'Hans Lopez', 'Ingeniero Electrónico', 'Doctorado'),
(30456, 'Jairo Soriano', 'Ingeniero Industrial', 'Maestría'),
(30580, 'Francisco Zamora', 'Ingeniero Electrónico', 'Doctorado'),
(30690, 'Adriana Segovia', 'Economista', 'Doctorado'),
(30890, 'Natalia Vega', 'Gestora de Proyectos', 'Maestría');

-- Asignaturas
INSERT INTO Asignaturas (cod_asignatura, nom_asignatura, credit_asignatura, inten_horaria) VALUES
(5014, 'Circuitos Eléctricos I', 4, 12),
(5015, 'Circuitos Eléctricos II', 4, 12),
(1001, 'Cálculo Diferencial', 4, 12),
(7777, 'Redes I', 3, 9),
(1324, 'Formulación y Evaluación de Proyectos', 3, 9);

-- Estudiantes
INSERT INTO Estudiantes (cod_estudiante, nom_estudiante, dir_estudiante, tel_estudiante, cod_carrera, fecha_nacimiento)
VALUES
(20142005141, 'Steven Valencia', 'Avenida Sol 132', '3142873121', 173, '1996-10-14'),
(20152005073, 'Ariana Ortiz', 'Avenida Luna 10', '3122345687', 173, '1997-03-07'),
(20162007001, 'Miguel Rodriguez', 'Calle Hermosa 57', '3118934566', 178, '2000-02-02'),
(20162007002, 'Sofía Guevara', 'Avenida Ocales 47', '3141321231', 178, '2005-08-02'),
(20202003001, 'Katerine Perez', 'Calle Galerias 53', '3245668901', 179, '1990-12-20'),
(20202003002, 'Felipe Mancilla', 'Avenida Only 67', '3216789012', 179, '1996-07-10'),
(20202003003, 'Ana Lopez', 'Calle del Parque 123', '3123456789', 173, '1998-01-15'),
(20212004001, 'Carlos Herrera', 'Avenida Siempre Viva 742', '3134567890', 178, '1995-11-30'),
(20212004002, 'Luisa Ramirez', 'Calle del Sol 89', '3145678901', 179, '2001-05-20'),
(20222005001, 'Mario Gomez', 'Avenida Primavera 45', '3156789012', 173, '1999-09-10'),
(20222005002, 'Laura Medina', 'Calle Verano 67', '3167890123', 178, '1997-07-30'),
(20232006001, 'Pedro Sanchez', 'Avenida Otoño 89', '3178901234', 179, '2002-12-15'),
(20232006002, 'Juliana Torres', 'Calle Invierno 12', '3189012345', 173, '1996-04-25'),
(20242007001, 'Sebastian Vargas', 'Avenida del Rio 34', '3190123456', 178, '2000-08-18'),
(20242007002, 'Valentina Ruiz', 'Calle del Lago 56', '3201234567', 179, '1995-03-09'),
(20252008001, 'David Castillo', 'Avenida de la Paz 78', '3212345678', 173, '1998-10-01'),
(20252008002, 'Camila Gonzalez', 'Calle de la Esperanza 90', '3223456789', 178, '1999-11-20'),
(20262009001, 'Jorge Martinez', 'Avenida del Bosque 11', '3234567890', 179, '2001-02-14'),
(20262009002, 'Natalia Morales', 'Calle de las Flores 22', '3245678901', 173, '1994-06-30'),
(20272010001, 'Gabriel Diaz', 'Avenida de los Pinos 33', '3256789012', 178, '1997-01-18');

-- Imparte (Profesores ↔ Asignaturas)
INSERT INTO Imparte (cod_profesor, cod_asignatura, grupo, horario) VALUES
(30590, 5014, 1, 'Lunes 6:00 AM'),
(30580, 5015, 1, 'Miércoles 8:00 AM'),
(30456, 1001, 1, 'Lunes 6:00 AM'),
(30580, 7777, 1, 'Lunes 6:00 AM'),
(30690, 1324, 1, 'Martes 8:00 AM');

-- Cursa (Estudiantes ↔ Asignaturas)
INSERT INTO Cursa (cod_estudiante, cod_asignatura) VALUES
(20142005141, 5014),
(20142005141, 1001),
(20152005073, 5015),
(20202003001, 1001),
(20202003002, 5015),
(20142005141, 7777),
(20142005141, 1324),
(20152005073, 1324),
(20162007001, 7777),
(20162007002, 5014),
(20202003001, 5015);

-- Tipos de Preguntas
INSERT INTO TiposPreguntas (id_tipo_pregunta, nombre_tipo)
VALUES
(1, 'Opción Múltiple - Múltiple Respuesta'),
(2, 'Opción Múltiple - Única Respuesta'),
(3, 'Verdadero/Falso');

-- Tipo Examen
INSERT INTO TipoExamen (id_tipo_examen, nombre_tipo_examen)
VALUES
(1, '1er corte'),
(2, '2do corte'),
(3, '3er corte'),
(4, 'Final');

-- Preguntas
INSERT INTO Preguntas (desc_pregunta, tipo_pregunta)
VALUES
('¿Qué componentes se necesitan para un circuito eléctrico básico?', 1), -- Múltiples Respuestas
('¿Cuál es la fórmula de la Ley de Ohm?', 2), -- Única Respuesta
('Verdadero o Falso: Un voltímetro se conecta en paralelo.', 3), -- Verdadero/Falso
('Seleccione los componentes de una red LAN.', 1), -- Múltiples Respuestas
('¿Cuál es el puerto estándar para HTTP?', 2); -- Única Respuesta

-- Respuestas
INSERT INTO Respuestas (desc_respuesta)
VALUES
('Una fuente de alimentación, cables y resistencias'), -- Respuesta para Pregunta 1
('Un interruptor y una batería'),                     -- Respuesta para Pregunta 1
('V = IR'),                                           -- Respuesta para Pregunta 2
('I = VR'),                                           -- Respuesta incorrecta para Pregunta 2
('Verdadero'),                                        -- Respuesta para Pregunta 3
('Falso'),                                            -- Respuesta incorrecta para Pregunta 3
('Switch, Router, Cables de red'),                    -- Respuesta para Pregunta 4
('Servidor Web, Cliente'),                            -- Respuesta para Pregunta 4
('80'),                                               -- Respuesta para Pregunta 5
('443');                                              -- Respuesta incorrecta para Pregunta 5

-- Corresponde
INSERT INTO Corresponde (id_pregunta, id_respuesta, correcta)
VALUES
(1, 1, TRUE), -- Pregunta 1, respuesta correcta
(1, 2, TRUE), -- Pregunta 1, otra respuesta correcta
(2, 3, TRUE), -- Pregunta 2, única respuesta correcta
(2, 4, FALSE), -- Pregunta 2, respuesta incorrecta
(3, 5, TRUE), -- Pregunta 3, verdadero es correcto
(3, 6, FALSE), -- Pregunta 3, falso es incorrecto
(4, 7, TRUE), -- Pregunta 4, correcta
(4, 8, TRUE), -- Pregunta 4, otra respuesta correcta
(5, 9, TRUE), -- Pregunta 5, respuesta correcta
(5, 10, FALSE); -- Pregunta 5, respuesta incorrecta

-- Evalua (Estudiantes responden preguntas)
INSERT INTO Evalua (cod_estudiante, cod_asignatura, grupo, cod_profesor, id_pregunta, id_respuesta)
VALUES
(20142005141, 5014, 1, 30590, 1, 1), -- Estudiante responde correctamente a Pregunta 1
(20152005073, 5015, 1, 30580, 2, 3), -- Estudiante responde correctamente a Pregunta 2
(20162007001, 7777, 1, 30580, 3, 5), -- Pregunta 3, correcto
(20162007002, 5014, 1, 30590, 4, 7), -- Pregunta 4, correcta
(20202003002, 5015, 1, 30580, 5, 9); -- Pregunta 5, correcta

INSERT INTO Crea (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen, tipo_examen, examen_finalizado, id_salon)
VALUES
(30590, 5014, 1, 20142005141, 1, 1, 1, 1, FALSE, NULL), -- Examen del 1er corte
(30580, 5015, 1, 20152005073, 2, 3, 2, 4, FALSE, NULL);    -- Examen final

-- Programa (Exámenes programados)
INSERT INTO Programa (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_respuesta, id_examen, fecha_examen, hora_examen)
VALUES
(30590, 5014, 1, 20142005141, 1, 1, 1, '2024-12-01', '09:00:00'), -- Examen 1 programado
(30580, 5015, 1, 20152005073, 2, 3, 2, '2024-12-02', '10:00:00'); -- Examen 2 programado

-- Selecciona (Respuestas seleccionadas por estudiantes)
INSERT INTO Selecciona (cod_profesor, cod_asignatura, grupo, cod_estudiante, id_pregunta, id_examen, id_respuesta, resp_seleccionada, fecha_seleccion)
VALUES
(30590, 5014, 1, 20142005141, 1, 1, 1, 1, '2024-12-01 09:30:00'), -- Respuesta seleccionada para Pregunta 1
(30580, 5015, 1, 20152005073, 2, 2, 3, 3, '2024-12-02 10:30:00'); -- Respuesta seleccionada para Pregunta 2
