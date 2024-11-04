import ply.lex as lex
import ply.yacc as yacc
from flask import Flask, render_template, request
import random

app = Flask(__name__)

# Lista de tokens para el analizador léxico
tokens = (
    'APELLIDO_PATERNO', 'APELLIDO_MATERNO', 'NOMBRE',
    'ANIO', 'MES', 'DIA',
    'SEXO', 'ESTADO'
)

# Definición de patrones para los tokens
def t_APELLIDO_PATERNO(t):
    r'[A-Za-z]+'
    t.type = 'APELLIDO_PATERNO'
    return t

def t_APELLIDO_MATERNO(t):
    r'[A-Za-z]+'
    t.type = 'APELLIDO_MATERNO'
    return t

def t_NOMBRE(t):
    r'[A-Za-z]+'
    t.type = 'NOMBRE'
    return t

t_ANIO = r'\d{4}'                       # Cuatro dígitos para el año
t_MES = r'0[1-9]|1[0-2]'                 # Dos dígitos para el mes (01-12)
t_DIA = r'0[1-9]|[12][0-9]|3[01]'        # Dos dígitos para el día (01-31)
t_SEXO = r'[HM]'                         # H para hombre, M para mujer
t_ESTADO = r'AS|BC|BS|CC|CL|CM|CS|CH|DF|DG|GT|GR|HG|JC|MC|MN|MS|NT|NL|OC|PL|QT|QR|SP|SL|SR|TC|TS|TL|VZ|YN|ZS'

# Ignorar espacios y tabulaciones
t_ignore = " \t"

# Función para manejar errores léxicos
def t_error(t):
    print(f"Caracter ilegal: {t.value[0]}")
    t.lexer.skip(1)

# Construcción del analizador léxico
lexer = lex.lex()

# Función para obtener la primera consonante interna de un nombre o apellido
def obtener_primera_consonante_interna(s):
    consonantes = [c for c in s[1:] if c not in 'AEIOU' and c.isalpha()]
    return consonantes[0] if consonantes else ''

# Definición de la gramática para el analizador sintáctico
def p_curp(p):
    '''
    curp : APELLIDO_PATERNO APELLIDO_MATERNO NOMBRE ANIO MES DIA SEXO ESTADO
    '''
    print("CURP válida:")
    print(f"Apellido Paterno: {p[1]}")
    print(f"Apellido Materno: {p[2]}")
    print(f"Nombre: {p[3]}")
    print(f"Año de Nacimiento: {p[4]}")
    print(f"Mes de Nacimiento: {p[5]}")
    print(f"Día de Nacimiento: {p[6]}")
    print(f"Sexo: {p[7]}")
    print(f"Estado de Nacimiento: {p[8]}")

def p_error(p):
    if p:
        print(f"Error de sintaxis en el token: {p.type} con valor {p.value}")
    else:
        print("Error de sintaxis en la CURP")

# Construcción del analizador sintáctico
parser = yacc.yacc()

# Rutas de la aplicación Flask
@app.route("/", methods=["GET", "POST"])
def home():
    return render_template("index.html")

@app.route('/generar-curp', methods=['POST'])
def generar_curp():
    apellido1 = request.form.get('apellido1').upper()
    apellido2 = request.form.get('apellido2').upper()
    nombre = request.form.get('nombre').upper()
    anio = request.form.get('anio')
    mes = request.form.get('mes')
    dia = request.form.get('dia')
    sexo = request.form.get('sexo')
    estado = request.form.get('estado')

    # Validación de campos obligatorios
    if not (apellido1 and apellido2 and nombre and anio and mes and dia and sexo and estado):
        mensaje = "Error: Todos los campos son obligatorios."
        return render_template('resultado_curp.html', mensaje=mensaje)

    # Tomar solo los últimos 2 dígitos del año
    anio_corto = anio[-2:]

    # Generar CURP
    curp = (
        apellido1[0] +  
        next((c for c in apellido1[1:] if c in 'AEIOU'), '') +  
        apellido2[0] +  
        nombre[0] +     
        anio_corto +    
        mes +           
        dia +           
        sexo +          
        estado +        
        obtener_primera_consonante_interna(apellido1) +  
        obtener_primera_consonante_interna(apellido2) +  
        obtener_primera_consonante_interna(nombre) +      
        "{:02d}".format(random.randint(0, 99))  
        #"{:02d}".format(5)
    )

    return render_template('resultado_curp.html', mensaje=curp)  

if __name__ == '__main__':
    app.run(debug=True)
