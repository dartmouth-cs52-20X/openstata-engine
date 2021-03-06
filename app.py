from flask import Flask, request, jsonify, abort
from flask_cors import CORS, cross_origin
from do import RunStata, handleTutorials
# import some stats library!!

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route("/")
@cross_origin()
def hello_world():
    return jsonify({ 'message': 'hi - this is our open-stata api!' })

@app.route("/do", methods=['POST'])
@cross_origin(origins="https://open-stata.herokuapp.com/*", methods=['POST'])
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
                output,logfiles = myStata.run_do_file(do_file)

                try:
                    tid = request_data['tutorialID']
                except:
                    p = 0
                    
                if tid!=None:
                    try:
                        tutorial_result = handleTutorials(tid, do_file)
                    except:
                        output.append('Tutorial ungradeable. Sorry!')
                    
                    if tutorial_result[0]==0:
                        output.append(tutorial_result[1])

                return jsonify({ 'output': output, 'logfiles': logfiles })
            else:
                return jsonify({ 'message': 'error', 'error': 'no .do file'})

        else: 
            return jsonify({ 'message': 'error', 'error': 'no .do file'})
    else:
        return jsonify({ 'message': 'error', 'error': 'Must call POST'})

if __name__ == '__main__':
    app.run()
