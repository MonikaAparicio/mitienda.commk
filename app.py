from flask import Flask, request
from flask.wrappers import Request #request importado para manejar peticiones que llegan al servidor
from flask_sqlalchemy import SQLAlchemy #importada para trabajar de python a SQL bases de datos
from sqlalchemy.orm import session

app = Flask(__name__)
#conexion a la base de datos: 'postgresql://<usuario>:<contraseña>@<direccion de la db>:<puerto>/<nombre de la db>'
app.config['SQLALCHEMY_DATABASE_URI']='postgresql://postgres:root@localhost:5432/mitiendadb2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key ='some-secret-key'

# definiendo la basse de datos en el codigo
db = SQLAlchemy(app)

# importar los modelos de las tablas que cree en el otro archivo
from models import Product, NewUser


#crear el esquema de la base de datos en postgre
db.create_all()
db.session.commit() #guardar los cambios, crea  las tablas


# Rutas del Proyecto, este es como el controlador
# que conecta la vista
# y el modelo, en este caso DB

@app.route('/')
def get_home():
    return 'Aquí va el home' # Home

@app.route('/signup')
def sing_up():
    return # render_template("register.html")'Aqui va el formulario de registro' # Registro

@app.route('/create-user', methods=['POST'])
def create_user():
    email = request.form["email"]
    password = request.form["password"]
    telephone = request.form["telephone"]
    role = request.form["role"]
    name = request.form["name"]
    lastname = request.form["lastname"]
    birthDate = request.form["birthDate"]
    newUser = NewUser(email, password, telephone, role, name, lastname, birthDate)  
    db.session.add(newUser)  
    db.session.commit()
    return "ok"

@app.route('/signin')
def sing_in():
    return 'Aqui va el Acceso' # Acceso

@app.route('/adminstock')
def admin_stock():
    return 'Aqui va el panel del administrar inventario, stock' # Panel de inventario

@app.route('/statistics')
def statistics():
    return 'Aqui va el panel de estadisticas e historial' # Historial y estadisticas

@app.route('/sales')
def sales():
    return 'Aqui va el panel de ventas' # Gestion de ventas de la tienda

@app.route('/purchases')
def purchases():
    return 'Aqui va el panel de compras a proveedores' # Gestion de compra de inventario

@app.route('/admin')
def admin():
    return 'Aqui va el panel del admin' # Panel de administrador

## Rutas de acciones

@app.route('/product', methods = ['GET','POST']) # definir ruta y le dije que acepte post y get una vez cambie datos no me acepta de nuevo

def crud_product(): # metodo, para probar es con postman
    if request.method == 'GET':
        # creo el producto en la db, mientras creamos la html, es uns prueba
        name = "cocacola"
        stock= 35
        measureUnit = "personla"
        codeProduct = 128
        productType = "bebidas"
        brand = "coke"
        date = 25
        price = 2500
        ivaTax = 19
        salePrice = 2800

        entry = Product (name, stock, measureUnit, codeProduct, type, brand, date, price)
        db.session.add(entry)
        db.session.commit()
        
        print('llego un GET')
        return "Esto fue un GET"

    elif request.method == 'POST':
        # Registrar un producto
        request_data = request.form
        #form es el formato en que se envian los datos, request_data es la variable que es un diccionario
        
        name = request_data['name']
        stock= request_data['stock']
        measureUnit = request_data['measureUnit']
        codeProduct = request_data['codeProduct']
        productType = request_data['productType']
        brand = request_data['mark']
        date = request_data['date']
        price = request_data['price']
        ivaTax = request['ivaTax']
        salePrice = request['salePrice']

        # insertar en base de datos el producto

        print ('Producto: ' + name, 'Cantidad: ' + stock, 'Presentacion: ' + measureUnit, 'price: '+ price)
        print ('code: ' + codeProduct, 'productType: ' + productType, 'mark: ' + brand, 'date:'+ date, 'IVA: ' + ivaTax , 'salePrice: ' + salePrice)
        return "Registro Exitoso"

     


@app.route('/section')
def section():
    return "seccion"    
    #return render_template("section.html")

@app.route('/inventary', methods=['POST'])    
def inventary():
    code_product = request.form["code_product"]
    print ("The code product is: ")
    print(code_product)
    return "Inventary"
    #return render_template("inventary.html")

#insertar producto html
#@app.route('/newproducts')
#def newproducts():
    #return render_template("newproducts.html")

@app.route('/create-p', methods=['POST'])
def create_product():
    name = request.form["name"]
    codeproduct = request.form['codeproduct']   
    brand = request.form['brand']   
    productType = request.form['productType']   
    admissionDate = request.form['admissionDate']   
    measureUnit = request.form['measureUnit']   
    ivaTax = request.form['ivaTax']   
    stock = request.form['stock'] 
    # stockmin = request.form['stockmin'] 
    #  amount = request.form['amount'] 
    entry = Product(name, codeproduct, brand, productType, admissionDate, measureUnit, ivaTax, stock)  
    db.session.add(entry)  
    db.session.commit()
    return "ok"

# esto es una prueba de consulta y modificacion

@app.route('/updateproduct')
def update_product():
    old_name ="leche"
    new_name = "leche deslactosada"
    old_product = Product.query.filter_by(name=old_name).first() #esto es una consulta por columna name, el primer campo
    old_product.name = new_name # se cambia el nombre
    db.session.commit()
    return "actualizacion exitosa" 

## aqui consulta la lista de productos
@app.route('/getproducts')
def get_products():
    products = Product.query.all() #para traerlo todo, el producto es un objeto
    print(products[0].name)
    return "trae lista de productos"

#aqui borra productos
@app.route('/deleteproducts')
def delete_product():
    product_name="leche deslactosada"
    product = Product.query.filteer_by(name=product_name).first()
    db.session.delete(product)
    db.session.commit()
    return "Se borro producto"


#merge
