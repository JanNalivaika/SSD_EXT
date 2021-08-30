from flask import Flask
import validate

app = Flask(__name__)

@app.route('/')
def hello_world():
  return 'Hello, Docker!. Call /validate'

@app.route('/validate')
def run_validate():
  validate.run()
  # get files names
  str = "<div><h1>OK</h1></div> <img src='.\data\mulset\set20\90_5.png'/>"
  return str


if __name__ == "__main__":
  app.run(host ='0.0.0.0')