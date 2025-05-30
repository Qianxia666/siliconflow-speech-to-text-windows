from flask import Flask, render_template, request, jsonify
import requests
import webbrowser

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    # 从请求中获取数据
    audio_file = request.files.get('audio_file')
    api_endpoint_url = request.form.get('api_endpoint_url')
    api_key = request.form.get('api_key')
    model_name = request.form.get('model_name')

    # 简单的输入验证
    if not all([audio_file, api_endpoint_url, api_key, model_name]):
        return jsonify({"status": "error", "message": "缺少必要的参数"}), 400

    # 验证 URL (基本检查)
    if not api_endpoint_url.startswith(('http://', 'https://')):
        return jsonify({"status": "error", "message": "API 端点 URL 格式不正确"}), 400

    try:
        files = {
            'file': (audio_file.filename, audio_file.stream, audio_file.mimetype)
        }
        payload = {
            'model': model_name
        }
        headers = {
            'Authorization': f'Bearer {api_key}'
        }

        # 调用外部 API
        response = requests.post(api_endpoint_url, files=files, data=payload, headers=headers)

        # 处理外部 API 响应
        if response.status_code == 200:
            try:
                transcription_data = response.json()
                if 'text' in transcription_data:
                    return jsonify({"status": "success", "transcription": transcription_data['text']})
                else:
                    return jsonify({"status": "error", "message": "外部 API 响应中缺少 'text' 字段"}), 500
            except ValueError: # requests.exceptions.JSONDecodeError 继承自 ValueError
                 return jsonify({"status": "error", "message": f"无法解析外部 API 响应为 JSON: {response.text}"}), 500
        else:
            error_message = f"外部 API 返回错误: {response.status_code}."
            try:
                # 尝试解析 API 返回的错误信息
                error_detail = response.json()
                if isinstance(error_detail, dict) and 'message' in error_detail:
                    error_message += f" 详情: {error_detail['message']}"
                elif isinstance(error_detail, dict) and 'detail' in error_detail: # 有些API使用 'detail'
                     error_message += f" 详情: {error_detail['detail']}"
                else:
                    error_message += f" 响应内容: {response.text}"
            except ValueError: # requests.exceptions.JSONDecodeError
                error_message += f" 响应内容: {response.text}"
            return jsonify({"status": "error", "message": error_message}), response.status_code

    except requests.exceptions.RequestException as e:
        return jsonify({"status": "error", "message": f"调用外部 API 时发生连接错误: {str(e)}"}), 500
    except Exception as e:
        # 一般错误处理，可以记录日志 e
        return jsonify({"status": "error", "message": f"处理请求时发生未知错误。"}), 500

if __name__ == '__main__':
    # app.run(debug=True) # 使用 Waitress 替代 Flask 自带的服务器
    from waitress import serve
    # 启动服务器前自动打开浏览器
    webbrowser.open_new("http://localhost:5000") 
    serve(app, host='0.0.0.0', port=5000)