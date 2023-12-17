import os
import sys
from getpass import getpass
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from editor import Editor
import console
from configparser import ConfigParser


parser = ConfigParser()
def get_file(file_path):
    if os.path.isfile(file_path):
        return file_path
    else:
        sys.exit()

def confirm(message):
    try:
        while True:
            choice = input(f"{message} y/n\n")
            choice = choice.lower()
            if choice in ["yes", "y", "1"]:
                return True
            elif choice in ["no", "n", "0", ""]:
                return False
            else:
                print("Invalid choice.")
    except KeyboardInterrupt:
        sys.exit()

def generate_byte_key(passkey):    
    salt_string = parser.get("CONFIG", "salt")
    salt_bytes = (salt_string.encode("utf-8"))
    salt_bytes_literal = salt_bytes
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        iterations=100000,
        salt=salt_bytes_literal,
        length=32
    )
    key_bytes = kdf.derive(bytes(passkey))
    url_safe_key = base64.urlsafe_b64encode(key_bytes)
    return url_safe_key

def load_from_file(filename):
    with open(filename, 'rb') as file:
        data = bytes(file.read())
        return data

def write_to_file(filename, data):
    with open(filename, 'wb') as file:
        file.write(data)
        
def decrypt_data(encrypted_data, passkey):
    passkey = generate_byte_key(passkey)
    cipher = Fernet(passkey)
    decrypted_data = cipher.decrypt(encrypted_data)
    return decrypted_data
    
def encrypt_data(decrypted_data, passkey):    
    passkey = generate_byte_key(passkey)
    cipher = Fernet(passkey)
    encrypted_data = cipher.encrypt(decrypted_data)
    return encrypted_data

def print_usage_message():
    print("""Usage: 'peek' (optional args)
    help      (prints this message)
    encrypt   (encrypt the data file in place)
    decrypt   (decrypt the data file in place)
    data      (prints the path of the data file)
    config    (prints the path of the config file)""")
    
def get_passkey():
    try:
        while True:
            passkey = getpass(f"Enter passkey")
            if not passkey:
                print("Passkey cannot be empty.")
            else:
                key = bytearray(passkey, 'utf-8')
                return key
    except KeyboardInterrupt:
        sys.exit()
        
if __name__ == "__main__":
    
    
    config_path = os.environ.get("PEEK_CONFIG_PATH")
    if os.path.exists(config_path):
        try:
            parser.read(config_path)
        except Exception as e:
            print(f"Error reading config path: {e}")
            sys.exit()
    else:
        print("No config path found @ \"PEEK_CONFIG_PATH\"")
        sys.exit()
    file_path = parser.get("CONFIG", "default_filepath")

     
    if len(sys.argv) == 2:
        given_arg = sys.argv[1]
        if given_arg == "encrypt":
            command = "encrypt"
            
        elif given_arg == "decrypt":
            command = "decrypt"
            
        elif given_arg == "data":
            print(file_path)
            sys.exit()
            
        elif given_arg == "config":
            print(config_path)
            sys.exit()
            
        elif given_arg == "help":
            print_usage_message()
            sys.exit()
            
        else:
            print_usage_message()
            sys.exit()
            
    elif len(sys.argv) == 1:
        command = "edit"
    else:
        print_usage_message()
        sys.exit()
    
    file_data = load_from_file(file_path)
    passkey = get_passkey()
    if command == "encrypt":
        output_data = encrypt_data(file_data, passkey)
        write_to_file(file_path, output_data)
        sys.exit()
        
    decrypted_data = decrypt_data(file_data, passkey)
    if command == "decrypt":
        write_to_file(file_path, decrypted_data)
        sys.exit()
        
    editor = Editor()
    editor.edit(decrypted_data)
    if editor.changes:
        saving = confirm("Save file?")
        if saving:
            data_to_encrypt = editor.data
            if not isinstance(data_to_encrypt, bytes):
                data_to_encrypt.encode("utf-8")
            print(type(data_to_encrypt), data_to_encrypt)
            output_data = encrypt_data(data_to_encrypt, passkey)
            write_to_file(file_path, output_data)
    
    console.clear()
    
    
        