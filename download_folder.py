import zipfile
import os
import sys

def zip_folder(folder_path, output_path):
    with zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                zipf.write(file_path, os.path.relpath(file_path, folder_path))

if __name__ == '__main__':
    # Check if the correct number of command-line arguments is provided
    if len(sys.argv) != 3:
        print("Usage: python download_folder.py [folder_path] [output_path]")
    else:
        # Get the folder path and output path from command-line arguments
        folder_path = sys.argv[1]
        output_path = sys.argv[2]

        # Call the function to create the ZIP archive
        zip_folder(folder_path, output_path)
