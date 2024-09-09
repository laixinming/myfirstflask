from flask import Flask, render_template,request,jsonify

import stun,base64,threading

upload_pic = [0]
app = Flask(__name__)
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

# 用于存储分块数据
chunks = {}

# 锁，用于确保并发安全
lock = threading.Lock()

@app.route('/upload', methods=['POST'])
def upload_chunk():
    # 获取分块文件
    chunk = request.files.get('chunk')
    chunk_index = int(request.form.get('chunkIndex'))
    total_chunks = int(request.form.get('totalChunks'))
    filename = request.form.get('filename')

    # 加锁以确保线程安全
    with lock:
        if filename not in chunks:
            chunks[filename] = [None] * total_chunks

        # 将分块存储到内存中
        chunks[filename][chunk_index] = chunk.read()

    # 检查是否所有分块都已经上传完毕
    if all(chunk is not None for chunk in chunks[filename]):
        # 合并所有分块
        merge_chunks(filename, total_chunks)

    return jsonify({'message': f'分块{chunk_index}上传成功'}), 200

def merge_chunks(filename, total_chunks):
    # 合并分块文件
    with lock:
        file_content = b''.join(chunks[filename])
        del chunks[filename]  # 清理内存

    # 写入最终文件
    upload_pic[0]=file_content

    return jsonify({'message': '文件合并完成'}), 200

@app.route('/list_files')
def list_files():
    global upload_pic
    if not upload_pic or not upload_pic[0]:
        return 'no pic', 404
    
    # 逐块发送图片数据
    image_data = upload_pic[0]
    
    def generate():
        chunk_size = 4096  # 每次发送4KB
        start = 0
        while start < len(image_data):
            end = min(start + chunk_size, len(image_data))
            yield image_data[start:end]
            start = end
    
    # 使用Response对象创建流式响应
    return Response(generate(), mimetype='image/jpeg')