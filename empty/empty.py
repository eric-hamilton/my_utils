import os

root_dir = os.getcwd()

def remove_empty_folders(path):
    # Walk bottom-up to find nested empty folders
    for subdir, dirs, files in os.walk(path, topdown=False):
        if not dirs and not files:
            try:
                os.rmdir(subdir)
                print(f"Deleted empty folder: {subdir}")
            except Exception as e:
                print(f"Failed to delete {subdir}: {e}")

remove_empty_folders(root_dir)
print("Finished.")
