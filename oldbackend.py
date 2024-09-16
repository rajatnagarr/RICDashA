from flask import Flask, jsonify, send_from_directory, redirect
from flask_cors import CORS
import os

app = Flask(__name__, static_url_path='/static', static_folder='static')
CORS(app, resources={r"/*": {"origins": "*"}})

@app.route('/', methods=['GET'])
def serve_frontend():
    return redirect('/index.html')

@app.route('/<filename>', methods=['GET'])
def serve_html(filename):
    return send_from_directory(os.path.dirname(__file__), filename)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
        os.path.dirname(__file__), 
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

@app.route('/getOnboarded', methods=['GET'])
def get_onboarded():
    dummy_result = '{"charts": ["chart1", "chart2", "chart3"]}'
    return dummy_result, 200

@app.route('/getDeployed', methods=['GET'])
def get_deployed():
    dummy_xapp_data = [
        {'xappName': 'xapp1', 'status': 'Running'},
        {'xappName': 'xapp2', 'status': 'Pending'},
        {'xappName': 'xapp3', 'status': 'Running'}
    ]
    return jsonify(dummy_xapp_data), 200

def extract_submgr_ip(input):
    return "192.168.0.1"

@app.route('/getE2Nodes', methods=['GET'])
def get_e2nodes():
    dummy_result = '{"e2nodes": ["node1", "node2", "node3"]}'
    return dummy_result, 200

@app.route('/getpltPods', methods=['GET'])
def get_pltPods():
    dummy_table = 'NAME\tREADY\tSTATUS\tRESTARTS\tAGE\n' \
                 'pod1\t1/1\tRunning\t0\t10d\n' \
                 'pod2\t1/1\tRunning\t1\t5d\n' \
                 'pod3\t0/1\tPending\t0\t1d\n'
    return dummy_table, 200

@app.route('/getxappPods', methods=['GET'])
def get_xappPods():
    dummy_table = 'NAME\tREADY\tSTATUS\tRESTARTS\tAGE\n' \
                 'xapp1\t1/1\tRunning\t0\t10d\n' \
                 'xapp2\t1/1\tRunning\t1\t5d\n' \
                 'xapp3\t0/1\tPending\t0\t1d\n'
    return dummy_table, 200

@app.route('/getUE', methods=['GET'])
def get_ue():
    dummy_max_prb_values = [50, 75, 100]
    return jsonify({'max_prb_values': dummy_max_prb_values}), 200

def run_bash_script(script_path):
    dummy_stdout = 'Dummy output from the Bash script'
    return {'status': 'success', 'stdout': dummy_stdout, 'stderr': ''}

def extract_key_subkey_value(key_line, value_line):
    return "main_key", "sub_key", "value"

def parse_and_organize_data(data_string):
    dummy_organized_data = {
        "key1": [["subkey1", "value1"], ["subkey2", "value2"]],
        "key2": [["subkey3", "value3"], ["subkey4", "value4"]]
    }
    return dummy_organized_data

@app.route('/accessRedis', methods=['GET'])
def access_redis():
    dummy_organized_data = {
        "key1": [
            ["subkey1", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."],
            ["subkey2", '{"name": "John", "age": 30}'],
            ["subkey3", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."]
        ],
        "key2": [
            ["subkey1", "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur."],
            ["subkey2", '{"city": "New York", "country": "USA"}'],
            ["subkey3", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."],
            ["subkey4", "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]
        ],
        "key3": [
            ["subkey1", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."],
            ["subkey2", '{"languages": ["Python", "JavaScript", "Java"]}'],
            ["subkey3", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."],
            ["subkey4", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."],
            ["subkey5", "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."]
        ],
        "key4": [
            ["subkey1", "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat."],
            ["subkey2", '{"email": "example@example.com", "phone": "123-456-7890"}']
        ],
        "key5": [
            ["subkey1", "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."],
            ["subkey2", "Lorem ipsum dolor sit amet, consectetur adipiscing elit."],
            ["subkey3", '{"address": {"street": "123 Main St", "city": "Anytown", "country": "USA"}}']
        ]
    }

    return jsonify({'data': dummy_organized_data}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1555)
