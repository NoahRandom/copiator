import os
import shutil

def backup_files(source_dir, destination_dir):
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
            shutil.copy2(source_file_path, destination_file_path)
            print(f"Copied: {source_file_path} -> {destination_file_path}")

# Example usage
source_directory = input("Source Directory: ")
destination_directory = input("Destination Directory: ")

backup_files(source_directory, destination_directory)