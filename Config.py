import tkinter as tk
from tkinter import filedialog, ttk
import json
import os

def browse_file(entry, file_type="file"):
    if file_type == "directory":
        filename = filedialog.askdirectory()
    else:
        filename = filedialog.askopenfilename()
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
    
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    
    # Write to JSON file
    with open(config_path, 'w') as f:
        json.dump(config, f, indent=4)
    
    window.destroy()

def load_config():
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "config.json")
    
    # Check if config file exists
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)
                
                # Fill the entry fields with loaded values
                api_key_entry.insert(0, config.get("api_key", ""))
                user_id_entry.insert(0, config.get("userId", ""))
                base_folder_entry.insert(0, config.get("base_folder", ""))
                output_path_entry.insert(0, config.get("output_path", ""))
                img_path_entry.insert(0, config.get("img_path", ""))
                texture_pack_entry.insert(0, config.get("texture_pack", ""))
        except json.JSONDecodeError:
            # If the config file is corrupted, just proceed with empty values
            pass

window = tk.Tk()
window.title("Configuration Interface")
window.geometry("600x300")

# API Key
tk.Label(window, text="API Key:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
api_key_entry = tk.Entry(window, width=50)
api_key_entry.grid(row=0, column=1, padx=5, pady=5)

# User ID
tk.Label(window, text="User ID:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
user_id_entry = tk.Entry(window, width=50)
user_id_entry.grid(row=1, column=1, padx=5, pady=5)

# Base Folder
tk.Label(window, text="Base Folder:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
base_folder_entry = tk.Entry(window, width=40)
base_folder_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")
base_folder_button = ttk.Button(window, text="Browse", 
                              command=lambda: browse_file(base_folder_entry, "directory"))
base_folder_button.grid(row=2, column=2, padx=5, pady=5)

# Output Path
tk.Label(window, text="Output Path:").grid(row=3, column=0, padx=5, pady=5, sticky="e")
output_path_entry = tk.Entry(window, width=40)
output_path_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")
output_path_button = ttk.Button(window, text="Browse", 
                              command=lambda: browse_file(output_path_entry, "directory"))
output_path_button.grid(row=3, column=2, padx=5, pady=5)

# Image Path
tk.Label(window, text="Image Path:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
img_path_entry = tk.Entry(window, width=40)
img_path_entry.grid(row=4, column=1, padx=5, pady=5, sticky="w")
img_path_button = ttk.Button(window, text="Browse", 
                           command=lambda: browse_file(img_path_entry, "directory"))
img_path_button.grid(row=4, column=2, padx=5, pady=5)

# Texture Pack
tk.Label(window, text="Texture Pack (.zip):").grid(row=5, column=0, padx=5, pady=5, sticky="e")
texture_pack_entry = tk.Entry(window, width=40)
texture_pack_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")
texture_pack_button = ttk.Button(window, text="Browse", 
                               command=lambda: browse_file(texture_pack_entry))
texture_pack_button.grid(row=5, column=2, padx=5, pady=5)

# Add some padding to the bottom
tk.Label(window, text="").grid(row=6, column=0, pady=10)

# Bind the save_config function to window close
window.protocol("WM_DELETE_WINDOW", save_config)

# Load the config file when the program starts
load_config()

window.mainloop()