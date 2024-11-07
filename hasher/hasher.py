import hashlib
import argparse
import os
from pathlib import Path
import json

file_hashes = {}


def get_file_hash(file_path, chunk_size=4096, hash_algorithm=hashlib.sha256):
    """Generates a hash for the specified file."""
    hasher = hash_algorithm()
    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def hash_files_in_folder(folder_path, recursive, ignore_dirs, ignore_types):
    """Hashes all files in the specified folder, respecting ignore lists."""
    global file_hashes
    print(f"Ignoring directories: {ignore_dirs}")
    print(f"Ignoring file types: {ignore_types}")
    skipped = 0

    for file_path in Path(folder_path).rglob('*' if recursive else '*.*'):
        if file_path.is_file():
            skip = any(ignored in str(file_path) for ignored in ignore_dirs) or \
                   any(file_path.suffix == ext for ext in ignore_types)

            if not skip:
                hash_value = get_file_hash(str(file_path))
                file_hashes.setdefault(hash_value, []).append(str(file_path))
            else:
                skipped += 1

    print(f"Skipped {skipped} files.")


def filter_duplicates(file_hashes):
    """Returns a dictionary with only duplicate file hashes."""
    return {hash_value: paths for hash_value, paths in file_hashes.items() if len(paths) > 1}


def save_hashes_to_json(file_hashes, output_file="output.json"):
    """Saves the hash dictionary to a JSON file."""
    with open(output_file, 'w') as f:
        json.dump(file_hashes, f, indent=4)
    print(f"File hash information saved to {output_file}")


def main(args):
    output_filename = args.output if args.output else "output.json"
    
    if args.folder:
        full_path = os.path.abspath(args.folder)
        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                # All files
                hash_files_in_folder(full_path, args.recursive, args.ignore, args.ignore_types)
                
                # Remove dupes
                output_data = filter_duplicates(file_hashes) if args.duplicates_only else file_hashes
                save_hashes_to_json(output_data, output_filename)
            elif os.path.isfile(full_path):
                # Single file
                hash_value = get_file_hash(full_path)
                print(f"{full_path} > {hash_value}")
                save_hashes_to_json({hash_value: [full_path]}, output_filename)
        else:
            print(f"Could not find file/folder: {full_path}")
    else:
        # no folder given, just use cwd
        full_path = os.getcwd()
        hash_files_in_folder(full_path, args.recursive, args.ignore, args.ignore_types)
        
        # Remove dupes
        output_data = filter_duplicates(file_hashes) if args.duplicates_only else file_hashes
        save_hashes_to_json(output_data, output_filename)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hash files in a folder and output results to a JSON file.")
    parser.add_argument("-f", "--folder", help="Specify the folder to hash files in.")
    parser.add_argument("-r", "--recursive", action="store_true", help="Recursively hash files in subdirectories")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="List of directories to ignore")
    parser.add_argument("--ignore-types", nargs='+', default=[], help="List of file types to ignore (e.g., .txt, .jpg)")
    parser.add_argument("-o", "--output", help="Specify the output JSON file (default: hash_output.json)")
    parser.add_argument("-d", "--duplicates-only", action="store_true", help="Only log files with duplicate hashes")
    args = parser.parse_args()

    main(args)
