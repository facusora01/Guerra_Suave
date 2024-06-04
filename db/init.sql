CREATE TABLE IF NOT EXISTS posadas (
    identificador SMALLINT UNIQUE,
    precioNoche DECIMAL(10,2),
    metrosCuadrados SMALLINT,
    ambientes TINYINT,
    camasIndividuales TINYINT,
    camasMatrimoniales TINYINT,
    calefacción BOOLEAN,
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
    identificadorPosada SMALLINT,
    personaUUID CHAR(36),
    fechaIngreso DATETIME,
    fechaEgreso DATETIME 
);

CREATE TABLE IF NOT EXISTS usuarios (
    UUID CHAR(36) UNIQUE NOT NULL,
    nombre VARCHAR(30),
    apellido VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    pass VARCHAR(60),
    PRIMARY KEY (UUID)
);


-- Usuarios precargados

INSERT INTO usuarios VALUES ("69d07c33-1eec-11ef-bc3d-0242ac120002", "Pedro", "Lopez", "p.lopez@gmail.com", "Pedropass11");

INSERT INTO usuarios VALUES ("123e4567-e89b-12d3-a456-426655440001", "Juan", "Perez", "j.perez@gmail.com", "JuanPerez2023");

INSERT INTO usuarios VALUES ("789a01bc-3456-789a-b2cd-e12345678901", "María", "Gómez", "maria.gomez@hotmail.com", "MariaGomez123");

INSERT INTO usuarios VALUES ("c3b1f29f-4567-89ab-cdef-0123456789ab", "Roberto", "Blanco", "roberto.blanco@yahoo.com", "RobertoBlanco");

INSERT INTO usuarios VALUES ("f4e23110-1234-5678-9abc-def012345678", "Ana", "López", "ana.lopez@otrodominio.com", "AnaLopez2024");

-- Posadas precargados

INSERT INTO posadas VALUES (
	101,
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
	"static/images/Amapola/amapola1.jpg",
	"static/images/Amapola/amapola2.jpg",
	"static/images/Amapola/amapola3.jpg",
	"static/images/Amapola/amapola4.jpg",
	"static/images/Amapola/amapola5.jpg"
);

INSERT INTO posadas VALUES (
	201,
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
	"static/images/TruchaDorada/truchaDorada1.jpg",
	"static/images/TruchaDorada/truchaDorada2.jpg",
	"static/images/TruchaDorada/truchaDorada3.jpg",
	"static/images/TruchaDorada/truchaDorada4.jpg",
	"static/images/TruchaDorada/truchaDorada5.jpg"
);

INSERT INTO posadas VALUES (
	301,
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
	"static/images/CiervoBlanco/ciervoBlanco1.jpg",
	"static/images/CiervoBlanco/ciervoBlanco2.jpg",
	"static/images/CiervoBlanco/ciervoBlanco3.jpg",
	"static/images/CiervoBlanco/ciervoBlanco4.jpg",
	"static/images/CiervoBlanco/ciervoBlanco5.jpg"
);

INSERT INTO posadas VALUES (
	401,
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
	"static/images/HierbaAlta/hierbaAlta1.jpg",
	"static/images/HierbaAlta/hierbaAlta2.jpg",
	"static/images/HierbaAlta/hierbaAlta3.jpg",
	"static/images/HierbaAlta/hierbaAlta4.jpg",
	"static/images/HierbaAlta/hierbaAlta5.jpg"
);

INSERT INTO posadas VALUES (
	501,
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
	"static/images/BosqueAlto/bosqueAlto1.jpg","static/images/BosqueAlto/bosqueAlto2.jpg",
	"static/images/BosqueAlto/bosqueAlto3.jpg",
	"static/images/BosqueAlto/bosqueAlto4.jpg",
	"static/images/BosqueAlto/bosqueAlto5.jpg"
);

INSERT INTO posadas VALUES (
	601,
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
	"static/images/Carpincho/carpincho7.jpg",
	"static/images/Carpincho/carpincho6.jpg",
	"static/images/Carpincho/carpincho5.jpg",
	"static/images/Carpincho/carpincho4.jpg",
	"static/images/Carpincho/carpincho3.jpg"
);
