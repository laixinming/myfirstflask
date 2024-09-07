from flask import Flask, render_template,request,jsonify
import stun,os

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './public/uploads/'
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return jsonify({"message": f"File {filename} uploaded successfully."})
    else:
        return jsonify({"error": "Invalid file type."})
@app.route('/list_files')
def list_files():
    # 如果上传文件夹不存在，则创建它
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
    # 获取当前目录下的 uploads 文件夹路径
    uploads_folder =  './public/uploads/'
    
    # 检查文件夹是否存在
    if not os.path.exists(uploads_folder):
        return jsonify({"error": "Uploads folder does not exist."})
    
    # 列出文件夹中的所有文件
    files = [f for f in os.listdir(uploads_folder) if os.path.isfile(os.path.join(uploads_folder, f))]
    return jsonify({"files": files})