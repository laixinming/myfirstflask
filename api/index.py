from flask import Flask, render_template,request
import stun

app = Flask(__name__)


@app.route('/')
def hello():
    client_ip = request.remote_addr
    client_port = request.environ.get('REMOTE_PORT')
    if client_port!=None:
        environ = request.environ
        if 'wsgi.input_terminated' in environ:
             # 在某些 WSGI 服务器中，如 gunicorn
            sock = environ['gunicorn.socket']
        else:
            # 在其他服务器中
            sock = environ['werkzeug.socket']

        client_address = sock.getpeername()
        remote_port = client_address[1]
        client_port = remote_port
    return str(client_ip)+':'+str(client_port)


@app.route('/test')
def test():
    nat_type,external_ip,external_port=stun.get_ip_info()


    return nat_type,exteenal_ip,external_port

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)