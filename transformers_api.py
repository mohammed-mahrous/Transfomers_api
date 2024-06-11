from flask import Flask , request , send_file
from TransformersProcessor import TransformersProcessor
import time , tempfile


HOST = '10.105.173.89'
PORT = 5000


app = Flask(__name__)
processor = TransformersProcessor()

@app.route('/tts', methods = ['POST'])
def text_to_speech():
    json:dict = request.get_json()
    text = json['text']
    f = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
    start = time.time()
    processor.ProcessAndWriteFile(text,file_path=f.name)
    # print('filePath: {}'.format(f.name))
    end = time.time()
    elapsed = end - start 
    print('elapsed: {}'.format(elapsed))
    response = send_file(f.name, as_attachment=True, download_name='data.wav', mimetype='.wav')
    f.close()
    return response
if __name__ == '__main__':
    # from waitress import serve
    # serve(app, host=HOST, port=PORT)
    app.run(host=HOST,debug=False, port=PORT)