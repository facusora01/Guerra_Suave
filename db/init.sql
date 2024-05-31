CREATE TABLE IF NOT EXISTS posadas (
    identificador SMALLINT UNIQUE,
    precioNoche DECIMAL(10,2),
    metrosCuadrados TINYINT,
    ambientes TINYINT,
    camasUnicas TINYINT,
    camasMatrimoniales TINYINT,
    calefacción BOOLEAN,
    desayuno BOOLEAN,
    accesoDiscapacitados BOOLEAN,
    vistaHacia VARCHAR(100),
    descripcion VARCHAR(500),
    foto1 VARCHAR(200),
    foto2 VARCHAR(200),
    foto3 VARCHAR(200),
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


-- Documentos precargados
INSERT INTO usuarios VALUES (UUID(), "Pedro", "Lopez", "p.lopez@gmail.com", "Pedropass11");

INSERT INTO posadas VALUES (
    103,  
    3500.00,
    58,
    4,
    1,
    2,
    1,
    1,
    0,
    "lago",
    "Hermosa postada con vista al lago, espaciosa y equipada para una agradables vacaciones",
    "https://kabania.ca/wp-content/uploads/2019/03/cabanes-pilotis-pilotis.jpg",
    "",
    ""
);
