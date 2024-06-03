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

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

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

@app.route('/rooms_single')
def rooms_single():
    return render_template('rooms_single.html')

@app.route('/Cabana_Lujosa')
def Cabana_Lujosa():
    return render_template('Cabana_Lujosa.html')

@app.route('/blog_single')
def blog_single():
    return render_template('blog_single.html')