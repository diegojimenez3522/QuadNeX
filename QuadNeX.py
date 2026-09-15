from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
from config import Config


QuadNeXApp   = Flask(__name__)
QuadNeXApp.config.from_object(Config)
db           = MySQL(QuadNeXApp)

@QuadNeXApp.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    QuadNeXApp.run(port=5000)