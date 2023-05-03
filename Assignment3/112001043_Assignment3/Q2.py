from random import uniform
import numpy as np


class RowVectorFloat:
    def __init__(self, initialList) -> None:
        self.entries = initialList
        self.len = len(initialList)

    def __str__(self) -> str:
        if self.len == 0:
            return '[]'
        text = ''
        for i in self.entries:
            text += str(i) + ' '
        return text

    def __len__(self) -> int:
        return self.len

    def __getitem__(self, key):
        return self.entries[key]

    def __setitem__(self, key, value):
        self.entries[key] = value

    def __add__(self, obj):
        if obj.len != self.len:
            raise Exception(
                'Invalid operation; Lengths of vectors must be equal')
        out = []
        for i in range(self.len):
            out.append(self[i] + obj[i])

        return RowVectorFloat(out)

    def __sub__(self, obj):
        if obj.len != self.len:
            raise Exception(
                'Invalid operation; Lengths of vectors must be equal')
        out = []
        for i in range(self.len):
            out.append(self[i] - obj[i])

        return RowVectorFloat(out)

    def __rmul__(self, coef):
        out = []
        for i in self.entries:
            out.append(i*coef)
        return RowVectorFloat(out)

    def __mul__(self, coef):
        out = []
        for i in self.entries:
            out.append(i*coef)
        return RowVectorFloat(out)

    def __truediv__(self, coef):
        out = []
        for i in self.entries:
            out.append(i/coef)
        return RowVectorFloat(out)


class SquareMatrixFloat:
    def __init__(self, n):
        self.dimension = n
        self.squareMatrix = []
        for _ in range(n):
            self.squareMatrix.append(RowVectorFloat([0] * n))

    def __str__(self):
        print('The matrix is:')
        out = ''
        for i in range(self.dimension):
            for j in range(self.dimension):
                out += "{:.2f}".format(self.squareMatrix[i][j]) + ' '
                if i != self.dimension - 1 and j == self.dimension - 1:
                    out += '\n'
        return out

    def sampleSymmetric(self):
        for i in range(self.dimension):
            for j in range(i, self.dimension):
                if i == j:
                    self.squareMatrix[i][j] = uniform(0, self.dimension)
                else:
                    self.squareMatrix[i][j] = self.squareMatrix[j][i] = uniform(
                        0, 1)

    def toRowEchloenForm(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                self.squareMatrix[i][j] /= self.squareMatrix[i][i]

        for i in range(self.dimension):
            if i == self.dimension - 1:
                self.squareMatrix[i][i] = 1
            for j in range(i+1, self.dimension):
                self.squareMatrix[i] = self.squareMatrix[i] / \
                    self.squareMatrix[i][i]
                coef = self.squareMatrix[j][i] / self.squareMatrix[i][i]
                self.squareMatrix[j] = self.squareMatrix[j] - \
                    coef*self.squareMatrix[i]

    def isDRDominant(self):
        for i in range(self.dimension):
            sum = 0
            for j in range(self.dimension):
                if i != j:
                    sum += abs(self.squareMatrix[i][j])
                if sum > abs(self.squareMatrix[i][i]):
                    return False
            if sum > abs(self.squareMatrix[i][i]):
                return False
        return True

    def isDRDominant(self):
        for i in range(self.dimension):
            sum = 0
            for j in range(self.dimension):
                if i != j:
                    sum += abs(self.squareMatrix[j][i])
                if sum > abs(self.squareMatrix[i][i]):
                    return False
            if sum > abs(self.squareMatrix[i][i]):
                return False
        return True

    def jSolve(self, vector, iterations):
        if self.isDRDominant() is False:
            raise Exception(
                'Not solving because convergence is not guaranteed')

        solution = np.zeros_like(vector)
        errors = []

        for iter in range(iterations):
            newSolution = np.zeros_like(vector)
            for i in range(self.dimension):
                newSolution[i] = (vector[i] - np.dot(self.squareMatrix[i][:], solution) +
                                  self.squareMatrix[i][i]*solution[i]) / self.squareMatrix[i][i]
            errors.append(np.linalg.norm(newSolution - solution))
            solution = newSolution

        return errors, solution

    def gSolve(self, vector, iterations):
        if self.isDRDominant() is False:
            raise Exception(
                'Not solving because convergence is not guaranteed')

        solution = np.zeros_like(vector)
        errors = []

        for iter in range(iterations):
            for i in range(self.dimension):
                prevSolution = solution[:]
                solution[i] = (vector[i] - sum(self.squareMatrix[i][j] * solution[j] for j in range(i)) -
                               sum(self.squareMatrix[i][j] * solution[j] for j in range(i+1, self.dimension))) / self.squareMatrix[i][i]
            errors.append(np.linalg.norm(solution - prevSolution))

        return errors, solution


if __name__ == '__main__':
    s = SquareMatrixFloat(4)
    s.sampleSymmetric()
    print(s)
    s.toRowEchloenForm()
    print(s)
    print(s.isDRDominant())
    print(s.jSolve([1, 2, 3, 4], 10))
    print(s.gSolve([1, 2, 3, 4], 10))
