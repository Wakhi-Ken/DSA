#!/usr/bin/env python3
# Import the os module for file path operations
import os

# Define the SparseMatrix class to handle sparse matrix operations
class SparseMatrix:
    # Initialize the SparseMatrix with optional file path or dimensions
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        # Initialize rows, columns, and matrix data dictionary
        self.rows, self.cols, self.matrix_data = 0, 0, {}

        # Load matrix from file if a path is provided
        if matrixFilePath:
            self.load_matrix_from_file(matrixFilePath)
        # Set dimensions if provided
        elif numRows is not None and numCols is not None:
            self.rows, self.cols = numRows, numCols
        # Raise an error if no valid input is provided
        else:
            raise ValueError("You must provide either a file path or dimensions for the matrix.")

    # Load matrix data from a specified file
    def load_matrix_from_file(self, filePath):
        # Check if the file exists
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file {filePath} was not found.")

        # Read the file line by line
        with open(filePath) as file:
            for line in file:
                line = line.strip()
                # Parse the number of rows
                if line.startswith('rows='):
                    self.rows = int(line.split('=')[1])
                # Parse the number of columns
                elif line.startswith('cols='):
                    self.cols = int(line.split('=')[1])
                # Parse matrix entries
                elif line.startswith('(') and line.endswith(')'):
                    try:
                        # Extract row, column, and value from the line
                        currRow, currCol, value = map(int, line[1:-1].split(','))
                        # Set the element if within bounds
                        if 0 <= currRow < self.rows and 0 <= currCol < self.cols:
                            self.setElement(currRow, currCol, value)
                    except ValueError as e:
                        print(f"Error parsing line '{line}': {e}")

    # Retrieve the value at the specified row and column
    def getElement(self, currRow, currCol):
        return self.matrix_data.get((currRow, currCol), 0)

    # Set the value at the specified row and column
    def setElement(self, currRow, currCol, value):
        # Store value in the dictionary if non-zero
        if value != 0:
            self.matrix_data[(currRow, currCol)] = value
        # Remove entry if the value is zero
        elif (currRow, currCol) in self.matrix_data:
            del self.matrix_data[(currRow, currCol)]

    # Add another SparseMatrix to the current one
    def add(self, next):
        # Check for dimension compatibility
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        # Create a new SparseMatrix for the result
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Add current matrix values to the result
        for (row, col), value in self.matrix_data.items():
            result.setElement(row, col, value)

        # Add values from the next matrix
        for (row, col), value in next.matrix_data.items():
            result.setElement(row, col, result.getElement(row, col) + value)

        return result

    # Subtract another SparseMatrix from the current one
    def subtract(self, next):
        # Check for dimension compatibility
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        # Create a new SparseMatrix for the result
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Copy current matrix values to the result
        for (row, col), value in self.matrix_data.items():
            result.setElement(row, col, value)

        # Subtract values from the next matrix
        for (row, col), value in next.matrix_data.items():
            result.setElement(row, col, result.getElement(row, col) - value)

        return result

    # Multiply the current SparseMatrix with another one
    def multiply(self, next):
        # Check for dimension compatibility
        if self.cols != next.rows:
            raise ValueError("The number of columns in the first matrix must equal the number of rows in the second.")

        # Create a new SparseMatrix for the result
        result = SparseMatrix(numRows=self.rows, numCols=next.cols)

        # Efficiently multiply the matrices
        for (i, j), value in self.matrix_data.items():
            for k in range(next.cols):
                result_value = value * next.getElement(j, k)
                # Store the result if non-zero
                if result_value != 0:
                    current_value = result.getElement(i, k)
                    result.setElement(i, k, current_value + result_value)

        return result

    # Save the current SparseMatrix to a file
    def save_to_file(self, resultFilePath):
        # Write rows, columns, and matrix data to the file
        with open(resultFilePath, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n")
            for (row, col), value in self.matrix_data.items():
                file.write(f"({row}, {col}, {value})\n")
        print(f"Result saved to {resultFilePath}")

# Main function to handle user input and operations
def main():
    # Prompt user for the desired action
    action = input("Enter action (Add, Subtract, Multiply): ").strip().lower()

    # Define paths for the input matrix files
    matrix1_path = '../../sample_inputs/easy_sample_02_1.txt'
    matrix2_path = '../../sample_inputs/easy_sample_02_2.txt'

    # List of valid actions
    valid_actions = ['add', 'subtract', 'multiply']

    # Check if the action is valid
    if action not in valid_actions:
        print("Invalid action. Please enter 'Add', 'Subtract', or 'Multiply'.")
        return

    try:
        # Load matrices from specified files
        matrix1 = SparseMatrix(matrixFilePath=matrix1_path)
        matrix2 = SparseMatrix(matrixFilePath=matrix2_path)

        # Perform the requested action and save the result
        if action == "add":
            result = matrix1.add(matrix2)
            result.save_to_file('result_add.txt')
        elif action == "subtract":
            result = matrix1.subtract(matrix2)
            result.save_to_file('result_subtract.txt')
        elif action == "multiply":
            result = matrix1.multiply(matrix2)
            result.save_to_file('result_multiply.txt')

    # Handle file not found error
    except FileNotFoundError as e:
        print(f"Error: The file {e.filename} was not found.")
    # Handle value errors
    except ValueError as e:
        print(f"Error: {e}")
    # Handle any unexpected errors
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Entry point of the script
if __name__ == "__main__":
    main()