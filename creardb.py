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
					PRIMARY KEY(id_pregunta),
					FOREIGN KEY(`etapa_nombre_etapa`) REFERENCES 'etapa'('nombre_etapa')
				);""";
	c.execute(tpreguntas);

	c.execute("DROP TABLE IF EXISTS alternativa")
	talternativa="""CREATE TABLE `alternativa` (
					`id_alterantiva`	INTEGER,
					`respuesta`	TEXT,
					`preguntas_id_pregunta`	INTEGER,
					PRIMARY KEY(id_alterantiva),
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

