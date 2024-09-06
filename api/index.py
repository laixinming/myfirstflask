from flask import Flask, render_template，request

app = Flask(__name__)


@app.route('/')
def hello():
    client_ip = request.remote_addr
    client_port = request.environ.get('REMOTE_PORT')
    return 'hello lxn'
    return str(client_ip)+':'+str(client_port)


@app.route('/test')
def test():
    return 'Test'

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)