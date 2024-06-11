CREATE TABLE IF NOT EXISTS posadas (
    identificador SMALLINT UNIQUE,
	nombre VARCHAR(100),
    precioNoche DECIMAL(10,2),
    metrosCuadrados SMALLINT,
    ambientes TINYINT,
    camasIndividuales TINYINT,
    camasMatrimoniales TINYINT,
    calefaccion BOOLEAN,
    desayuno BOOLEAN,
    accesoDiscapacitados BOOLEAN,
    vistaHacia VARCHAR(100),
    descripcion VARCHAR(500),
    foto1 VARCHAR(200),
    foto2 VARCHAR(200),
    foto3 VARCHAR(200),
    foto4 VARCHAR(200),
    foto5 VARCHAR(200),
    PRIMARY KEY (identificador)
);

CREATE TABLE IF NOT EXISTS reservas (
	id MEDIUMINT NOT NULL AUTO_INCREMENT,
    identificadorPosada SMALLINT,
    personaUUID CHAR(36),
    fechaIngreso DATETIME,
    fechaEgreso DATETIME,
	PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS usuarios (
    UUID CHAR(36) UNIQUE NOT NULL,
    nombre VARCHAR(30),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    pass VARCHAR(60),
    PRIMARY KEY (UUID)
);

CREATE TABLE IF NOT EXISTS resenias (
    idResena INT PRIMARY KEY AUTO_INCREMENT,
    identificadorPosada SMALLINT NOT NULL,
    personaUUID CHAR(36) NOT NULL,
    fechaResena DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    puntuacion TINYINT NOT NULL CHECK (puntuacion BETWEEN 1 AND 5),
    comentario VARCHAR(200),
    FOREIGN KEY (identificadorPosada) REFERENCES posadas(identificador),
    FOREIGN KEY (personaUUID) REFERENCES usuarios(UUID)
);

-- Usuarios precargados

INSERT INTO usuarios VALUES ("69d07c33-1eec-11ef-bc3d-0242ac120002", "Pedro", "Lopez", "p.lopez@gmail.com", "Pedropass11");

INSERT INTO usuarios VALUES ("123e4567-e89b-12d3-a456-426655440001", "Juan", "Perez", "j.perez@gmail.com", "JuanPerez2023");

INSERT INTO usuarios VALUES ("789a01bc-3456-789a-b2cd-e12345678901", "María", "Gómez", "maria.gomez@hotmail.com", "MariaGomez123");

INSERT INTO usuarios VALUES ("c3b1f29f-4567-89ab-cdef-0123456789ab", "Roberto", "Blanco", "roberto.blanco@yahoo.com", "RobertoBlanco");

INSERT INTO usuarios VALUES ("f4e23110-1234-5678-9abc-def012345678", "Ana", "López", "ana.lopez@otrodominio.com", "AnaLopez2024");

-- Posadas precargadas

INSERT INTO posadas VALUES (
	101,
	"Amapola",
	60000.00,
	70,
	3,
	2,
	1,
	1,
	1,
	0,
	"complejo",
	" -Heladera -Microondas -Termotanque -Cocina a gas -Cafetera -Calefactor -Aire acondicionado frio-calor - Secador de pelo - Smart TV",
	"static/images/Amapola/amapola_Living.jpg",
	"static/images/Amapola/amapola_Camas.jpg",
	"static/images/Amapola/amapola_Matrimonial.jpg",
	"static/images/Amapola/amapola_Cocina.jpg",
	"static/images/Amapola/amapola_Sala.jpg"
);

INSERT INTO posadas VALUES (
	201,
	"Trucha Dorada",
	80000.00,
	100,
	3,
	3,
	1,
	1,
	1,
	1,
	"complejo",
	"-Hogar a lenia -Aire acondicionado -Baniera de hidromasaje -TV -Cafetera -Heladera  -Cafetera -Microondas -Secador de pelo -Horno - Tostadora",
	"static/images/TruchaDorada/truchaDorada_Living.jpg",
	"static/images/TruchaDorada/truchaDorada_Camas.jpg",
	"static/images/TruchaDorada/truchaDorada_Matrimonial.jpg",
	"static/images/TruchaDorada/truchaDorada_Cocina.jpg",
	"static/images/TruchaDorada/truchaDorada_Bano.jpg"
);

INSERT INTO posadas VALUES (
	301,
	"Ciervo Blanco",
	200000.00,
	120,
	5,
	5,
	1,
	1,
	1,
	0,
	"lago",
	" -Banio en suite -Cocina completa -Smart TV -Hogar a lenia -Banios completos",
	"static/images/CiervoBlanco/ciervoBlanco_Living.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Camas.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Camas_2.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Matrimonial.jpg",
	"static/images/CiervoBlanco/ciervoBlanco_Bano.jpg"
);

INSERT INTO posadas VALUES (
	401,
	"Hierba Alta",
	40000.00,
	40,
	2,
	0,
	1,
	1,
	1,
	1,
	"bosque",
	"- Cocina completa - Lavadora -Banio completo -Smart TV  -Secador de pelo -Secadora de ropa ",
	"static/images/HierbaAlta/hierbaAlta_Cocina.jpg",
	"static/images/HierbaAlta/hierbaAlta_Cocina_2.jpg",
	"static/images/HierbaAlta/hierbaAlta_Balcon.jpg",
	"static/images/HierbaAlta/hierbaAlta_Matrimonial.jpg",
	"static/images/HierbaAlta/hierbaAlta_Bano.jpg"
);

INSERT INTO posadas VALUES (
	501,
	"Bosque Alto",
	250000.00,
	150,
	5,
	6,
	2,
	1,
	1,
	0,
	"bosque",
	"-Heladera -Microondas -Termotanque -Cocina a gas -Cafetera -Calefactor - Aire acondicionado frio/calor -Secador de pelo -Smart TV",	
	"static/images/BosqueAlto/bosqueAlto_Living.jpg",
	"static/images/BosqueAlto/bosqueAlto_Camas.jpg",
	"static/images/BosqueAlto/bosqueAlto_Camas_2.jpg",
	"static/images/BosqueAlto/bosqueAlto_Cocina.jpg",
	"static/images/BosqueAlto/bosqueAlto_Bano.jpg"
);

INSERT INTO posadas VALUES (
	601,
	"Carpincho",
	1250000.00,
	200,
	2,
	0,
	1,
	1,
	1,
	1,
	"bosque",
	"-Hogar a lenia -Aire acondicionado - Baniera de hidromasaje -Smart TV -Cafetera -Heladera -Cafetera -Microondas -Secador de pelo - Horno -Tostadora",
	"static/images/Carpincho/carpincho_Living.jpg",
	"static/images/Carpincho/carpincho_Matrimonial.jpg",
	"static/images/Carpincho/carpincho_Camas.jpg",
	"static/images/Carpincho/carpincho_Bano_1.jpg",
	"static/images/Carpincho/carpincho_Cocina.jpg"
);

-- Reservas

INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso) VALUES (101, "69d07c33-1eec-11ef-bc3d-0242ac120002", "2024-6-10", "2024-6-21");
INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso) VALUES (501, "c3b1f29f-4567-89ab-cdef-0123456789ab", "2024-5-10", "2024-6-10");
INSERT INTO reservas (identificadorPosada, personaUUID, fechaIngreso, fechaEgreso) VALUES (101, "f4e23110-1234-5678-9abc-def012345678", "2024-5-22", "2024-6-30");

--Resenias

INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (101, '123e4567-e89b-12d3-a456-426655440001', 3, 'Hermoso complejo. Un lugar unico para disfrutar las vacaciones en familia');
INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (301, 'c3b1f29f-4567-89ab-cdef-0123456789ab', 5, 'Las vistas son realmente increibles. Super recomendable Posadas del Lago');
INSERT INTO resenias (identificadorPosada, personaUUID, puntuacion, comentario) VALUES (601, 'f4e23110-1234-5678-9abc-def012345678', 5, 'Disfrutamos cada momento, vistas impresionante. Nuestra estadia fue simplemente perfecta');
