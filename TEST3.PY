import tkinter as tk
import subprocess
import threading
from tkinter import ttk

def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return process

def filter_rx_tx(log_data):
    filtered_lines = []
    for line in log_data.splitlines():
        if "RX" not in line and "TX" not in line:
            filtered_lines.append(line.strip())
    return "\n".join(filtered_lines)

def start_command():
    selected_command = command_combobox.get()
    com_port = com_port_entry.get()
    
    if selected_command == "Clock":
        command = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.1.0.0.255:2;0.0.1.0.0.255:3"'
    elif selected_command == "Asocisecallocical":
        commands = [
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.40.0.0.255:2;0.0.40.0.0.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.40.0.1.255:2;0.0.40.0.1.255:3"'
        ]
        run_commands_sequentially(commands)
        return
    elif selected_command == "Data":
        commands = [
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.42.0.0.255:2;0.0.42.0.0.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.43.1.2.255:2;0.0.43.1.2.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.43.1.3.255:2;0.0.43.1.3.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.43.1.4.255:2;0.0.43.1.4.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.42.0.5.255:2;0.0.42.0.5.255:3"',
            f'python main.py -S {com_port} -w 1 -f 128 -t Verbose -g "0.0.96.1.0.255:2;0.0.96.1.0.255:3"'
        ]
        run_commands_sequentially(commands)
        return
    elif selected_command == "PC ALL":
        command = f'python main.py -S {com_port} -w 1 -f 128 -t Verbose'
    elif selected_command == "US ALL":
        command = f'python main.py -S {com_port} -c 48 -a High -P wwwwwwwwwwwwwwww -C AuthenticationEncryption -T 7177657274797569 -A 62626262626262626262626262626262 -B 62626262626262626262626262626262 -v 0.0.43.1.3.255 -d India -w 1 -f 128 -t Verbose'
    else:
        return

    terminal_output_text.delete(1.0, tk.END)
    filtered_output_text.delete(1.0, tk.END)
    progress_bar['value'] = 0
    process = run_command(command)
    threading.Thread(target=read_output, args=(process,), daemon=True).start()

def run_commands_sequentially(commands):
    def run_next_command(index):
        if index < len(commands):
            progress_bar['value'] = 0
            
            command = commands[index]
            process = run_command(command)
            threading.Thread(target=read_and_continue, args=(process, commands, index), daemon=True).start()

    def read_and_continue(process, commands, index):
        while True:
            output = process.stdout.readline()
            if output == '' and process.poll() is not None:
                break
            if output:
                log_data = output.strip()
                update_output(log_data)

        update_progress(100)
        if index + 1 < len(commands):
            run_next_command(index + 1)

    run_next_command(0)

def read_output(process):
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            log_data = output.strip()
            update_output(log_data)

    update_progress(100)

def update_output(log_data):
    terminal_output_text.insert(tk.END, log_data + "\n")
    filtered_log = filter_rx_tx(log_data)
    if filtered_log.strip():
        filtered_output_text.insert(tk.END, filtered_log + "\n")
    terminal_output_text.see(tk.END)

def update_progress(value):
    progress_bar['value'] = value

# Create the main window
root = tk.Tk()
root.title("Command Runner")
root.geometry("1000x500")
root.configure(bg='#E0F7FA')

# Frame for the input section
input_frame = tk.Frame(root, bg='#B2EBF2', padx=10, pady=10)
input_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=10)

# Entry for COM port input
com_port_label = tk.Label(input_frame, text="Enter COM Port:", font=('Arial', 12, 'bold'), bg='#B2EBF2', fg='#00796B')
com_port_label.grid(row=0, column=0, padx=5)

com_port_entry = tk.Entry(input_frame, width=20, font=('Arial', 12), bg='white', fg='black')
com_port_entry.grid(row=0, column=1, padx=5)

# Dropdown for command selection
command_label = tk.Label(input_frame, text="Select Command:", font=('Arial', 12, 'bold'), bg='#B2EBF2', fg='#00796B')
command_label.grid(row=0, column=2, padx=5)

command_combobox = ttk.Combobox(input_frame, values=["Clock", "Asocisecallocical", "Data", "PC ALL", "US ALL"], font=('Arial', 12), state="readonly")
command_combobox.grid(row=0, column=3, padx=5)
command_combobox.current(0)

# Button to start command
run_command_button = tk.Button(root, text="Run Command", command=start_command, height=2, width=15, font=('Arial', 12, 'bold'), bg='#FF6F61', fg='white', relief='raised')
run_command_button.grid(row=0, column=4, padx=10)

# Frame for output section
output_frame = tk.Frame(root, bg='#E0F7FA')
output_frame.grid(row=1, column=0, columnspan=5, padx=20, pady=10, sticky="ew")

# Text box for terminal output
terminal_output_text = tk.Text(output_frame, height=20, width=50, font=('Courier New', 10), bg='#FFFFFF', fg='black', wrap=tk.WORD)
terminal_output_text.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

# Text box for filtered output
filtered_output_text = tk.Text(output_frame, height=20, width=50, font=('Courier New', 10), bg='#B2FF59', fg='black', wrap=tk.WORD)
filtered_output_text.pack(side=tk.LEFT, padx=5, fill=tk.BOTH, expand=True)

# Progress bar
progress_bar = ttk.Progressbar(root, orient='horizontal', length=300, mode='determinate')
progress_bar.grid(row=2, column=0, columnspan=5, pady=10)

# Start the GUI event loop
root.mainloop()
