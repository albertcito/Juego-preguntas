# -*- coding: utf-8 -*-
#!/usr/bin/python

from flask import Flask, redirect, url_for,request, Response,render_template,session
from flask import jsonify 
import hashlib
import sys
import random
import sqlite3
import datetime,time
from pprint import pprint


app = Flask(__name__)
app.secret_key="quieres ser millonario => trabaja como negro"
primera = "Basica"

# Define la variable coneción y la retorna 
def getConexion():
    conn = sqlite3.connect('proyecto.db')
    return conn

#define un cursos y lo retorna
def getCursor(conn):
    c = conn.cursor()
    return c;

#muestra el formulario de inicio se sesión
@app.route('/',methods=['GET','POST'])
def index():
    error  = ''
    if request.method == 'POST':
        email = request.form['email']
        clave = request.form['clave']
        c = getCursor(getConexion());
        result = c.execute('select salt from usuario where email = ?',[email])
        matches = result.fetchall()
        error = ""
        if len(matches) > 0:
            user_data = matches[0]
            salt = user_data[0]

            clave = clave+salt
            clave_h = hashlib.sha224(clave.encode('utf-8')).hexdigest()

            result = c.execute('select * from usuario where email=? and clave = ?', 
                                [email,clave_h])
            matches = result.fetchone()
            if matches : 
                session['logged_in'] = True
                session['email'] = email
                session['nombre'] = matches[3]

                return redirect('jugar')
            else:
                error = "Clave erronea."
        else:
            error = "Usuario no existe."

    return render_template('login.html',error=error)

#Muestra las veces que he jugado y hasta donde he llegado
@app.route('/perfil' )
def form():
    if 'email' not in session: return redirect('')
    email = session['email']
    c = getCursor(getConexion());
    participacion = c.execute('select * from participacion WHERE usuario_email=? order by fecha DESC',[email])
    return render_template('perfil.html',participacion=participacion,usuario = session['nombre'])

#Cierra la sesión
@app.route('/salir')
def salir():
    session.pop('email', None)
    return redirect (url_for('index'))

#Muestra la ventana de jugar con preguntas, opciones y etapas
@app.route('/jugar')
def jugar():
    if 'email' not in session: return redirect('')
    
    conn = getConexion()
    c = getCursor(conn)
    result = c.execute('select * from preguntas where etapa_nombre_etapa = ? ORDER BY RANDOM()  limit 1 ',[primera])
    pregunta = result.fetchone()
    id_pregunta = pregunta[0]

    result2 = c.execute('select * from alternativa where preguntas_id_pregunta=? limit 3', [id_pregunta])
    alternativa = result2.fetchall()

    etapa = c.execute('select * from etapa order by monto desc');

    return render_template('jugar.html',pregunta=pregunta,alternativa=alternativa,etapa=etapa,usuario = session['nombre'])

#Muestra la página que perdió
@app.route('/perdio')
def perdio():
    if 'email' not in session: return redirect('')
    etapa = request.args.get('etapa')
    return render_template('perdio.html',usuario = session['nombre'])

#Muestra la página que ganó
@app.route('/gano')
def gano():
    if 'email' not in session: return redirect('')
    return render_template('gano.html',usuario = session['nombre'])

