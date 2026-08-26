from flask import Flask, render_template, request, redirect, url_for

QuadNeXApp   = Flask(__name__)

@QuadNeXApp.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    QuadNeXApp.run(port=5000, debug=True)