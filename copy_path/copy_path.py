import sys
import pyperclip

file_path = sys.argv[1]
style = sys.argv[2]

if style == "forward":
    file_path = file_path.replace("\\", "/")
elif style == "back":
    pass
elif style == "escaped":
    file_path = file_path.replace("\\", "\\\\")
else:
    sys.exit()

pyperclip.copy(file_path)
