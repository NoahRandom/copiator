import os
import shutil
import json
import tkinter as tk
from tkinter import filedialog

source_folder = None
destination_folder = None

def backup_files_old(source_dir, destination_dir):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist!")
        return

    # Ensure the destination directory exists; if not, create it
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file_path = os.path.join(root, file)

            # Get the relative path of the file and determine its destination path
            relative_path = os.path.relpath(source_file_path, source_dir)
            destination_file_path = os.path.join(destination_dir, relative_path)

            # Create destination folders if they don't exist
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

            # Copy file to destination
            try:
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied: {source_file_path} -> {destination_file_path}")
            except Exception as e:
                print(f"Error: '{e}'")

def backup_files(source_dir, destination_dir, success_log_path='success_log.json', error_log_path='error_log.json'):
    # Ensure the source directory exists
    if not os.path.exists(source_dir):
        print(f"Source directory '{source_dir}' does not exist!")
        return

    # Ensure the destination directory exists
    os.makedirs(destination_dir, exist_ok=True)

    success_log = []
    error_log = []

    # Walk through the source directory
    for root, dirs, files in os.walk(source_dir):
        for file in files:
            source_file_path = os.path.join(root, file)
            relative_path = os.path.relpath(source_file_path, source_dir)
            destination_file_path = os.path.join(destination_dir, relative_path)

            # Create destination subfolders if needed
            os.makedirs(os.path.dirname(destination_file_path), exist_ok=True)

            # Try to copy
            try:
                shutil.copy2(source_file_path, destination_file_path)
                print(f"Copied: {source_file_path} -> {destination_file_path}")
                success_log.append({
                    "source": source_file_path,
                    "destination": destination_file_path
                })
            except Exception as e:
                print(f"Error copying '{source_file_path}': {e}")
                error_log.append({
                    "source": source_file_path,
                    "error": str(e)
                })

    # Save logs
    with open(success_log_path, 'w') as f:
        json.dump(success_log, f, indent=2)

    with open(error_log_path, 'w') as f:
        json.dump(error_log, f, indent=2)

    print(f"\nBackup complete. Successes: {len(success_log)} | Failures: {len(error_log)}")
    print(f"Logs saved to '{success_log_path}' and '{error_log_path}'")

def get_file_sizes(folder):
    """Recursively get file sizes in a folder."""
    file_sizes = {}
    for root, _, files in os.walk(folder):
        for file in files:
            file_path = os.path.relpath(os.path.join(root, file), folder)
            file_sizes[file_path] = os.path.getsize(os.path.join(root, file))
    return file_sizes

def compare_folders(folder1, folder2, output_file = "discrepancies.json"):
    """Compare files and subfolders, checking for missing files and size mismatches."""
    folder1 = source_entry.get()
    folder2 = destination_entry.get()

    files1 = get_file_sizes(folder1)
    files2 = get_file_sizes(folder2)

    only_in_folder1 = list(set(files1.keys()) - set(files2.keys()))
    only_in_folder2 = list(set(files2.keys()) - set(files1.keys()))
    
    size_mismatches = {file: {"folder1_size": files1[file], "folder2_size": files2[file]}
                       for file in files1.keys() & files2.keys() if files1[file] != files2[file]}

    discrepancies = {
        "only_in_folder1": only_in_folder1,
        "only_in_folder2": only_in_folder2,
        "size_mismatches": size_mismatches
    }

    # Save discrepancies to a JSON file
    with open(output_file, "w") as json_file:
        json.dump(discrepancies, json_file, indent=4)

    print(f"Discrepancies saved to {output_file}")

def my_function():
    result_label.config(text="Hello, Tkinter!")

def select_source_folder():
    folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder)

def select_destination_folder():
    folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END)
    destination_entry.insert(0, folder)

def process_folders():
    source = source_entry.get()
    destination = destination_entry.get()
    result_label.config(text=f"Source: {source}\nDestination: {destination}")

def save_folders_to_json(source: str, destination: str, filename="folders_selection.json"):
    data = {
        "source_folder": source,
        "destination_folder": destination
    }
    
    if os.path.exists(filename):
        with open(filename, "r") as json_file:
            existing_data = json.load(json_file)

        if source:
            existing_data['source_folder'] = source
        if destination:
            existing_data['destination_folder'] = destination
        # Update the existing data
        # existing_data.update(data)
        data = existing_data

    with open(filename, "w") as json_file:
        json.dump(data, json_file, indent=4)
    
    print(f"Folders saved/updated in {filename}")

def read_folders_from_json(filename="folders_selection.json"):
    if os.path.exists(filename):
        with open(filename, "r") as json_file:
            data = json.load(json_file)
            source = data.get("source_folder", "Not found")
            destination = data.get("destination_folder", "Not found")
            return source, destination
    else:
        print(f"{filename} does not exist.")
        return None, None

def select_source_folder():
    folder = filedialog.askdirectory()
    source_entry.delete(0, tk.END)
    source_entry.insert(0, folder)
    source_folder = folder

def select_destination_folder():
    folder = filedialog.askdirectory()
    destination_entry.delete(0, tk.END) # deletes from zero to the end
    destination_entry.insert(0, folder)
    destination_folder = folder

def process_folders():
    source = source_entry.get()
    destination = destination_entry.get()
    result_label.config(text=f"Source: {source}\nDestination: {destination}")



# Create the main window
root = tk.Tk()
root.title("Copiator App")

# Configure grid layout. One colum, all space for that column
root.columnconfigure(1, weight=1)

# Source folder selection
source_label = tk.Label(root, text="Source Folder:")
source_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
source_entry = tk.Entry(root, width=50)
# if source_folder:
#     source_entry.insert(0, source_folder)
source_entry.grid(row=0, column=1, padx=10, pady=5)
source_button = tk.Button(root, text="Browse", command=select_source_folder)
source_button.grid(row=0, column=2, padx=10, pady=5)

# Destination folder selection
destination_label = tk.Label(root, text="Destination Folder:")
destination_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
destination_entry = tk.Entry(root, width=50)
# if destination_folder:
#     destination_entry.insert(0, destination_folder)
destination_entry.grid(row=1, column=1, padx=10, pady=5)
destination_button = tk.Button(root, text="Browse", command=select_destination_folder)
destination_button.grid(row=1, column=2, padx=10, pady=5)

# source_folder="C:/Users/Noe/Pictures/copy-test/copy-test-source"
# destination_folder="C:/Users/Noe/Pictures/copy-test/copy-test-destination"
# Process button
process_button = tk.Button(root, text="Copy", command=lambda: backup_files(source_folder, destination_folder))
process_button.grid(row=2, column=1, padx=10, pady=10)

# Compare button
process_button = tk.Button(root, text="Compare", command=lambda: compare_folders(folder1=source_folder, folder2=destination_folder))
process_button.grid(row=2, column=2, padx=10, pady=10)

# Result label
result_label = tk.Label(root, text="")
result_label.grid(row=3, column=1, padx=10, pady=10)

# Run the application
root.mainloop()

