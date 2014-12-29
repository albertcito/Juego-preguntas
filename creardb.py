#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sqlite3

with sqlite3.connect("proyecto.db") as connection:
	c = connection.cursor()
	c.execute("DROP TABLE IF EXISTS usuario")
	tuser="""CREATE TABLE `usuario` (
				`email`	TEXT,
				`clave`	TEXT,
				`salt`	TEXT,
				`nombre`	TEXT,
				PRIMARY KEY(email)
			);""";
	c.execute(tuser);

	c.execute("DROP TABLE IF EXISTS etapa")
	tetapa="""CREATE TABLE `etapa` (
				`nombre_etapa`	TEXT,
				`monto`	INTEGER,
				"no_etapa" INTEGER UNIQUE,
				"mensaje" TEXT,
				PRIMARY KEY(nombre_etapa)
			);""";
	c.execute(tetapa);

	c.execute("DROP TABLE IF EXISTS participacion")
	tparticipacion="""CREATE TABLE `participacion` (
						`fecha`	DATETIME,
						`usuario_email`	TEXT,
						`etapa_nombre_etapa`	TEXT,
						FOREIGN KEY(`usuario_email`) REFERENCES 'usuario'('email'),
						FOREIGN KEY(`etapa_nombre_etapa`) REFERENCES 'etapa'('nombre_etapa')
					);""";
	c.execute(tparticipacion);

	c.execute("DROP TABLE IF EXISTS preguntas")
	tpreguntas="""CREATE TABLE `preguntas` (
					`id_pregunta`	INTEGER,
					`pregunta`	TEXT,
					`respuesta_correcta`	TEXT,
					`etapa_nombre_etapa`	TEXT,
					PRIMARY KEY(id_pregunta AUTOINCREMENT),
					FOREIGN KEY(`etapa_nombre_etapa`) REFERENCES 'etapa'('nombre_etapa')
				);""";
	c.execute(tpreguntas);

	c.execute("DROP TABLE IF EXISTS alternativa")
	talternativa="""CREATE TABLE `alternativa` (
					`id_alterantiva`	INTEGER,
					`respuesta`	TEXT,
					`preguntas_id_pregunta`	INTEGER,
					PRIMARY KEY(id_alterantiva AUTOINCREMENT),
					FOREIGN KEY(`preguntas_id_pregunta`) REFERENCES 'preguntas'('id_pregunta')
				);""";
	c.execute(talternativa);

	#Agregamos usuarios
	
	nuevosUsuarios = """
    INSERT INTO usuario ('email', 'clave','salt','nombre')
    VALUES (?, ?, ?, ?)""";

	c.execute(
		nuevosUsuarios,
		(
			"diego@gmail.com",
			"34e264d853b546fe79c13163ab2dfacc57d4ecaff3f9fc3984125916",
			"nopasanada",
			"Diego"
		)
	);
	c.execute(
		nuevosUsuarios,
		(
			"albert@gmail.com", 
			"1b8ee216f179fe4c44c30201e551c3fe2ccc06234d24ba4ea09900f8",
			"quepasa",
			"Albert"
		)
	);
	nuevaEtapa = ("""INSERT INTO `etapa`(`nombre_etapa`,`monto`,`no_etapa`,`mensaje`) VALUES (?,?,?,?);""");
	c.execute(nuevaEtapa,("Basica",1000,1,"etapa 1"));
	c.execute(nuevaEtapa,("Liceo",5000,2,"etapa 2"));
	c.execute(nuevaEtapa,("Universidad",10000,3,"etapa 3"));
	c.execute(nuevaEtapa,("Magister",150000,4,"etapa 4"));
	c.execute(nuevaEtapa,("Doctorado",200000,5,"etapa 5"));

	#preguntas ETAPA 1
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué instrumento musical tiene nombre y forma geométricos?","triangulo","Basica");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el fruto del roble?","bellota","Basica");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el único mamífero con cuatro rodillas?","el elefante","Basica");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuántos jugadores se pueden sustituir en un partido de fútbol amistoso?","7","Basica");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué hace una persona alrededor de 295 veces durante la comida?","tragar","Basica");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el único mamífero que no puede saltar?","elefante","Basica");""");
	#ALTERNATIVA ETAPA 1
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("guitarra",1)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("bajo",1)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("tambor",1)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("manzana",2)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("papa",2)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("naranja",2)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("hipopotamo",3)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("leon",3)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("jirafa",3)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("1",4)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("2",4)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("5",4)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("mirar",5)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("oler",5)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("tocar",5)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("jirafa",6)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("leon",6)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("gato",6)""");
	#PREGUNTAS ETAPA 2
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿En qué deporte se usa tiza?.","billar","Liceo");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Con qué nombre firmaba Pablo Picasso sus pinturas?","picasso","Liceo");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué parte de los libros suele tener los números pares?","izquierdo","Liceo");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál de los cinco sentidos se desarrolla primero?","el olfato","Liceo");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cómo se dice vino en italiano?","vino","Liceo");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el dedo más sensible de la mano?","indice","Liceo");""");
	#ALTERNATIVAS ETAPA 2
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("futbol",7)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("natacion",7)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("tenis",7)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("pablo",8)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("pp",8)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("pablo picasso",8)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("derecho",9)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("arriba",9)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("abajo",9)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("el oido",10)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("la vista",10)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("el tacto",10)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("wine",11)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("vinho",11)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("wein",11)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("pulgar",12)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("meñique",12)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("anular",12)""");

	#PREGUNTAS ETAPA 3
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Quién escribió El Diario de Ana Frank?","ella misma","Universidad");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué isla del Caribe tiene nombre de flor?","isla margarita","Universidad");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿En qué provincia española se halla la ciudad de Jabugo, famosa por sus exquisitos jamones?","Huelva","Universidad");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuántas pirámides hay en Egipto?","10000","Universidad");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuántas personas se refugiaron en el Arca de Noé?","8","Universidad");""");

	#ALTERNATIVAS ETAPA 3
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Pablo neruda",13)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Jose manuel",13)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Gabriela Mistral",13)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("isla tulipan",14)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("isla rosa",14)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("isla jirasol",14)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Valencia",15)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Valladolid",15)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("Valladolid",15)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("10",16)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("100",16)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("1000",16)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("6",17)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("4",17)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("2",17)""");

	#PREGUNTAS ETAPA 4
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el limite de edad establecido para participar en los Juegos Olímpicos?","ninguna","Magister");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es la residencia oficial más grande del mundo?","el vaticano","Magister");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es la moneda de Suiza?","franco suizo","Magister");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿De qué color es la pelota de hockey sobre césped? ","blanca","Magister");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el segundo idioma más hablado del mundo?","ingles","Magister");""");

	#ALTERNATIVAS ETAPA 4
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("30 años",18)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("40 años",18)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("50 años",18)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("iglesia catolica",19)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("san francisco",19)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("luterana",19)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("peso",20)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("soles",20)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("euro",20)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("negra",21)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("roja",21)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("azul",21)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("chino",22)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("japones",22)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("aleman",22)""");


	#PREGUNTAS ETAPA 5
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuáles son las dos primeras palabras de la Biblia?","al principio","Doctorado");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué órgano segrega la hormona insulina?","pancreas","Doctorado");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿En qué árbol crecen los dátiles?","palmera","Doctorado");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Qué rasgo facial no tiene la Mona Lisa?","cejas","Doctorado");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cuál es el signo de puntuación más usado?","coma","Doctorado");""");
	c.execute("""insert into "preguntas"("pregunta","respuesta_correcta","etapa_nombre_etapa")
	values("¿Cómo se conoce vulgarmente el encéfalo?","sesos","Doctorado");""");

	#ALTERNATIVAS ETAPA 5
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("moises",23)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("jesus",23)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("no pecaras",23)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("higado",24)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("el ojo",24)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("corazon",24)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("manzano",25)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("roble",25)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("avellano",25)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("orejas",26)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("boca",26)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("ojos",26)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("punto",27)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("parentesis",27)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("signo interrogación",27)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("cerebelo",28)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("craneo",28)""");
	c.execute("""INSERT INTO `alternativa`(`respuesta`,`preguntas_id_pregunta`)VALUES ("cerebro",28)""");




	#tira problemas
	#nuevaPregunta = ("""INSERT INTO `preguntas`(`pregunta`,`respuesta_correcta`,`etapa_nombre_etapa`) VALUES (?,?,?);""");
	#c.execute(nuevaPregunta,("Que instrumento musical tiene nombre y forma geometricos","triangulo","Basica"));





























