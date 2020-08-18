from flask import Flask, request, jsonify, abort
# import some stats library!!

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({ 'message': 'hi' })

if __name__ == '__main__':
    app.run()
