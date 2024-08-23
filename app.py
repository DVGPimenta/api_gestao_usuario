from flask import Flask
from controller.usuarios_controllers import usuarios_page

app = Flask(__name__)
app.json.sort_keys = False
app.register_blueprint(usuarios_page)


@app.route('/')
def rota():
    return 'Hello Wolrd'


if __name__ == '__main__':
    app.run(debug=True)
