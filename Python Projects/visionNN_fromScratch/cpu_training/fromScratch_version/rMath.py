class Rmath:
    @staticmethod
    # Transpose a vector (convert a row vector to a column vector)
    def vector_transpose(vector: list[int | float]):
        t_vector = []

        for i in range(len(vector)):
            t_vector.append([])
            t_vector[i].append(vector[i])
        return t_vector

    @staticmethod
    # Calculate the outer product of a vector and its transpose
    def vector_product(vector: list[int | float], t_vector: list[list[int | float]]):
        if len(vector) != len(t_vector):
            print("Vector len error")
            return None

        output_vector = []

        for i in range(len(vector)):
            output_vector.append([])
            for j in range(len(vector)):
                output_vector[i].append(vector[i] * t_vector[j][0])
        return output_vector

    @staticmethod
    # Transpose a matrix
    def matrix_transpose(matrix: list[list[int | float]]):
        t_matrix = []

        for i in range(len(matrix[0])):
            t_matrix.append([])
            for j in range(len(matrix)):
                t_matrix[i].append(0)

        counter = 0
        for i in range(len(matrix)):
            for j in range(len(matrix[0])):
                t_matrix[j][counter] = matrix[counter][j]
            counter += 1
        return t_matrix

    @staticmethod
    # Calculate the product of two matrices
    def matrix_product(matrix: list[list[int | float]], t_matrix: list[list[int | float]]):
        if len(matrix[0]) != len(t_matrix):
            print("Matrix shape error!")
            return None

        output_matrix = []
        b = 0

        for i in range(len(matrix)):
            output_matrix.append([])
            for j in range(len(t_matrix[0])):
                for k in range(len(t_matrix)):
                    a = matrix[i][k] * t_matrix[k][j]
                    b += a
                output_matrix[i].append(b)
                b = 0
        return output_matrix

    @staticmethod
    # Calculate the product of two matrices and add a bias vector.
    def matrix_product_with_bias(matrix: list[list[int | float]], t_matrix: list[list[int | float]],
                                 bias_vector: list[int | float]):
        if len(matrix[0]) != len(t_matrix):
            print("Matrix shape error!")
            return None

        output_matrix = []
        b = 0

        for i in range(len(matrix)):
            output_matrix.append([])
            for j in range(len(t_matrix[0])):
                for k in range(len(t_matrix)):
                    a = matrix[i][k] * t_matrix[k][j]
                    b += a
                output_matrix[i].append(b + bias_vector[j])
                b = 0
        return output_matrix

    @staticmethod
    # Subtract one matrix from another
    def matrix_sub(matrix1: list[list[int | float]], matrix2: list[list[int | float]]):
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            print("Matrix shape error!")
            return None

        output_matrix = []

        for i in range(len(matrix1)):
            output_matrix.append([])
            for j in range(len(matrix1[0])):
                output_matrix[i].append(matrix1[i][j] - matrix2[i][j])
        return output_matrix

    @staticmethod
    # Multiply element wise two matrices
    def matrix_mul(matrix1: list[list[int | float]], matrix2: list[list[int | float]]):
        if len(matrix1) != len(matrix2) or len(matrix1[0]) != len(matrix2[0]):
            print("Matrix shape error!")
            return None

        output_matrix = []

        for i in range(len(matrix1)):
            output_matrix.append([])
            for j in range(len(matrix1[0])):
                output_matrix[i].append(matrix1[i][j] * matrix2[i][j])
        return output_matrix

    # Average column sum
    @staticmethod
    def matrix_column_sum(matrix: list[list[int | float]]):
        output_matrix = []

        for i in range(len(matrix[0])):
            column_sum = 0
            for j in range(len(matrix)):
                column_sum += matrix[j][i]
            output_matrix.append(column_sum)
        return output_matrix
