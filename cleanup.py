import os
import argparse
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def create_folder(folder_path):
    """Create a folder if it does not exist."""
    try:
        os.mkdir(folder_path)
        logging.info(f"Folder {folder_path} created.")
    except FileExistsError:
        logging.warning(f"Folder already exists at {folder_path}.")

def move_file(doc, subfolder_path):
    """Move a file to the specified subfolder."""
    try:
        new_doc_path = os.path.join(subfolder_path, os.path.basename(doc))
        os.rename(doc, new_doc_path)
        logging.info(f"Moved file {doc} to {new_doc_path}.")
        return True
    except Exception as e:
        logging.error(f"Error moving file {doc} to {subfolder_path}: {e}")
        return False

def clean_directory(path):
    """Clean up the directory by organizing files into folders based on their extensions."""
    logging.info(f"Cleaning up directory {path}")

    # Get all files from the given directory
    dir_content = os.listdir(path)
    path_dir_content = [os.path.join(path, doc) for doc in dir_content]

    # Filter directory content into documents and folders list
    docs = [doc for doc in path_dir_content if os.path.isfile(doc)]
    folders = [folder for folder in path_dir_content if os.path.isdir(folder)]

    moved = 0

    logging.info(f"Cleaning up {len(docs)} of {len(dir_content)} elements.")
    
    for doc in docs:
        # Separate name from file extension
        _, filetype = os.path.splitext(doc)
        filetype = filetype[1:].lower()  # Remove the dot and convert to lowercase

        # Skip hidden files and the script itself
        if os.path.basename(doc).startswith('.') or os.path.basename(doc) == "directory_cleanup.py":
            continue

        # Get the subfolder name and create folder if it does not exist
        subfolder_path = os.path.join(path, filetype)

        if subfolder_path not in folders:
            create_folder(subfolder_path)

        # Move the file to the new folder
        if move_file(doc, subfolder_path):
            moved += 1

    logging.info(f"Moved {moved} of {len(docs)} files.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Clean up directory and put files into corresponding folders."
    )

    parser.add_argument(
        "--path",
        type=str,
        default=".",
        help="Directory path of the to be cleaned directory",
    )

    # Parse the arguments given by the user and extract the path
    args = parser.parse_args()
    path = args.path

    clean_directory(path)
