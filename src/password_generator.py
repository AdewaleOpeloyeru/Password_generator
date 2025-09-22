
import secrets
import string
import pyperclip


def get_menu_choice():
    while True:
        print("Choose option:")
        print("1: generate password")
        print("2: exit the program")
        print()
        response = input("Your choice: => ")
        print()
        if response.isdigit() and int(response) in [1, 2]:
            break
        else:
            print("please choose a valid option")
    return int(response)


def get_password_options():
    print("-- Define password properties --")
    while True:
        print()
        response = input("Enter password length (min 8; max 64): ")
        if response.isdigit() and int(response) > 7 and int(response) < 65:
            password_length = int(response)
            break
        else:
            print(
                "Please enter a number greater than 7 and less than 65. To exit the program, press ctrl + c"
            )
    while True:
        print()
        response = input("Use uppercase letters? (y/n): ")
        if response == "y":
            use_uppercase = True
            break
        elif response == "n":
            use_uppercase = False
            break
        else:
            print(
                'Only "y" or "n" are valid responses. To exit the program, press ctrl + c'
            )
    while True:
        print()
        response = input("Use digits? (y/n): ")
        if response == "y":
            use_digits = True
            break
        elif response == "n":
            use_digits = False
            break
        else:
            print(
                'Only "y" or "n" are valid responses. To exit the program, press ctrl + c'
            )
    while True:
        print()
        response = input("Use special characters (!@#$%&^()_+*-=)? (y/n): ")
        if response == "y":
            use_special_characters = True
            break
        elif response == "n":
            use_special_characters = False
            break
        else:
            print(
                'Only "y" or "n" are valid responses. To exit the program, press ctrl + c'
            )
    return password_length, use_uppercase, use_digits, use_special_characters


def generate_password(length, use_uppercase, use_digits, use_special_characters):
    categories = [string.ascii_lowercase]
    required_chars = [secrets.choice(string.ascii_lowercase)]

    if use_uppercase:
        categories.append(string.ascii_uppercase)
        required_chars.append(secrets.choice(string.ascii_uppercase))
    if use_digits:
        categories.append(string.digits)
        required_chars.append(secrets.choice(string.digits))
    if use_special_characters:
        special = "!@#$%&^()_+*-="
        categories.append(special)
        required_chars.append(secrets.choice(special))
    regenerate = "y"
    while regenerate != "n":
        all_characters = "".join(categories)
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [
            secrets.choice(all_characters) for _ in range(remaining_length)
        ]
        secrets.SystemRandom().shuffle(password_chars)
        password = "".join(password_chars)
        # uncomment below line if you want to see the password in the console
        # print("Generated password:", password)
        pyperclip.copy(password)
        print("Password copied to clipboard!")
        regenerate = input("Regenerate password? (y/n). Only 'n' will exit: ")
        return password


def main():
    while True:
        print()
        print("---------- Password generator ----------")
        choice = get_menu_choice()
        if choice == 1:
            options = get_password_options()
            generate_password(*options)
        elif choice == 2:
            print("Bye!")
            break


if __name__ == "__main__":
    main()
