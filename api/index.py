from flask import Flask, render_template,request

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
    # 获取客户端 IP 地址
    real_ip = request.headers.get('X-Forwarded-For')
    if not real_ip:
        real_ip = request.remote_addr

    # 尝试从环境变量获取端口号
    remote_port = request.environ.get('REMOTE_PORT')

    if remote_port is None:
        # 如果环境变量中没有端口信息，尝试从 Socket 对象获取
        if 'wsgi.input_terminated' in request.environ:
            # 对于 gunicorn
            sock = request.environ['gunicorn.socket']
        else:
            # 对于 werkzeug 服务器
            sock = request.environ['werkzeug.socket']

        remote_port = sock.getpeername()[1]

    return f"Your IP address is: {real_ip}\nYour port is: {remote_port}"

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)