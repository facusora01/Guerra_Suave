-- TABLA DE POSADAS
CREATE TABLE IF NOT EXISTS posadas (
    identificador SMALLINT UNIQUE, -- Identificador de la posada
	nombre VARCHAR(100), -- Nombre de la posada
    precioNoche DECIMAL(10,2), -- Precio por noche
    metrosCuadrados SMALLINT, -- Metros cuadrados
    ambientes TINYINT, -- Cantidad de ambientes
    camasIndividuales TINYINT, -- Cantidad de camas individuales
    camasMatrimoniales TINYINT, -- Cantidad de camas matrimoniales
    calefaccion BOOLEAN, -- Si tiene callefaccion o no
    desayuno BOOLEAN, -- Si incluye desayuno o no
    accesoDiscapacitados BOOLEAN, -- Si tiene acceso para discapacitados o no
    vistaHacia VARCHAR(100), -- Vista
    descripcion VARCHAR(500), -- Descripcion
    foto1 VARCHAR(200),
    foto2 VARCHAR(200),
    foto3 VARCHAR(200),
    foto4 VARCHAR(200),
    foto5 VARCHAR(200),
    PRIMARY KEY (identificador) -- Clave primaria
);

-- TABLA DE RESERVAS
CREATE TABLE IF NOT EXISTS reservas (
	id MEDIUMINT NOT NULL AUTO_INCREMENT, -- Identificador de la reserva
    identificadorPosada SMALLINT, -- Identificador de la posada
    personaUUID CHAR(36), -- UUID de la persona que reserva (El UUID es el identificador de la persona en la tabla de usuarios)
    fechaIngreso DATETIME, -- Fecha de ingreso
    fechaEgreso DATETIME, -- Fecha de egreso
	nombrePosada VARCHAR(100), -- Nombre de la posada
	imagen VARCHAR(200), -- Imagen de la posada
	PRIMARY KEY (id) -- Clave primaria
);

-- TABLA DE USUARIOS
CREATE TABLE IF NOT EXISTS usuarios (
    UUID CHAR(36) UNIQUE NOT NULL, -- Identificador de la persona
    nombre VARCHAR(30), -- Nombre
    apellido VARCHAR(50), -- Apellido
    email VARCHAR(100) UNIQUE, -- Email
    pass VARCHAR(60), -- Password
    PRIMARY KEY (UUID) -- Clave primaria
);

-- TABLA DE RESEÑAS
CREATE TABLE IF NOT EXISTS resenias (
    idResena INT PRIMARY KEY AUTO_INCREMENT, -- Identificador de la reseña
    identificadorPosada SMALLINT NOT NULL, -- Identificador de la posada
    personaUUID CHAR(36) NOT NULL, -- UUID de la persona que realiza la reseña
    fechaResena DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP, -- Fecha de la reseña
    puntuacion TINYINT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5), -- Puntuación de la reseña
    comentario VARCHAR(200), -- Comentario de la reseña
    FOREIGN KEY (identificadorPosada) REFERENCES posadas(identificador), -- Clave foránea de la posada
    FOREIGN KEY (personaUUID) REFERENCES usuarios(UUID) -- Clave foránea de la persona
);

-- Usuarios precargados

INSERT INTO usuarios VALUES ("69d07c33-1eec-11ef-bc3d-0242ac120002", "Pedro", "Lopez", "p.lopez@gmail.com", "Pedropass11");

INSERT INTO usuarios VALUES ("123e4567-e89b-12d3-a456-426655440001", "Juan", "Perez", "j.perez@gmail.com", "JuanPerez2023");

INSERT INTO usuarios VALUES ("789a01bc-3456-789a-b2cd-e12345678901", "María", "Gómez", "maria.gomez@hotmail.com", "MariaGomez123");

INSERT INTO usuarios VALUES ("c3b1f29f-4567-89ab-cdef-0123456789ab", "Roberto", "Blanco", "roberto.blanco@yahoo.com", "RobertoBlanco");

INSERT INTO usuarios VALUES ("f4e23110-1234-5678-9abc-def012345678", "Ana", "López", "ana.lopez@otrodominio.com", "AnaLopez2024");

-- Posadas precargadas

INSERT INTO posadas VALUES (
	101, -- identificador
	"Amapola", -- nombre
	60000.00, -- precioNoche
	70, -- metrosCuadrados
	3, -- ambientes
	2, -- camasIndividuales
	1, -- camasMatrimoniales
	1, -- Booleano calefaccion
	1, -- Booleano desayuno
	0, -- Booleano accesoDiscapacitados
	"complejo", -- vistaHacia
	"-Heladera -Microondas -Termotanque -Cocina a gas -Cafetera -Calefactor -Aire acondicionado frio-calor - Secador de pelo - Smart TV",
	"static/images/Amapola/amapola_Living.jpg",
	"static/images/Amapola/amapola_Camas.jpg",
	"static/images/Amapola/amapola_Matrimonial.jpg",
	"static/images/Amapola/amapola_Cocina.jpg",
	"static/images/Amapola/amapola_Sala.jpg"
);

