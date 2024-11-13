# /project_folder/app.py

from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# Route to serve the index.html page
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the run command request
@app.route('/run-command', methods=['POST'])
def run_command():
    try:
        # Simulating the execution of the command (you can modify this as needed)
        data = request.get_json()
        comPort = data.get('comPort')
        command = data.get('command')

        print(f"Received command: {command} on COM port: {comPort}")

        # Simulate terminal output
        terminal_output = f"Executed command: {command} on {comPort}"
        filtered_output = f"Filtered output for: {command}"

        # Return simulated result in JSON format
        return jsonify({
            'terminalOutput': terminal_output,
            'filteredOutput': filtered_output
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Route to handle the export to Excel request
@app.route('/export-to-excel', methods=['POST'])
def export_to_excel():
    try:
        # Simulate exporting filtered data to an Excel file
        data = request.get_json()
        filtered_data = data.get('data')

        # Here, you can add actual logic to create and save an Excel file
        # For now, we simulate returning a file (just a placeholder)
        print(f"Exporting data: {filtered_data}")

        # Sending a dummy file for the sake of demonstration
        from io import BytesIO
        import xlsxwriter

        # Create an in-memory Excel file
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()

        worksheet.write(0, 0, "Filtered Data")
        worksheet.write(1, 0, filtered_data)
        workbook.close()

        # Rewind the buffer to the beginning so Flask can send the response
        output.seek(0)

        # Return the Excel file as a response
        return send_file(output, as_attachment=True, download_name="filtered_output.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
