from flask import Flask, render_template,request
import stun

app = Flask(__name__)


@app.route('/')
def hello():
    client_ip = request.remote_addr
    client_port = request.environ.get('REMOTE_PORT')
    client_port = request.headers.get('X-Forwarded-Port')
    
    return '你好yyp!\r\n'+str(client_ip)


@app.route('/test')
def test():
    nat_type,external_ip,external_port=stun.get_ip_info()


    return str(nat_type)+str(external_ip)+str(external_port)

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)