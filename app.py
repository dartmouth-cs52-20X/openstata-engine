from flask import Flask, request, jsonify, abort
from do import RunStata
# import some stats library!!

app = Flask(__name__)

@app.route('/')
def hello_world():
    return jsonify({ 'message': 'hi - this is our open-stata api!' })

@app.route('/do', methods=['POST'])
def run_do_file():
    if request.method == 'POST':    # check that request is POST
        request_data = request.get_json()   # get the json data
        
        if request_data != None:    # check that there is data
            
            try:
                do_file = request_data['dofile']
            except:
                return jsonify({ 'message': 'error', 'error': 'no .do file in request data'})

            if do_file != None:
                # return jsonify({ 'message': 'running the do file' })
                myStata = RunStata()
                output = myStata.run_do_file(do_file)
                return jsonify({ 'output': output })
            else:
                return jsonify({ 'message': 'error', 'error': 'no .do file'})

        else: 
            return jsonify({ 'message': 'error', 'error': 'no .do file'})
    else:
        return jsonify({ 'message': 'error', 'error': 'Must call POST'})

if __name__ == '__main__':
    app.run()
