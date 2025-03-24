#!/usr/bin/env python3
import os

class SparseMatrix:
    # Initialize the SparseMatrix with optional file path or dimensions
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.rows, self.cols, self.matrix_data = 0, 0, {}

        # Load matrix from file if a file path is provided
        if matrixFilePath:
            self.load_matrix_from_file(matrixFilePath)
        # If dimensions are provided, set them
        elif numRows is not None and numCols is not None:
            self.rows, self.cols = numRows, numCols
        else:
            # Raise an error if neither a file path nor dimensions are provided
            raise ValueError("You must provide either a file path or dimensions for the matrix.")

    # Load matrix data from a specified file
    def load_matrix_from_file(self, filePath):
        # Check if the specified file exists
        if not os.path.exists(filePath):
            raise FileNotFoundError(f"The file {filePath} was not found.")

        # Read the file line by line
        with open(filePath) as file:
            for line in file:
                line = line.strip()
                # Extract number of rows
                if line.startswith('rows='):
                    self.rows = int(line.split('=')[1])
                # Extract number of columns
                elif line.startswith('cols='):
                    self.cols = int(line.split('=')[1])
                # Extract non-zero elements
                elif line.startswith('(') and line.endswith(')'):
                    try:
                        # Parse row, column, and value
                        currRow, currCol, value = map(int, line[1:-1].split(','))
                        # Check if indices are valid
                        if 0 <= currRow < self.rows and 0 <= currCol < self.cols:
                            self.setElement(currRow, currCol, value)
                    except ValueError as e:
                        # Print error if there's an issue parsing the line
                        print(f"Error parsing line '{line}': {e}")

    # Retrieve the value at a specific row and column
    def getElement(self, currRow, currCol):
        return self.matrix_data.get((currRow, currCol), 0)

    # Set the value at a specific row and column
    def setElement(self, currRow, currCol, value):
        if value != 0:
            # Store non-zero values in the matrix
            self.matrix_data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix_data:
            # Remove the element if it's zero
            del self.matrix_data[(currRow, currCol)]

    # Add another SparseMatrix to this one
    def add(self, next):
        # Check if matrices are the same size
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        # Create a result matrix to hold the sum
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Process addition directly
        for (row, col), value in self.matrix_data.items():
            result.setElement(row, col, value)

        # Add values from the second matrix
        for (row, col), value in next.matrix_data.items():
            result.setElement(row, col, result.getElement(row, col) + value)

        return result  # Return the resulting matrix

    # Subtract another SparseMatrix from this one
    def subtract(self, next):
        # Check if matrices are the same size
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        # Create a result matrix to hold the difference
        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        # Process subtraction directly
        for (row, col), value in self.matrix_data.items():
            result.setElement(row, col, value)

        # Subtract values from the second matrix
        for (row, col), value in next.matrix_data.items():
            result.setElement(row, col, result.getElement(row, col) - value)

        return result  # Return the resulting matrix

    # Multiply this SparseMatrix by another
    def multiply(self, next):
        # Check if the matrices can be multiplied
        if self.cols != next.rows:
            raise ValueError("The number of columns in the first matrix must equal the number of rows in the second.")

        # Create a result matrix to hold the product
        result = SparseMatrix(numRows=self.rows, numCols=next.cols)

        # Efficient multiplication
        for (i, j), value in self.matrix_data.items():
            for k in range(next.cols):
                # Calculate the product and accumulate
                result_value = value * next.getElement(j, k)
                if result_value != 0:
                    current_value = result.getElement(i, k)
                    result.setElement(i, k, current_value + result_value)

        return result  # Return the resulting matrix

    # Save the matrix to a specified file
    def save_to_file(self, resultFilePath):
        with open(resultFilePath, 'w') as file:
            file.write(f"rows={self.rows}\n")
            file.write(f"cols={self.cols}\n") 
            for (row, col), value in self.matrix_data.items():
                # Write non-zero elements
                file.write(f"({row}, {col}, {value})\n")
        # Inform the user that the result has been saved
        print(f"Result saved to {resultFilePath}")

def main():
    # Get user input for the desired action
    action = input("Enter action (Add, Subtract, Multiply): ").strip().lower()

    # Define paths for input matrices
    matrix1_path = '../../sample_inputs/easy_sample_02_1.txt'
    matrix2_path = '../../sample_inputs/easy_sample_02_2.txt'

    # Define valid actions
    valid_actions = ['add', 'subtract', 'multiply']

    # Check if the input action is valid
    if action not in valid_actions:
        print("Invalid action. Please enter 'Add', 'Subtract', or 'Multiply'.")
        return

    try:
        # Load the two matrices from files
        matrix1 = SparseMatrix(matrixFilePath=matrix1_path)
        matrix2 = SparseMatrix(matrixFilePath=matrix2_path)

        # Perform the requested action
        if action == "add":
            result = matrix1.add(matrix2
            result.save_to_file('result_add.txt
        elif action == "subtract":
            result = matrix1.subtract(matrix2)  
            result.save_to_file('result_subtract.txt
        elif action == "multiply":
            result = matrix1.multiply(matrix2)
            result.save_to_file('result_multiply.txt')

    except FileNotFoundError as e:
        # Handle file not found error
        print(f"Error: The file {e.filename} was not found.")
    except ValueError as e:
        # Handle value errors (e.g., dimension mismatches)
        print(f"Error: {e}")
    except Exception as e:
        # Handle any other unexpected errors
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()