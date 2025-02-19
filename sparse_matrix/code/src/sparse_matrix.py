class SparseMatrix:
    def __init__(self, matrixFilePath=None, numRows=None, numCols=None):
        self.rows, self.cols, self.matrix_data = 0, 0, {}

        if matrixFilePath:
            self.load_matrix_from_file(matrixFilePath)
        elif numRows is not None and numCols is not None:
            self.rows, self.cols = numRows, numCols
        else:
            raise ValueError("You must provide either a file path or dimensions for the matrix.")

#Load a sparse matrix from the specified file path.
    def load_matrix_from_file(self, filePath):
        with open(filePath) as file:
            lines = file.readlines()

        self.matrix_data = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith('rows='):
                self.rows = int(line.split('=')[1])
            elif line.startswith('cols='):
                self.cols = int(line.split('=')[1])
            elif line.startswith('(') and line.endswith(')'):
                try:
                    currRow, currCol, value = map(int, line[1:-1].split(','))
                    print(f"Processing: row={currRow}, col={currCol}, value={value}")
                    
                    if currRow < 0 or currRow >= self.rows:
                        raise ValueError(f"Row index out of bounds: {currRow} (max: {self.rows - 1})")
                    if currCol < 0 or currCol >= self.cols:
                        raise ValueError(f"Column index out of bounds: {currCol} (max: {self.cols - 1})")
                    
                    self.setElement(currRow, currCol, value)
                except ValueError as e:
                    raise ValueError(f"Error parsing line '{line}': {e}")

#Return the value at the specified row and column, defaulting to zero if not set.
    def getElement(self, currRow, currCol):
        if not (0 <= currRow < self.rows and 0 <= currCol < self.cols):
            raise ValueError("Row or column index out of bounds.")
        return self.matrix_data.get((currRow, currCol), 0)

#Set the value at the specified row and column in the sparse matrix.
    def setElement(self, currRow, currCol, value):
        if not (0 <= currRow < self.rows and 0 <= currCol < self.cols):
            raise ValueError("Row or column index out of bounds.")

        if value != 0:
            self.matrix_data[(currRow, currCol)] = value
        elif (currRow, currCol) in self.matrix_data:
            del self.matrix_data[(currRow, currCol)]

#Add another sparse matrix to this one and return the result.
    def add(self, next):
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for addition.")

        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        for (row, col), value in self.matrix_data.items():
            result.setElement(row, col, value + next.getElement(row, col))

        for (row, col), value in next.matrix_data.items():
            if (row, col) not in self.matrix_data:
                result.setElement(row, col, value)

        return result

#Subtract another sparse matrix from this one and return the result.
    def subtract(self, next):
        if self.rows != next.rows or self.cols != next.cols:
            raise ValueError("Matrices must have the same dimensions for subtraction.")

        result = SparseMatrix(numRows=self.rows, numCols=self.cols)

        for (row, col), value in self.matrix_data.items():
         result.setElement(row, col, value - next.getElement(row, col))

        for (row, col), value in next.matrix_data.items():
            if (row, col) not in self.matrix_data:
                result.setElement(row, col, -value)

        return result

#Multiply this sparse matrix by another and return the resulting matrix.
    def multiply(self, next):
        if self.cols != next.rows:
         raise ValueError("The number of columns in the first matrix must equal the number of rows in the second.")

        result = SparseMatrix(numRows=self.rows, numCols=next.cols)

        for (i, j), value in self.matrix_data.items():
            for k in range(next.cols):
                result_value = value * next.getElement(j, k)
                if result_value != 0:
                    current_value = result.getElement(i, k)
                    result.setElement(i, k, current_value + result_value)

        return result
        
        return result

#Print the sparse matrix in a human-readable format.
    def easy_to_get(self):
        for row in range(self.rows):
            row_elements = []
        for col in range(self.cols):
            value = self.getElement(row, col)
            row_elements.append(f"({row}, {col}, {value})")
        print(" ".join(row_elements))

def main():
    # Prompt user for the action
    action = input("Enter action (Add, Subtract, Multiply): ").strip().lower()

    # Define file paths for the matrices
    matrix1_path = 'sample_inputs/easy_sample_01_2.txt'
    matrix2_path = 'sample_inputs/easy_sample_01_3.txt'

    try:
        # Load the sparse matrices from the specified files
        matrix1 = SparseMatrix(matrixFilePath=matrix1_path)
        matrix2 = SparseMatrix(matrixFilePath=matrix2_path)

        # Perform the specified action
        if action == "add":
            result = matrix1.add(matrix2)
        elif action == "subtract":
            result = matrix1.subtract(matrix2)
        elif action == "multiply":
            result = matrix1.multiply(matrix2)
        else:
            print("Invalid action")
            return

        # Print the resulting matrix data
        result.easy_to_get()

    except FileNotFoundError as e:
        print(f"Error: The file {e.filename} was not found.")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()