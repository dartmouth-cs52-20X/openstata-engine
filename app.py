from flask import Flask, request, jsonify, abort
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
                raw_cmds = request_data['input']
            except: 
            parsed_cmds = request_data['parsed']

            if raw_cmds != None and parsed_cmds != None:
                return jsonify({ 'message': 'running the do file' })
                # output = run_do_file(raw_cmds, parsed_cmds)
            else:
                return jsonify({ 'message': 'error', 'error': 'no .do file'})

        else: 
            return jsonify({ 'message': 'error', 'error': 'no .do file'})

        # return jsonify({ 'message': 'success'})
    else:
        return jsonify({ 'message': 'error', 'error': 'Must call POST'})

if __name__ == '__main__':
    app.run()
