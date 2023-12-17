import hashlib
import argparse
import os
from pathlib import Path
import sys

all_hashes = {}

def get_hash(file_path, chunk_size=4096, hash_algorithm=hashlib.sha256):
    hasher = hash_algorithm()

    with open(file_path, 'rb') as file:
        for chunk in iter(lambda: file.read(chunk_size), b''):
            hasher.update(chunk)

    return hasher.hexdigest()

def print_hash(path, hash_value):
    print(f"{path} > {hash_value}")

def hash_folder(folder_path, recursive, duplicates_only, ignoring):
    global all_hashes
    print(f"Ignoring: {ignoring}")
    skipped = 0

    for file_path in Path(folder_path).rglob('*'):
        if file_path.is_file():
            skip = any(ignored in str(file_path) for ignored in ignoring)
            if not skip:
                hash_value = get_hash(str(file_path))

                if duplicates_only:
                    all_hashes.setdefault(hash_value, []).append(str(file_path))
                else:
                    print_hash(str(file_path), hash_value)
            else:
                skipped += 1

            if not recursive:
                if duplicates_only:
                    
                    dupe_print()
                print(f"Skipped {skipped} files.")
                sys.exit()
    if duplicates_only:
        dupe_print()
    print(f"Skipped {skipped} files.")

def dupe_print():
    global all_hashes
    dupes_found = False

    for hash_value, paths in all_hashes.items():
        if len(paths) > 1:
            dupes_found = True
            print(f"hash: {hash_value} ({len(paths)} dupes found)")
            for path in paths:
                print(path)
            print("") # Add a newline for readability between dupes

    if not dupes_found:
        print("No duplicates found")

def main(current_folder, args):
    if args.folder:
        full_path = os.path.abspath(args.folder)

        if os.path.exists(full_path):
            if os.path.isdir(full_path):
                hash_folder(full_path, args.recursive, args.duplicates_only, args.ignore)
            elif os.path.isfile(full_path):
                print_hash(full_path, get_hash(full_path))
        else:
            print(f"Could not find file/folder: {full_path}")
            sys.exit()
    else:
        full_path = os.getcwd()
        hash_folder(full_path, args.recursive, args.duplicates_only, args.ignore)

if __name__ == "__main__":
    current_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--folder")
    parser.add_argument("-r", "--recursive", action="store_true", help="Hash recursively")
    parser.add_argument("-d", "--duplicates_only", action="store_true", help="Only show duplicates")
    parser.add_argument("-i", "--ignore", nargs='+', default=[], help="Folders to ignore")
    args = parser.parse_args()

    main(current_folder, args)
