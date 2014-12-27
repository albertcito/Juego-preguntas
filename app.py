from flask import Flask, redirect, url_for,request, Response,render_template,session
from flask import jsonify 
import hashlib
import sys,pprint
import random
import sqlite3

app = Flask(__name__)
app.secret_key="quieres ser millonario => trabaja como negro"


def getCursor():
    conn = sqlite3.connect('proyecto.db')
    c = conn.cursor()
    return c;

@app.route('/',methods=['GET','POST'])
def index():
    error  = ''
    if request.method == 'POST':
        email = request.form['email']
        clave = request.form['clave']
        c = getCursor();
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
            if len(matches) > 0: 
                session['logged_in'] = True
                session['email'] = email
                session['nombre'] = matches[3]

                return redirect('usuarios')
            else:
                error = "Clave erronea."
        else:
            error = "Usuario no existe."

    return render_template('login.html',error=error)

@app.route('/usuarios' )
def form():
    if 'email' not in session: return redirect('')
    
    c = getCursor();
    usuarios = c.execute('select * from usuario')
    return render_template('usuarios.html',usuarios=usuarios,usuario = session['nombre'])

@app.route('/salir')
def salir():
    session.pop('email', None)
    return redirect (url_for('index'))

@app.route('/jugar')
def jugar():
    if 'email' not in session: return redirect('')
    
    c = getCursor();
    result = c.execute('select * from preguntas where etapa_nombre_etapa = "Liceo" limit 1 ')
    pregunta = result.fetchone()
    id_pregunta = pregunta[0]

    result2 = c.execute('select * from alternativa where preguntas_id_pregunta=? limit 3', [id_pregunta])
    alternativa = result2.fetchall()

    etapa = c.execute('select * from etapa order by monto desc');

    return render_template('jugar.html',pregunta=pregunta,alternativa=alternativa,etapa=etapa,usuario = session['nombre'])

@app.route('/_verificar_respuesta')
def _verificar_respuesta():
    respuesta = request.args.get('respuesta')
    etapa = request.args.get('etapa')
    c = getCursor();
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

    resultado = [(res[0])]
    
    if( res[0] == 1):
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
        if resu :
            resultado.append(resu)
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
                limit 1 
                """, 
                [resu[0]]
            )
            pregunta_ = result3.fetchone()
            resultado.append(pregunta_[0])

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
            resultado.append(alternativa)

    return jsonify(result=resultado)


if __name__ == '__main__':
    app.run(debug=True)