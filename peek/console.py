from msvcrt import getch, setmode
import os
import sys
from key_tables import ascii_chars, special_chars, f_chars

    
def get_key(key_code, key_type="standard"):
    output = None
    if key_type=="standard":
        output = ascii_chars[key_code]
        
    elif key_type=="special":        
        output = special_chars[key_code]
        
    elif key_type=="f":
        output = f_chars[key_code]
    
    if isinstance(output, list):
        output = output[0]
    return output
                
def get_input():
    while True:

        key = ord(getch())
        output = None
        
        if key == 224:
            special_key = ord(getch())
            output = get_key(special_key, key_type="special")
            
        elif key == 0:
            f_key = ord(getch())
            output = get_key(f_key, key_type="f")
            
        else:
            output = get_key(key)
                
        if output:
            return output
        


def get_console_lines():
    return os.get_terminal_size().lines

def get_console_columns():
    return os.get_terminal_size().columns
    
def clear_console():
    os.system('cls')

def clear():
    clear_console()

def move_cursor(row, col):
    print(f"\033[{row};{col}H")

def enable_raw_mode():
    setmode(sys.stdin.fileno(), os.O_BINARY)

def disable_raw_mode():
    setmode(sys.stdin.fileno(), os.O_TEXT)
    
def hide_cursor():
    print("\033[?25l", end="")

def show_cursor():
    print("\033[?25h", end="")
    
def print_at(row, col, text):
    move_cursor(row, col)
    sys.stdout.write(text)
    sys.stdout.flush()    