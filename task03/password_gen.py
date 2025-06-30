# password_generator.py

import random
import string

def generate_password(length, use_letters, use_numbers, use_symbols):
    """
    Generates a random password based on specified criteria.
    """
    # Start with an empty string of possible characters.
    character_pool = ""
    
    # Add character types to the pool based on user's choice.
    if use_letters:
        character_pool += string.ascii_letters  # Adds both lowercase and uppercase letters
    if use_numbers:
        character_pool += string.digits  # Adds numbers 0-9
    if use_symbols:
        character_pool += string.punctuation  # Adds common symbols like !@#$%^&*()

    # If the user selected no character types, we can't generate a password.
    if not character_pool:
        return None

    # Generate the password by randomly choosing characters from the pool.
    # The loop runs 'length' times to build a password of the correct length.
    password_list = [random.choice(character_pool) for _ in range(length)]
    
    # Join the list of characters into a single string.
    return "".join(password_list)

def main():
    """
    Main function to run the password generator. It gets user preferences
    and prints the generated password.
    """
    print("--- Command-Line Password Generator ---")

    # --- Get Password Length ---
    while True:
        try:
            length_str = input("Enter the desired password length (e.g., 12): ")
            length = int(length_str)
            if length > 0:
                break  # Exit the loop if a valid positive number is entered
            else:
                print("Error: Please enter a positive number for the length.")
        except ValueError:
            print("Error: Invalid input. Please enter a whole number.")

    # --- Get Character Type Preferences ---
    # A simple helper function to get a 'yes' or 'no' answer.
    def get_yes_no(prompt):
        while True:
            answer = input(prompt).lower()
            if answer in ["y", "yes"]:
                return True
            elif answer in ["n", "no"]:
                return False
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    while True:
        use_letters = get_yes_no("Include letters (a-z, A-Z)? (y/n): ")
        use_numbers = get_yes_no("Include numbers (0-9)? (y/n): ")
        use_symbols = get_yes_no("Include symbols (!@#$%)? (y/n): ")

        # Check if the user selected at least one character type.
        if use_letters or use_numbers or use_symbols:
            break
        else:
            print("\nError: You must select at least one character type. Please try again.")

    # Generate the password by calling our function with the user's criteria.
    password = generate_password(length, use_letters, use_numbers, use_symbols)

    # Display the final password.
    if password:
        print("\n-------------------------")
        print("  Generated Password:  ")
        print(f"    {password}")
        print("-------------------------")
    # This else block should theoretically not be reached due to the check above,
    # but it's good practice for robustness.
    else:
        print("Could not generate a password with the selected criteria.")


# This standard Python line calls the main() function to start the program.
if __name__ == "__main__":
    main()
