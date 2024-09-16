from flask import Flask, jsonify, send_from_directory, redirect
import subprocess
import os
import json
import re
from flask_cors import CORS

# Flask is a micro web framework written in Python.
# CORS stands for Cross-Origin Resource Sharing. This extension enables cross-origin requests.
# Other imported modules like 'os', 'json', 're', 'subprocess' are standard Python modules for various functionalities like OS interactions, JSON processing, regular expressions, and running subprocesses respectively.

# Create a Flask application instance
app = Flask(__name__, static_url_path='/static', static_folder='static')

# Enable CORS for all routes, allowing requests from any origin
CORS(app, resources={r"/*": {"origins": "*"}})

def error_response(message, status_code, details=None):
    """Standardized error response format."""
    error_data = {
        'status': 'error',
        'message': message,
        'code': status_code,
    }
    
    if details:
        error_data['details'] = details
    
    response = jsonify(error_data)
    response.status_code = status_code
    return response


# Define a route for the root URL ('/')
@app.route('/', methods=['GET'])
def serve_frontend():
    """ Serve the index.html file, which redirects to other HTML files. """
    # Redirects any request to the root URL to the index.html file
    return redirect('/index.html')

# Define a route to serve HTML files
@app.route('/<filename>', methods=['GET'])
def serve_html(filename):
    """ Serve other HTML files based on filename. """
    # Serves files from the same directory as this script, using the provided filename
    return send_from_directory(os.path.dirname(__file__), filename)

# Define a route for the favicon
@app.route('/favicon.ico')
def favicon():
    """ Serve the favicon.ico file. """
    # Serves the favicon.ico file with the specified MIME type
    return send_from_directory(
        os.path.dirname(__file__), 
        'favicon.ico', 
        mimetype='image/vnd.microsoft.icon'
    )