#Verifica si su respuesta es correcta, si es correcta envia una nueva pregunta
@app.route('/_verificar_respuesta')
def _verificar_respuesta():
    respuesta = request.args.get('respuesta')
    etapa = request.args.get('etapa')
    conn = getConexion()
    c = getCursor(conn)
    result = c.execute("""
        select 
            count(*)
        from 
            preguntas p, 
            etapa e 
        where 
            p.respuesta_correcta=? AND 
            p.etapa_nombre_etapa= e.nombre_etapa AND
            e.no_etapa = ?
        """, 
        [respuesta,etapa]
    )
    res = result.fetchone()
    
    #return jsonify(result=res)
    resultado = {}
    resultado["error"] = [(res[0])]
    
    #Si respondió bien la pregunta
    if( res[0] == 1):

        #buscar etapa actual 
        result_etapa = c.execute("""
            select 
                nombre_etapa
            from 
                etapa e 
            where 
                e.no_etapa = ?
            """, 
            etapa
        )
        res_etapa = result_etapa.fetchone()
        #Si la etapa es la primera se inserta, si no se actualiza
        if primera == res_etapa[0]:
            insertParticipacion = """
            INSERT INTO participacion ('fecha', 'usuario_email','etapa_nombre_etapa')
            VALUES (?, ?, ?)""";
            session['now'] = time.strftime("%d/%m/%y %H:%M:%S")
            c.execute(
                insertParticipacion,
                (
                    session['now'],
                    session['email'],
                    res_etapa[0]
                )
            );
            conn.commit()
        else: 
            actualizarParticipacion = """
                UPDATE participacion
                SET etapa_nombre_etapa= ?
                WHERE 
                    usuario_email=? AND
                    fecha = ?;
            """
            c.execute(
                actualizarParticipacion,
                (
                    res_etapa[0],
                    session['email'],
                    session['now']
                )
            );
            conn.commit()

        #Se busca la siguiente etapa
        e = int(etapa)+1
        result2 = c.execute("""
            select 
                *
            from 
                etapa e 
            where 
                e.no_etapa = ?
            """, 
            [e]
        )
        resu = result2.fetchone()

        #Si hay una siguiente etapa se buscan las pregunta sy respustas
        if resu :
            resultado["etapa"] = resu
            result3 = c.execute("""
                select 
                    p.pregunta,
                    p.id_pregunta,
                    p.respuesta_correcta
                from 
                    preguntas p,
                    etapa e 
                where 
                    p.etapa_nombre_etapa= e.nombre_etapa AND
                    e.nombre_etapa = ?
                ORDER BY RANDOM() 
                limit 1 
                """, 
                [resu[0]]
            )
            pregunta_ = result3.fetchone()
            resultado["pregunta"] = pregunta_[0]
            resultado["id_pregunta"] = pregunta_[1]

            result4 = c.execute("""
                select 
                    respuesta 
                from 
                    alternativa 
                where 
                    preguntas_id_pregunta=? 
                limit 3
                """, 
                [pregunta_[1]]
            )
            alternativa = result4.fetchall()
            alternativa.append([pregunta_[2]])
            random.shuffle(alternativa)
            resultado['alternativas'] = alternativa;
        else:
            resultado['gano'] = 1;
    return jsonify(resultado)

#El comodin de 50 porciento envia solo 2 respuestas 
@app.route('/_porciento')
def _porciento():
    id_pregunta = request.args.get('id_pregunta')
    c = getCursor(getConexion())
    p = c.execute("""
        select 
            respuesta_correcta
        from 
            preguntas
        where 
            id_pregunta = ?
        """, 
        [id_pregunta]
    )
    respuestas = p.fetchone()
    resultado = []
    resultado.append(respuestas[0])
    p2 = c.execute("""
        select 
            respuesta 
        from 
            alternativa 
        where 
            preguntas_id_pregunta = ? 
        ORDER BY RANDOM() 
        limit 1
        """, 
        [id_pregunta]
    )
    pregunta2 = p2.fetchone()
    resultado.append(pregunta2[0])
    random.shuffle(resultado)
    matriz = {}
    matriz['alternativas'] = resultado
    return jsonify(matriz)

#El comodin de otra pregunta envía otra pregunta con sus alternativas.
@app.route('/_otra_pregunta')
def _otra_pregunta():
    id_pregunta = request.args.get('id_pregunta')
    no_etapa    = request.args.get('no_etapa')
    c = getCursor(getConexion())
    resultado = {}
    result3 = c.execute("""
        select 
            p.pregunta,
            p.id_pregunta,
            p.respuesta_correcta
        from 
            preguntas p,
            etapa e 
        where 
            p.etapa_nombre_etapa= e.nombre_etapa AND
            e.no_etapa = ? AND
            p.id_pregunta != ?
        ORDER BY RANDOM() 
        limit 1 
        """, 
        [no_etapa,id_pregunta]
    )
    pregunta_ = result3.fetchone()
    resultado["pregunta"] = pregunta_[0]
    resultado["id_pregunta"] = pregunta_[1]

    result4 = c.execute("""
        select 
            respuesta 
        from 
            alternativa 
        where 
            preguntas_id_pregunta=? 
        limit 3
        """, 
        [pregunta_[1]]
    )
    alternativa = result4.fetchall()
    alternativa.append([pregunta_[2]])
    random.shuffle(alternativa)
    resultado['alternativas'] = alternativa;
    return jsonify(resultado)
    

if __name__ == '__main__':
    app.run(debug=True)