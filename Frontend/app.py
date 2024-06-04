from flask import Flask, render_template, request
import os

app = Flask(__name__)

#activar debugger

'''
ESTO ES PARA QUE EL DEBUGGER SE ACTIVE AUTOMATICAMENTE
============================================================
============================================================
''' 
os.environ['FLASK_DEBUG'] = '1'
'''
============================================================
============================================================
'''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/Cabanas')
def Cabanas():
    return render_template('Cabanas.html')

@app.route('/restaurant')
def restaurant():
    return render_template('restaurant.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/Amapola')
def Amapola():
    return render_template('Cabana_Amapola.html')

@app.route('/Carpincho')
def Carpincho():
    return render_template('Cabana_Carpincho.html')

@app.route('/Ciervo_Blanco')
def Ciervo_Blanco():
    return render_template('Cabana_Ciervo_Blanco.html')

@app.route('/Hierba_Alta')
def Hierba_Alta():
    return render_template('Cabana_Hierba_Alta.html')

@app.route('/Bosque_Alto')
def Bosque_Alto():
    return render_template('Cabana_Bosque_Alto.html')

@app.route('/Trucha_Dorada')
def Trucha_Dorada():
    return render_template('Cabana_Trucha_Dorada.html')

@app.route('/blog_single')
def blog_single():
    return render_template('blog_single.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)