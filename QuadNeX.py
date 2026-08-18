from flask import Flask

QuadNeXApp   = Flask(__name__)

@QuadNeXApp.route('/')
def home():
    return '<h1>hello world</h1>'

if __name__ == '__main__':
    QuadNeXApp.run(port=5000, debug=True)