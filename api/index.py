from flask import Flask, render_template,request,jsonify

import stun,base64

upload_pic = []
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/picture'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def hello():
    client_ip = request.remote_addr
    client_port = request.environ.get('REMOTE_PORT')
    client_port = request.headers.get('X-Forwarded-Port')
    
    return '你好yyp!\r\n'+str(client_ip)


@app.route('/test')
def test():
  return render_template('upfload.html')

@app.route('/result')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('result.html', result = dict)

@app.route('/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    if file and allowed_file(file.filename):
        filename = file.filename
        global upload_pic
        upload_pic.append(file.read())
        return jsonify({"message": f"File {filename} uploaded successfully."})
    else:
        return jsonify({"error": "Invalid file type."})
@app.route('/list_files')
def list_files():
    global upload_pic
    image_data = upload_pic[0]
    encoded_image=base64.b64encode(image_data).decode('utf-8')
    return render_template('sending_pic.html',image_data=image_data)