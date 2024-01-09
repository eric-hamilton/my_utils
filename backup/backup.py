import os
import sys
import json
from pathlib import Path
import configparser
import shutil

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    backupables = {}
    for section in config.sections():
        source_path = config.get(section, "source")
        item_type = config.get(section, "type")
        if item_type == "folder":
            copy_all = config.get(section, "copy_all")
            if copy_all == "0":
                copy_all = False
            else:
                copy_all = True
        else:
            copy_all = False
        dest_paths = json.loads(config.get(section, "destinations"))
        backupables[section] = {
            "source_path": source_path,
            "destinations": dest_paths,
            "item_type": item_type,
            "copy_all": copy_all
        }
    return backupables

def backup_item(source, dest, item_type, copy_all):
    if os.path.isdir(dest):
        if item_type == "file":
            shutil.copy2(source, dest)
        elif item_type == "folder":
            if copy_all:
                shutil.copytree(source, dest, dirs_exist_ok=True)
            else:
                src_files = next(os.walk(source), (None, None, []))[2] 
                dst_files = next(os.walk(dest), (None, None, []))[2] 
                files_to_sync = []
                for x in src_files:
                    if x not in dst_files:
                        files_to_sync.append(x)
                total_files = len(files_to_sync)
                for x in files_to_sync:
                    print(f"Copying {x}")
                    shutil.copyfile(os.path.join(source, x), os.path.join(dest,x))
                    total_files -=1
                    if total_files:
                        print(f"{total_files} remaining")
    else:
        return f"Could not find dest: {dest} (source = {source})"

def main(backupables):
    fails = []
    successes = 0
    for name, backup in backupables.items():
        source = backup["source_path"]
        print(name)
        item_type = backup["item_type"]
        copy_all = backup["copy_all"]
        if os.path.exists(source):
            for dest in backup["destinations"]:
                fail_message = backup_item(source, dest, item_type, copy_all)
                if fail_message:
                    fails.append(fail_message)
                else:
                    successes += 1
        else:
            fails.append(f"Could not find source: {source}")
    return successes, fails

if __name__ == '__main__':
    try:
        script_dir = Path(__file__).resolve().parent.parent
        config_path = script_dir.joinpath("data/backup.ini")
        backupables = read_config(config_path)
        successes, fails = main(backupables)
        for fail in fails:
            print(fail)
        else:
            print(f"Backed up {successes} file(s) successfully")
    except Exception as e:
        print(e)
