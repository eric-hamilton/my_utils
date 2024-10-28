import os
import shutil
import argparse
import sys

VIDEO_EXTENSIONS = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.m4v']
IMAGE_EXTENSIONS = [
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.tif', '.svg', '.webp',
    '.heif', '.heic', '.raw', '.psd', '.ai', '.eps', '.ico'
]
AUDIO_EXTENSIONS = [
    '.mp3', '.wav', '.aac', '.flac', '.ogg', '.wma', '.m4a', '.alac', '.aiff',
    '.amr', '.opus'
]

def get_type_list(args):
    if args.type:
        if args.type == "video":
            return VIDEO_EXTENSIONS
        elif args.type == "audio":
            return AUDIO_EXTENSIONS
        elif args.type == "image":
            return IMAGE_EXTENSIONS
        else:
            print("Invalid type. Select 'video', 'audio', 'image', or type your own with -e")
            return False
        
    if args.extension:
        return args.extension.split(",")
    else:
        print("Must select a filetype. Use -t for a type or -e to declare extensions.")
        return False


def main(root_dir, extension_list, output_dir, dry_run=False):

    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extension_list):
                file_path = os.path.join(subdir, file)
                
                new_file_name = file
                
                if subdir != output_dir:
                    # If a file with the same name exists in the root directory, rename it
                    if os.path.exists(os.path.join(output_dir, file)):
                        folder_name = os.path.basename(subdir)
                        name, ext = os.path.splitext(file)
                        new_file_name = f"{name}_{folder_name}{ext}"

                    # Move the file to the root directory
                    try:
                        if not dry_run:
                            shutil.move(file_path, os.path.join(output_dir, new_file_name))
                        print(f"Moved: {file_path} -> {os.path.join(output_dir, new_file_name)}")
                    except Exception as e:
                        print(f"Failed to move {file_path}: {e}")

    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Move files of a certain type from within a folder to the root.")
    parser.add_argument("-t", "--type", type=str, 
                        choices=["video", "audio", "image"],
                        help="Types of files to pull.")
    parser.add_argument("-o", "--output", type=str, help="Output directory.")
    parser.add_argument("-e", "--extension", type=str, help="Comma-separated list of file extensions to include (e.g., '.txt,.py').")
    parser.add_argument("-d", "--dry", action="store_true", help="Option to print the output but not move the files.")

    args = parser.parse_args()
    
    type_list = get_type_list(args)
    if not type_list:
            
        sys.exit()
    
    root_dir = os.getcwd()
    output_dir = args.output if args.output else root_dir
    if not os.path.isdir(output_dir):
        print("Output directory could not be found")
        sys.exit()
    
    main(root_dir, type_list, output_dir, args.dry)

    print("Finished moving files.")
