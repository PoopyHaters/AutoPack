import tkinter as tk
from tkinter import filedialog, ttk, scrolledtext
import json
import os
import subprocess
from tkinter import messagebox
import threading
import queue
import sys

def browse_file(entry, file_type="file"):
    if file_type == "directory":
        filename = filedialog.askdirectory()
    else:
        filename = filedialog.askopenfilename(filetypes=[("ZIP files", "*.zip"), ("All files", "*.*")])
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def save_config():
    config = {
        "api_key": api_key_entry.get(),
        "userId": user_id_entry.get(),
        "base_folder": base_folder_entry.get(),
        "output_path": output_path_entry.get(),
        "img_path": img_path_entry.get(),
        "texture_pack": texture_pack_entry.get()
    }
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)

def load_config():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                api_key_entry.insert(0, config.get("api_key", ""))
                user_id_entry.insert(0, config.get("userId", ""))
                base_folder_entry.insert(0, config.get("base_folder", ""))
                output_path_entry.insert(0, config.get("output_path", ""))
                img_path_entry.insert(0, config.get("img_path", ""))
                texture_pack_entry.insert(0, config.get("texture_pack", ""))
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Failed to load config file: Invalid JSON")

def run_autopack():
    save_config()
    script_dir = os.path.dirname(os.path.abspath(__file__))
    autopack_path = os.path.join(script_dir, "AutoPack.py")
    
    if not os.path.exists(autopack_path):
        messagebox.showerror("Error", "AutoPack.py not found in script directory!")
        return

    console_window = tk.Toplevel(window)
    console_window.title("AutoPack Console")
    console_window.geometry("600x400")
    console_window.configure(bg="#212121")
    
    console_text = scrolledtext.ScrolledText(console_window, width=70, height=20, wrap=tk.WORD, bg="#212121", fg="#ffffff", insertbackground="white")
    console_text.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    
    window.attributes('-disabled', True)
    
    output_queue = queue.Queue()
    running = [True]

    def on_console_close():
        running[0] = False
        window.attributes('-disabled', False)
        console_window.destroy()

    console_window.protocol("WM_DELETE_WINDOW", on_console_close)

    def run_process():
        try:
            env = os.environ.copy()
            env["PYTHONUNBUFFERED"] = "1"
            
            process = subprocess.Popen(
                [sys.executable, autopack_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
                env=env
            )
            
            while running[0]:
                line = process.stdout.readline()
                if not line and process.poll() is not None:
                    break
                if line:
                    output_queue.put(line.strip())
            
            return_code = process.wait()
            if running[0]:
                if return_code == 0:
                    output_queue.put("Process completed successfully!")
                else:
                    output_queue.put(f"Process failed with return code {return_code}")
                    
        except Exception as e:
            if running[0]:
                output_queue.put(f"An error occurred: {str(e)}")
        finally:
            if running[0]:
                output_queue.put(None)

    def update_console():
        try:
            while True:
                line = output_queue.get_nowait()
                if line is None:
                    console_text.configure(state='disabled')
                    window.attributes('-disabled', False)
                    break
                console_text.insert(tk.END, line + '\n')
                console_text.see(tk.END)
        except queue.Empty:
            if running[0]:
                console_window.after(100, update_console)
            else:
                console_text.configure(state='disabled')
                window.attributes('-disabled', False)

    threading.Thread(target=run_process, daemon=True).start()
    console_window.after(100, update_console)

# Create main window
window = tk.Tk()
window.title("Configuration Interface")
window.geometry("800x500")
window.configure(bg="#212121")
window.resizable(False, False)

# Style configuration
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", padding=6, font=('Helvetica', 10), background="#424242", foreground="#ffffff")
style.map("TButton", background=[('active', '#616161')])
style.configure("TLabel", background="#212121", foreground="#ffffff", font=('Helvetica', 10))
style.configure("TEntry", fieldbackground="#303030", foreground="#ffffff", insertbackground="white", background="#212121")
style.configure("TSeparator", background="#424242")
style.configure("TFrame", background="#212121")

# Main frame
main_frame = ttk.Frame(window, padding="20")
main_frame.grid(row=0, column=0, sticky="nsew")
main_frame.configure(style="TFrame")

# Input fields with descriptions
fields = [
    ("API Key:", "api_key_entry", None, "Your authentication key for the API"),
    ("User ID:", "user_id_entry", None, "Your unique user identifier"),
    ("Base Folder:", "base_folder_entry", "directory", "Where your images will be exported"),
    ("Output Path:", "output_path_entry", "directory", "Where FBX files will be saved"),
    ("Image Path:", "img_path_entry", "directory", "Location of your source images"),
    ("Texture Pack:", "texture_pack_entry", "file", "ZIP file containing textures")
]

for i, (label_text, entry_name, file_type, desc) in enumerate(fields):
    ttk.Label(main_frame, text=label_text).grid(row=i*2, column=0, padx=5, pady=(10, 0), sticky="e")
    entry = ttk.Entry(main_frame, width=50)
    entry.grid(row=i*2, column=1, padx=5, pady=(10, 0), sticky="w")
    globals()[entry_name] = entry
    ttk.Label(main_frame, text=desc, font=('Helvetica', 8), foreground="#b0b0b0").grid(row=i*2+1, column=1, padx=5, pady=(0, 10), sticky="w")
    
    if file_type:
        browse_btn = ttk.Button(main_frame, text="Browse", command=lambda e=entry, ft=file_type: browse_file(e, ft))
        browse_btn.grid(row=i*2, column=2, padx=5, pady=(10, 0))

# Separator
ttk.Separator(main_frame, orient="horizontal").grid(row=len(fields)*2, column=0, columnspan=3, sticky="ew", pady=5)  # Reduced from 15 to 5

# Buttons frame
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=len(fields)*2+1, column=0, columnspan=3, pady=5)  # Reduced from 10 to 5
button_frame.configure(style="TFrame")

save_button = ttk.Button(button_frame, text="Save", command=save_config)
save_button.grid(row=0, column=0, padx=10)

create_button = ttk.Button(button_frame, text="Create", command=run_autopack)
create_button.grid(row=0, column=1, padx=10)

# Center the window
window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')

# Load config and start
window.protocol("WM_DELETE_WINDOW", lambda: [save_config(), window.destroy()])
load_config()
window.mainloop()
