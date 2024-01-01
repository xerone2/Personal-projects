import getpass
import json
from argon2 import PasswordHasher
from cryptography.fernet import Fernet
import base64
from prettytable import PrettyTable

# Initialize PasswordHasher with default parameters
ph = PasswordHasher()

# Initialize Fernet symmetric key for encryption
key = Fernet.generate_key()
cipher_suite = Fernet(key)


def create_new_account():
    master_username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")
    email = input("Enter email (optional): ")
    vault_pin = input("Enter a 4-digit one-time vault pin: ")

    # Validate one-time vault pin format
    if not vault_pin.isdigit() or len(vault_pin) != 4:
        print("Invalid one-time vault pin. It should be a 4-digit number.")
        return

    # Check if the username already exists
    if check_existing_username(master_username):
        print("Username already exists. Choose a different username.")
        return

    # Hash and salt the password using Argon2
    hashed_password = ph.hash(password)

    # Save user details to 'master_key' file
    with open('master_key.json', 'a') as file:
        data = {
            "master_username": master_username,
            "hashed_password": hashed_password,
            "email": email,
            "vault_pin": vault_pin
        }
        json.dump(data, file)
        file.write('\n')

    print("Account created successfully.")


def check_existing_username(username):
    # Check if the username already exists in 'master_key' file
    try:
        with open('master_key.json', 'r') as file:
            for line in file:
                data = json.loads(line)
                if data["master_username"] == username:
                    return True
    except FileNotFoundError:
        return False
    return False


def login():
    master_username = input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # Verify the username and password
    if verify_login(master_username, password):
        print("Login successful.")
        vault_menu(master_username)
    else:
        print("Invalid credentials. Please try again.")


def verify_login(username, password):
    # Verify the username and password using 'master_key' file
    try:
        with open('master_key.json', 'r') as file:
            for line in file:
                data = json.loads(line)
                if data["master_username"] == username and ph.verify(data["hashed_password"], password):
                    return True
    except FileNotFoundError:
        return False
    return False


def vault_menu(master_username):
    while True:
        print("\nVault Menu:")
        print("1. Add Credentials")
        print("2. Show Saved Credentials")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            add_credentials(master_username)
        elif choice == '2':
            show_saved_credentials(master_username)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")


def add_credentials(master_username):
    app_username = input("Enter app username: ")
    app_password = getpass.getpass("Enter app password: ")
    website = input("Enter website/url/app name: ")
    email = input("Enter email (optional): ")

    # Encrypt the password using Fernet symmetric key and base64 encoding
    encrypted_password = base64.b64encode(cipher_suite.encrypt(app_password.encode())).decode()

    # Save credentials to 'vault_key' file
    with open('vault_key.json', 'a') as file:
        data = {
            "master_username": master_username,
            "app_username": app_username,
            "app_password": encrypted_password,
            "website": website,
            "email": email
        }
        json.dump(data, file)
        file.write('\n')

    print("Credentials added successfully.")


def show_saved_credentials(master_username):
    vault_pin = input("Enter a 4-digit one-time vault pin: ")

    # Validate one-time vault pin format
    if not vault_pin.isdigit() or len(vault_pin) != 4:
        print("Invalid one-time vault pin. It should be a 4-digit number.")
        return

    # Verify the one-time vault pin
    if verify_one_time_pin(master_username, vault_pin):
        # Display saved credentials for the given user from 'vault_key' file using PrettyTable
        table = PrettyTable()
        table.field_names = ["App Username", "App Password", "Website/URL/App Name", "Email"]

        with open('vault_key.json', 'r') as file:
            for line in file:
                data = json.loads(line)
                if data["master_username"] == master_username:
                    try:
                        decrypted_password = cipher_suite.decrypt(base64.b64decode(data["app_password"])).decode()
                        table.add_row(
                            [data["app_username"], decrypted_password, data["website"], data.get("email", "N/A")])
                    except Exception as e:
                        print(f"Error decrypting password: {e}")

        print(table)
    else:
        print("Invalid one-time vault pin. Access denied.")


def verify_one_time_pin(username, pin):
    # Verify the one-time vault pin using 'master_key' file
    try:
        with open('master_key.json', 'r') as file:
            for line in file:
                data = json.loads(line)
                if data["master_username"] == username and data["vault_pin"] == pin:
                    return True
    except FileNotFoundError:
        return False
    return False


if __name__ == "__main__":
    while True:
        print("\nPassword Manager Menu:")
        print("1. Create New Account")
        print("2. Login")
        print("3. Quit")
        choice = input("Enter your choice: ")

        if choice == '1':
            create_new_account()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
