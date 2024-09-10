from flask import Flask, render_template,request,jsonify,Response

import stun,base64,threading,io

upload_pic = [0]
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024
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

@app.route('/list_files')
def list_files():
  return render_template('sending_pic.html')

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

@app.route('/download')
def downloads():
    global upload_pic
    if not upload_pic or not upload_pic[0]:
        return 'no pic', 404
    file_content = upload_pic[0]
    # 获取客户端请求的范围
    range_header = request.headers.get('Range', None)
    if not range_header:
        # 如果没有指定范围，则返回整个文件
        return Response(file_content, mimetype='application/octet-stream')

    # 解析 Range 请求头
    range_start, range_end = parse_range_header(range_header, len(file_content))
    # 创建一个文件对象
    file_stream = io.BytesIO(file_content[range_start:range_end + 1])

    # 设置响应头
    response = Response(file_stream.getvalue(), 206, mimetype='application/octet-stream', direct_passthrough=True)
    response.headers.add('Content-Range', f'bytes {range_start}-{range_end}/{len(file_content)}')
    response.headers.add('Content-Length', str(range_end - range_start + 1))
    response.headers.add('Accept-Ranges', 'bytes')

    return response

def parse_range_header(range_header, file_length):
    # 解析 Range 请求头
    range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
    if range_match:
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_length - 1
        return start, end
    return 0, file_length - 1

