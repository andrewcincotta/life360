from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World'

@app.route('/hello/<name>')
def hello_name(name):
    newName = name.upper();
    return 'Hello %s!' % newName 

if __name__ == '__main__':
    app.run()