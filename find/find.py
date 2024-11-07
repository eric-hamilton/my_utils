import os
import argparse
import sys

def find_files(base_dir, search_string, include_ext=None, exclude_ext=None, exact_match=False, case_sensitive=False):
    """
    Recursively searches for files containing a specific string in the given directory.
    
    Args:
        base_dir (str): The directory to start the search.
        search_string (str): The string to search for in filenames.
        include_ext (list, optional): List of file extensions to include (e.g., [".txt", ".py"]).
        exclude_ext (list, optional): List of file extensions to exclude (e.g., [".log", ".tmp"]).
        exact_match (bool, optional): Whether to match filenames exactly to search_string.
        case_sensitive (bool, optional): Whether to make the search case-sensitive. Defaults to False.
    """
    found = []
    count=0
    if not case_sensitive:
        search_string = search_string.lower()
    
    for dirpath, _, files in os.walk(base_dir):
        for file_name in files:
            count += 1
            file_path = os.path.join(dirpath, file_name)
            
            # Case sensitivity
            file_name_to_check = file_name if case_sensitive else file_name.lower()
            
            # Check name full or partial
            if (exact_match and file_name_to_check == search_string) or \
               (not exact_match and search_string in file_name_to_check):
                file_ext = os.path.splitext(file_name)[1]
                
                # Include/Exclude file extensions
                if include_ext and file_ext not in include_ext:
                    continue
                if exclude_ext and file_ext in exclude_ext:
                    continue
                
                found.append(file_path)
    if found:
        print("Results:\n")
        for x in found:
            print(x)
        print(f"\nFound {len(found)} matching file(s). Searched: {count}")
    else:
        print(f"Found no matches in {count} files")

def main():
    parser = argparse.ArgumentParser(description="Search for files containing a specific string in filenames.")
    parser.add_argument("search_string", type=str, help="The string to search for in filenames.")
    parser.add_argument("-s", "--search", type=str, help="The string to search for in filenames.")
    parser.add_argument("-i", "--include", type=str, help="Comma-separated list of file extensions to include (e.g., '.txt,.py').")
    parser.add_argument("-e", "--exclude", type=str, help="Comma-separated list of file extensions to exclude (e.g., '.log,.tmp').")
    parser.add_argument("-d", "--directory", type=str, help="Directory to search. Defaults to CWD")
    parser.add_argument("-x", "--exact", action="store_true", help="Require an exact match for the filename.")
    parser.add_argument("-c", "--case", action="store_true", help="Make the search case-sensitive.")
    
    args = parser.parse_args()
    
    include_ext = args.include.split(",") if args.include else None
    exclude_ext = args.exclude.split(",") if args.exclude else None
    
    search_string = args.search if args.search else args.search_string
    
    base_dir = args.directory if args.directory else os.getcwd()
    if not os.path.isdir(base_dir):
        print(f"Could not find directory: {base_dir}")
        return
    
    print(f"Searching {base_dir} for '{search_string}'...")
    find_files(base_dir, search_string, include_ext, exclude_ext, exact_match=args.exact, case_sensitive=args.case)

if __name__ == "__main__":
    main()
