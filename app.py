from typing import IO
from flask import Flask, request, jsonify, send_file, send_from_directory
import subprocess
import os
import pandas as pd
from io import BytesIO  # Add import for BytesIO

app = Flask(__name__)

@app.route('/')
def command_runner_page():
    # Serve the command runner HTML page
    return send_from_directory('static', 'index.html')

@app.route('/connect')
def ble_connect_page():
    # Serve the BLE connection page
    return send_from_directory('static', 'ble_connect.html')

@app.route('/run-command', methods=['POST'])
def run_command():
    data = request.json
    command = data.get('command')
    com_port = data.get('comPort')

    if not com_port:
        return jsonify({"error": "COM port is required"}), 400

    # Construct the command based on the selected command
    if command == "Clock":
        command_str = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.1.0.0.255:2;0.0.1.0.0.255:3"'
    elif command == "Asocisecallocical":
        command_str = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.40.0.0.255:2;0.0.40.0.0.255:3"'
    elif command == "Data":
        command_str = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.42.0.0.255:2;0.0.42.0.0.255:3"'
    elif command == "PC ALL":
        command_str = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose'
    elif command == "US ALL":
        command_str = f'python main.py -S {com_port} -c 48 -a High -P wwwwwwwwwwwwwwww -C AuthenticationEncryption -T 7177657274797569 -A 62626262626262626262626262626262 -B 62626262626262626262626262626262 -v 0.0.43.1.3.255 -d India -w 1 -f 128 -t Verbose'
    elif command == "Energy":
        command_str = f'python main.py -S {com_port} -c 48 -a High -P wwwwwwwwwwwwwwww -C AuthenticationEncryption -T 7177657274797569 -A 62626262626262626262626262626262 -B 62626262626262626262626262626262 -v 0.0.43.1.3.255 -d India -w 1 -f 128 -t Verbose -g "1.0.1.8.0.255:2"'
    else:
        return jsonify({"error": "Unknown command"}), 400

    # Simulate running the command (you can replace this with actual logic)
    process = subprocess.Popen(command_str, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    terminal_output = ""
    filtered_output = ""

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            terminal_output += output
            filtered_output += filter_rx_tx(output, command)

    return jsonify({
        'terminalOutput': terminal_output,
        'filteredOutput': filtered_output
    })

@app.route('/export-to-excel', methods=['POST'])
def export_to_excel():
    data = request.json
    filtered_data = data.get('data').splitlines()

    # Check if there's any filtered data
    if not filtered_data:
        return jsonify({"error": "No data to export"}), 400

    # Create a DataFrame from the filtered data
    df = pd.DataFrame(filtered_data, columns=["Filtered Data"])

    # Save the data to an Excel file in memory
    output = BytesIO()  # Use BytesIO for in-memory file
    df.to_excel(output, index=False)
    output.seek(0)

    # Return the file as an attachment for download
    return send_file(output, mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", as_attachment=True, download_name="filtered_output.xlsx")

def filter_rx_tx(log_data, command):
    # Simple filtering logic based on the command
    # For simplicity, filtering out "RX" and "TX" in this example
    if "RX" not in log_data and "TX" not in log_data:
        return log_data
    return ""

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5500)