# Define a route to get onboarded charts
@app.route('/getOnboarded', methods=['GET'])
def get_onboarded():
    """ Execute a command to get onboarded charts. """
    try:
        # Executes a subprocess command 'dms_cli get_charts_list'
        curl_process = subprocess.Popen(
            ['dms_cli', 'get_charts_list'],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        result, error = curl_process.communicate()

        if curl_process.returncode != 0:
            return error_response("Failed to retrieve charts list", 500, error)

        return jsonify({'status': 'success', 'data': result}), 200
    except Exception as e:
        return error_response("An unexpected error occurred", 500, str(e))

# Define a route to get deployed pods and parse their output
@app.route('/getDeployed', methods=['GET'])
def get_deployed():
    """ Execute a command to get deployed pods and parse the output. """
    try:
        # Executes the 'kubectl get pods -A' command using subprocess
        curl_process = subprocess.Popen(
            ['kubectl', 'get', 'pods', '-A'],
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output and error from the command
        result, error = curl_process.communicate()

        # Checks if the command execution failed and returns an error if so
        if curl_process.returncode != 0:
            return jsonify({'error': error}), 500

        # Parses the output using regular expressions
        lines = result.split('\n')
        xapp_data = []
        regex = re.compile(r'ricxapp\s+(\S+)\s+(\S+)\s+(\S+)\s+(\S+)')

        for line in lines:
            match = regex.match(line)
            if match:
                xapp_name, status = match.group(1), match.group(3)
                xapp_object = {'xappName': xapp_name, 'status': status}
                xapp_data.append(xapp_object)

        # Returns the parsed data in JSON format
        return jsonify(xapp_data), 200

    except Exception as e:
        # Handles any other exceptions
        return jsonify({'error': str(e)}), 500

# Define a function to extract the IP address for submgr from a given input string
def extract_submgr_ip(input):
    """ Extract the IP address for submgr from the input string. """
    # Splits the input string into lines
    lines = input.split('\n')
    # Iterates through each line
    for line in lines:
        # Looks for 'submgr' in the line
        if 'submgr' in line:
            # Extracts the IP address using a regular expression
            ip_match = re.search(r'\d+\.\d+\.\d+\.\d+', line)
            if ip_match:
                return ip_match.group(0)
    # Returns an empty string if no IP address is found
    return ""

# Define a route to get E2 Nodes information
@app.route('/getE2Nodes', methods=['GET'])
def get_e2nodes():
    """ Get E2 Nodes information by executing a series of commands. """
    try:
        # Executes the 'kubectl get pods -A -o wide' command using subprocess
        curl_process = subprocess.Popen(
            ['kubectl', 'get', 'pods', '-A', '-o', 'wide'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output and error from the command
        wideout, error = curl_process.communicate()

        # Extracts the IP address using the custom function
        output_ip = extract_submgr_ip(wideout)

        # Formulates the next curl command using the extracted IP address
        curl_command = f'curl -X GET http://{output_ip}:8080/ric/v1/get_all_e2nodes'
        curl_process = subprocess.Popen(
            curl_command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output and error from the command
        result, error = curl_process.communicate()

        # Checks if the command execution failed and returns an error if so
        if curl_process.returncode != 0:
            return jsonify({'error': error}), 500

        # Returns the result in JSON format
        return result, 200
    except Exception as e:
        # Handles any other exceptions
        return jsonify({'error': str(e)}), 500
    

    
# Define a route to get ricplt pod information
@app.route('/getpltPods', methods=['GET'])
def get_pltPods():
    """ Get wide info on ricplt pods. """
    try:
        # Executes the 'kubectl get pods -n ricplt -o wide' command using subprocess
        curl_process = subprocess.Popen(
            ['kubectl', 'get', 'pods', '-n', 'ricplt', '-o', 'wide'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output and error from the command
        result, error = curl_process.communicate()

        # Checks if the command execution failed and returns an error if so
        if curl_process.returncode != 0:
            return jsonify({'error': error}), 500

        # Split the lines of the result into a list
        lines = result.split('\n')

        # Remove the last three columns from the header (we say 5 because there are extra words)
        header = lines[0].split()[:-5]

        # Initialize a list to store the modified lines
        modified_lines = [header]

        # Loop through the remaining lines and remove the last three columns
        for line in lines[1:]:
            columns = line.split()[:-3]
            modified_lines.append(columns)

        # Create a formatted string to represent the table
        formatted_table = ''
        for row in modified_lines:
            formatted_table += '\t'.join(row) + '\n'

        # Returns the table
        return formatted_table, 200
    except Exception as e:
        # Handles any other exceptions
        return jsonify({'error': str(e)}), 500


@app.route('/getxappPods', methods=['GET'])
def get_xappPods():
# Define a route to get ricxapp pod information
    """ Get wide info on ricplt pods. """
    try:
        # Executes the 'kubectl get pods -n ricplt -o wide' command using subprocess
        curl_process = subprocess.Popen(
            ['kubectl', 'get', 'pods', '-n', 'ricxapp', '-o', 'wide'], 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output and error from the command
        result, error = curl_process.communicate()

        # Checks if the command execution failed and returns an error if so
        if curl_process.returncode != 0:
            return jsonify({'error': error}), 500

        # Split the lines of the result into a list
        lines = result.split('\n')

        # Remove the last three columns from the header (we say 5 because there are extra words)
        header = lines[0].split()[:-5]

        # Initialize a list to store the modified lines
        modified_lines = [header]

        # Loop through the remaining lines and remove the last three columns
        for line in lines[1:]:
            columns = line.split()[:-3]
            modified_lines.append(columns)

        # Create a formatted string to represent the table
        formatted_table = ''
        for row in modified_lines:
            formatted_table += '\t'.join(row) + '\n'
            
        print(formatted_table)


        # Returns the table
        return formatted_table, 200
    except Exception as e:
        # Handles any other exceptions
        return jsonify({'error': str(e)}), 500


# Define a route to get User Equipment (UE) related information
@app.route('/getUE', methods=['GET'])
def get_ue():
    """ Get User Equipment (UE) related information. """
    try:
        # Executes a curl command to get the policy ID using subprocess
        curl_command = 'curl -s -X GET "http://172.16.80.173:32080/a1mediator/a1-p/policytypes/20008/policies/" | jq .'
        curl_process = subprocess.Popen(
            curl_command, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output of the command
        policy_id, policy_id_error = curl_process.communicate()

        # Parses the JSON response
        policy_json = json.loads(policy_id)
        extracted_policy = policy_json[0]

        # Formulates the next curl command using the extracted policy ID
        get_prb_allocation = f'curl -s -X GET "http://172.16.80.173:32080/a1mediator/a1-p/policytypes/20008/policies/{extracted_policy}" | jq .'

        # Executes the curl command using subprocess
        curl_process = subprocess.Popen(
            get_prb_allocation, 
            shell=True, 
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            universal_newlines=True
        )

        # Captures the output of the command
        result, error = curl_process.communicate()

        # Checks if the command execution failed and returns an error if so
        if curl_process.returncode != 0:
            return jsonify({'error': error}), 500

        # Tries to parse and return the JSON response
        try:
            response_data = json.loads(result)
            ue_rc = response_data.get("ue_rc", [])
            max_prb_values = [entry.get("max_prb") for entry in ue_rc]

            return jsonify({'max_prb_values': max_prb_values}), 200
        except json.JSONDecodeError:
            # Handles JSON parsing errors
            return jsonify({'error': 'Failed to parse JSON response'}), 500

    except Exception as e:
        # Handles any other exceptions
        return jsonify({'error': str(e)}), 500

def run_bash_script(script_path):
    # Function to run your Bash script and capture its output
    try:
        process = subprocess.Popen([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        if process.returncode == 0:
            return {'status': 'success', 'stdout': stdout.decode('utf-8'), 'stderr': ''}
        else:
            return {'status': 'error', 'stdout': '', 'stderr': stderr.decode('utf-8')}
    except Exception as e:
        return {'status': 'error', 'stdout': '', 'stderr': str(e)}

def extract_key_subkey_value(key_line, value_line):
    key_start = key_line.find('"') + 1
    key_end = key_line.find(',', key_start)
    main_key = key_line[key_start:key_end].strip()

    sub_key_start = key_end + 1
    sub_key_end = key_line.find('"', sub_key_start)
    sub_key = key_line[sub_key_start:sub_key_end].strip()

    value_start = value_line.find('"') + 1
    value_end = value_line.rfind('"')
    value = value_line[value_start:value_end]

    return main_key, sub_key, value

def parse_and_organize_data(data_string):
    organized = {}
    lines = data_string.splitlines()

    for i in range(0, len(lines), 3):
        if i + 2 < len(lines):
            key_line = lines[i]
            value_line = lines[i + 2]

            main_key, sub_key, value = extract_key_subkey_value(key_line, value_line)
            
            # Remove brackets from main_key
            main_key = main_key.replace('{', '').replace('}', '')

            # Remove backslashes and quote symbols from the value
            value = value.replace('\\', '').replace('"', '')
            
            # If value is empty or null, set it to "NULL"
            if not value or value.lower() == 'null':
                value = "NULL"
            
            # print(main_key)
            # print(sub_key)
            # print(value)

            # Try to parse the value as JSON, if possible
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                # If not JSON, leave it as is
                pass

            if main_key not in organized:
                organized[main_key] = []
            organized[main_key].append([sub_key, value])
    return organized

@app.route('/accessRedis', methods=['GET'])
def access_redis():
    """ Access and retrieve data from a Redis database using a Bash script. """
    bash_script_path = "./redis.sh"

    try:
        # Run the Bash script and capture its output
        result = run_bash_script(bash_script_path)

        if result['status'] == 'success':
            # Process the output and organize the data
            organized_data = parse_and_organize_data(result['stdout'])
            return jsonify({'data': organized_data}), 200
        else:
            # Return any errors encountered
            return jsonify({'error': result['stderr']}), 500

    except Exception as e:
        # Handle any other exceptions
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    # Run the Flask application on the specified host and port
    app.run(host='0.0.0.0', port=1555)

