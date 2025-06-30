# bmi_calculator.py

def calculate_bmi(weight_kg, height_m):
    """
    Calculates the Body Mass Index (BMI) using weight in kilograms and height in meters.
    Formula: BMI = weight / (height * height)
    """
    # This check prevents a "division by zero" error if height is 0.
    if height_m <= 0:
        return None
    
    # Calculate and return the BMI value. The ** 2 is for squaring the height.
    return weight_kg / (height_m ** 2)

def classify_bmi(bmi):
    
    """
    Classifies the calculated BMI into standard health categories based on
    common standards.
    """
    if bmi is None:
        return "Invalid input provided."
    elif bmi < 18.5:
        return "Underweight"
    elif 18.5 <= bmi < 25:
        return "Normal weight"
    elif 25 <= bmi < 30:
        return "Overweight"
    else:  # This covers any BMI of 30 or greater
        return "Obesity"

def main():
    """
    This is the main function that runs the program. It handles user interaction,
    calls the other functions, and displays the final output.
    """
    print("--- Command-Line BMI Calculator ---")
    
    # This 'while True' loop will keep asking for input until valid numbers are entered.
    while True:
        try:
            # Step 1: Prompt the user for their weight.
            weight_str = input("\nPlease enter your weight in kilograms (e.g., 70.5): ")
            weight_kg = float(weight_str) # Convert the text input to a number

            # Step 2: Prompt the user for their height.
            height_str = input("Please enter your height in meters (e.g., 1.75): ")
            height_m = float(height_str) # Convert the text input to a number
            
            # Check for non-positive values which are not physically possible.
            if weight_kg <= 0 or height_m <= 0:
                print("Error: Weight and height must be positive numbers. Please try again.")
                continue # This skips the rest of the loop and asks for input again.

            # If the input was valid, break out of the while loop.
            break

        except ValueError:
            # This 'except' block runs if float() fails because the user entered text.
            print("\nError: Invalid input. Please enter numbers only. Let's try that again.")
    
    # Step 3: Calculate the BMI by calling the function we defined earlier.
    bmi_value = calculate_bmi(weight_kg, height_m)
    
    # Step 4: Classify the BMI result by calling the other function.
    bmi_category = classify_bmi(bmi_value)
    
    # Step 5: Display the BMI result and category to the user.
    print("\n--------------------")
    print("      YOUR BMI      ")
    print("--------------------")
    # We use an f-string to format the BMI value to two decimal places (e.g., 22.49)
    print(f"Calculated BMI: {bmi_value:.2f}")
    print(f"Health Category: {bmi_category}")
    print("--------------------")
    print("\nNote: This calculator is for informational purposes for adults.")


# This is a standard Python line that checks if the script is being run directly.
# If it is, it calls our main() function to start the program.
if __name__ == "__main__":
    main()
