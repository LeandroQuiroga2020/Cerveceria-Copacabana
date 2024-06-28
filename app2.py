from flask import Flask, render_template, request, redirect, send_from_directory , session , jsonify
from flask_mysqldb import MySQL 
import MySQLdb
from datetime import datetime
import os


app = Flask(__name__)
app.secret_key='dev'

mysql = MySQL()
mysql.init_app(app)

#app.config['MYSQL_DATABASE_HOST']='localhost'
#app.config['MYSQL_DATABASE_USER']='root'
#app.config['MYSQL_DATABASE_PASSWORD']='12345'
#app.config['MYSQL_DATABASE_DB']='barcopacabana's

#mysql = MySQL(app)
valores= []
preciosAcumulados = []
#precios = []

@app.route('/')
def inicio():
    return render_template('sitio/index.html')

@app.route('/nosotros')
def nosotros():
    return render_template('sitio/nosotros.html')

@app.route('/admin/')
def admin_index():   
    return render_template('admin/index.html')

@app.route('/libros', methods=['POST', 'GET'])
def libros():

    miConexion = MySQLdb.connect( host='localhost', user= 'root', passwd='12345', db='barcopacabana' )
    cur = miConexion.cursor()
    cur.execute("SELECT * FROM `menu`")
    libros=cur.fetchall()  #fetchall trae toda la info que le pedi de la base
    miConexion.commit() 
    #print(libros)
    acum=0
    for i in libros:
      #print(i[3]) #imprime el valor de la comida en este caso que esta en la posicion 3
      #print(i) #imprime todos los valores, todo completo
      acum= acum + i[3]

    


    return render_template('sitio/libros.html', libros=libros, acum=acum)
    
# Ruta para manejar la petición de imprimir un array
@app.route('/procesar_formulario', methods=['POST', 'GET'])
def imprimir_array():
    miConexion = MySQLdb.connect( host='localhost', user= 'root', passwd='12345', db='barcopacabana' )
    cur = miConexion.cursor()
    cur.execute("SELECT * FROM `menu`")
    libros=cur.fetchall()  
    miConexion.commit() 

    sumaMenu= 0

    indice_boton =int(request.form['boton'])
    precios =int(request.form['txtID'])
    print(precios)
    preciosAcumulados.append(precios)
    print(preciosAcumulados)

    print(indice_boton)
   
    valores.append(indice_boton)

    #for precio in precios:     #falta aca como iterar contra que?
    #    sumaMenu = sumaMenu + precios

    #print(sumaMenu)  
    #return f'El índice del botón presionado es: {indice_boton} {libros[indice_boton]}'
    
    for i in preciosAcumulados:
        sumaMenu= sumaMenu + i
    
    
    
    print(valores)
    print(sumaMenu)
    
    return render_template('sitio/libros.html', libros= libros, indice_boton=indice_boton, valores=valores, sumaMenu= sumaMenu)  # falta hacer que imprima dentro de esta direccion

   # return redirect('/libros')


@app.route('/admin/libros', methods=['POST', 'GET'])
def admin_libros():
    
    miConexion = MySQLdb.connect( host='localhost', user= 'root', passwd='12345', db='barcopacabana' )
    cur = miConexion.cursor()
    cur.execute("SELECT * FROM `menu`")
    libros=cur.fetchall()  #fetchall trae toda la info que le pedi de la base
    miConexion.commit() 

    print('------------------------------------------------')
    #print(libros[2])

    print('------------------------------------------------')

    acum=0
    for i in libros:
      #acum = acum + libros[2]
      #print(i[3]) #imprime el valor de la comida en este caso que esta en la posicion 3
      #print(i) #imprime todos los valores, todo completo
      acum= acum + i[3]

    print(acum)

   

    #print(libros) #imprimo todos los librso en consola para probar nomas
    return render_template('admin/libros.html', libros=libros, acum=acum)


@app.route('/admin/libros/guardar', methods=['POST', 'GET'])
def admin_libros_guardar():

    #CS = mysql.connection.cursor()
    #print(CS)

    _nombre=request.form['txtNombre']
    _archivo=request.files['txtImagen']
    _valor=request.form['txtValor']

    print(_nombre)
    print(_archivo)
    print(_valor)
    
    tiempo = datetime.now()
    #print(tiempo)
    horaActual=tiempo.strftime('%Y%H%M%S')  #pido que me muestre año minutos seg....nomasr

    if _archivo.filename != '':
        nuevoNombre= horaActual+'_'+_archivo.filename
        _archivo.save('templates/sitio/img/'+nuevoNombre)

    
    miConexion = MySQLdb.connect( host='localhost', user= 'root', passwd='12345', db='barcopacabana' )
    cur = miConexion.cursor()

    sql="INSERT INTO `menu` (`id`, `nombre`, `imagen`, `precio`) VALUES (NULL, %s,%s,%s);"
    datos=(_nombre,nuevoNombre, _valor)  #_archivo.filename es porque le paso texto, no la imagen en si por ahora

    cur.execute(sql,datos)
    miConexion.commit()  # agrego la sentencia sql a la base

    #array_id = request.form['array_id']  #el eeror esta en que el servidor no lee el name del html
    #print(array_id)
    #if array_id in arrays:
    #    selected_array = arrays[array_id]
    #    return jsonify(selected_array)
    #else:
    #    return jsonify({'error': 'Array not found'})
    
    return redirect('/admin/libros')

if __name__ == '__main__':
    app.run(debug=True)