INSERT INTO posadas VALUES (
	201, -- identificador
	"Trucha Dorada", -- nombre
	80000.00, -- precioNoche
	100, -- metrosCuadrados
	3, -- ambientes
	3, -- camasIndividuales
	1, -- camasMatrimoniales
	1, -- Booleano calefaccion
	1, -- Booleano desayuno
	1, -- Booleano accesoDiscapacitados
	"complejo", -- vistaHacia
	"-Hogar a lenia -Aire acondicionado -Baniera de hidromasaje -TV -Cafetera -Heladera  -Cafetera -Microondas -Secador de pelo -Horno - Tostadora",
	"static/images/TruchaDorada/truchaDorada_Living.jpg",
	"static/images/TruchaDorada/truchaDorada_Camas.jpg",
	"static/images/TruchaDorada/truchaDorada_Matrimonial.jpg",
	"static/images/TruchaDorada/truchaDorada_Cocina.jpg",
	"static/images/TruchaDorada/truchaDorada_Bano.jpg" 
);

INSERT INTO posadas VALUES (
	301, -- identificador
	"Ciervo Blanco", -- nombre
	200000.00, -- precioNoche
	120, -- metrosCuadrados
	5, -- ambientes
	5, -- camasIndividuales
	1, -- camasMatrimoniales
	1, -- Booleano calefaccion
	1, -- Booleano desayuno
	0, -- Booleano accesoDiscapacitados
	"lago", -- vistaHacia
	"-Banio en suite -Cocina completa -Smart TV -Hogar a lenia -Banios completos",
	"static/images/CiervoBlanco/ciervoBlanco_Living.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Camas.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Camas_2.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Matrimonial.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Bano.jpg"
);

INSERT INTO posadas VALUES (
	401, -- identificador
	"Hierba Alta", -- nombre
	40000.00, -- precioNoche
	40, -- metrosCuadrados
	2, -- ambientes
	0, -- camasIndividuales
	1, -- camasMatrimoniales
	1, -- Booleano calefaccion
	1, -- Booleano desayuno
	1, -- Booleano accesoDiscapacitados
	"bosque", -- vistaHacia
	"- Cocina completa - Lavadora -Banio completo -Smart TV  -Secador de pelo -Secadora de ropa ",
	"static/images/HierbaAlta/hierbaAlta_Cocina.jpg",
	"static/images/HierbaAlta/hierbaAlta_Cocina_2.jpg",
	"static/images/HierbaAlta/hierbaAlta_Balcon.jpg",
	"static/images/HierbaAlta/hierbaAlta_Matrimonial.jpg",
	"static/images/HierbaAlta/hierbaAlta_Bano.jpg"
);

INSERT INTO posadas VALUES (
	501, -- identificador
	"Bosque Alto", -- nombre
	250000.00, -- precioNoche
	150, -- metrosCuadrados
	5, -- ambientes
	6, -- camasIndividuales
	2, -- camasMatrimoniales
	1, -- Booleano calefaccion
	1, -- Booleano desayuno
	0, -- Booleano accesoDiscapacitados
	"bosque", -- vistaHacia
	"-Heladera -Microondas -Termotanque -Cocina a gas -Cafetera -Calefactor - Aire acondicionado frio/calor -Secador de pelo -Smart TV",	
	"static/images/BosqueAlto/bosqueAlto_Living.jpg",
	"static/images/BosqueAlto/bosqueAlto_Camas.jpg",
	"static/images/BosqueAlto/bosqueAlto_Camas_2.jpg",
	"static/images/BosqueAlto/bosqueAlto_Cocina.jpg",
	"static/images/BosqueAlto/bosqueAlto_Bano.jpg"
);

INSERT INTO posadas VALUES (
	601, -- identificador
	"Carpincho", -- nombre
	1250000.00, -- precioNoche
	200, -- metrosCuadrados,
	2, -- ambientes,
	8, -- camasIndividuales,
	1, -- camasMatrimoniales,
	1, -- Booleano calefaccion,
	1, -- Booleano desayuno,
	1, -- Booleano accesoDiscapacitados,
	"bosque", -- vistaHacia
	"-Hogar a lenia -Aire acondicionado - Baniera de hidromasaje -Smart TV -Cafetera -Heladera -Cafetera -Microondas -Secador de pelo - Horno -Tostadora",
	"static/images/Carpincho/carpincho_Living.jpg",
	"static/images/Carpincho/carpincho_Matrimonial.jpg",
	"static/images/Carpincho/carpincho_Camas.jpg",
	"static/images/Carpincho/carpincho_Bano_1.jpg",
	"static/images/Carpincho/carpincho_Cocina.jpg"
);

-- Reservas

INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso, nombrePosada, imagen) VALUES (101, "69d07c33-1eec-11ef-bc3d-0242ac120002", "2024-6-10", "2024-6-21", "Amapola", "static/images/Amapola/amapola_Living.jpg");
INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso, nombrePosada, imagen) VALUES (501, "c3b1f29f-4567-89ab-cdef-0123456789ab", "2024-5-10", "2024-6-10", "Bosque Alto", "static/images/BosqueAlto/bosqueAlto_Living.jpg");
INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso, nombrePosada, imagen) VALUES (301, "69d07c33-1eec-11ef-bc3d-0242ac120002", "2024-5-22", "2024-6-29", "Trucha Dorada", "static/images/CiervoBlanco/ciervoBlanco_Living.jpg");

--Resenias

INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (101, '123e4567-e89b-12d3-a456-426655440001', 3, 'Hermoso complejo. Un lugar unico para disfrutar las vacaciones en familia');
INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (301, 'c3b1f29f-4567-89ab-cdef-0123456789ab', 5, 'Las vistas son realmente increibles. Super recomendable Posadas del Lago');
INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (601, 'f4e23110-1234-5678-9abc-def012345678', 5, 'Disfrutamos cada momento, vistas impresionante. Nuestra estadia fue simplemente perfecta');
