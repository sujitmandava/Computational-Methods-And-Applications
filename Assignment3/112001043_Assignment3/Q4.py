import numpy as np
import matplotlib.pyplot as plt


class Polynomial:
    def __init__(self, coefficients):
        self.coefs = coefficients[:]

    def __str__(self) -> str:
        print('Coefficients of the polynomial are:')
        out = ''
        for coef in self.coefs:
            out += str(coef) + ' '
        return out

    def __add__(self, obj):
        n = len(self.coefs)
        m = len(obj.coefs)
        if n < m:
            out = obj.coefs[:]
            for i in range(n):
                out[i] += self.coefs[i]
            return Polynomial(out)
        else:
            out = self.coefs[:]
            for i in range(m):
                out[i] += obj.coefs[i]
            return Polynomial(out)

    def __sub__(self, obj):
        newObj = []
        for coef in obj.coefs:
            newObj.append((-1)*coef)

        out = Polynomial(newObj[:])
        out2 = Polynomial(self.coefs[:])
        return out+out2

    def __rmul__(self, scalar):
        coefs = []
        for coef in self.coefs:
            coefs.append(scalar*coef)
        return Polynomial(coefs)

    def __mul__(self, obj):
        if isinstance(obj, Polynomial):
            newCoefs = [0] * (len(self.coefs) + len(obj.coefs) - 1)
            for i in range(len(self.coefs)):
                for j in range(len(obj.coefs)):
                    newCoefs[i+j] += self.coefs[i] * obj.coefs[j]
            return Polynomial(newCoefs)
        elif isinstance(obj, float) or isinstance(obj, int):
            coefs = []
            for coef in self.coefs:
                coefs.append(obj*coef)
            return Polynomial(coefs)

    def __getitem__(self, n):
        out = 0
        for i in range(len(self.coefs)):
            out += (self.coefs[i])*(n**i)
        return out

    def evaluate(self, n):
        return self[n]

    def show(self, a, b, points=[], isMatrixMethod=False, isLagrangeMethod=False):
        x = np.linspace(a, b, num=1000)
        y = [self.evaluate(xi) for xi in x]
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid()
        plotTitle = 'Plot of the polynomial'
        if isMatrixMethod:
            plotTitle = 'Polynomial interpolation using matrix method'
            if isLagrangeMethod:
                plotTitle = 'Polynomial interpolation using Lagrange method'
            xp, yp = zip(*points)
            plt.plot(xp, yp, 'o', color='red', )
        plt.title(plotTitle)
        plt.plot(x, y, color='blue')
        plt.show()

    def fitViaMatrixMethod(self, points: list):
        n = len(points)
        coefs = np.zeros((n, n))
        vector = np.zeros(n)
        for i in range(n):
            for j in range(n):
                coefs[i][j] = points[i][0]**j
            vector[i] = points[i][1]

        solution = np.linalg.solve(coefs, vector)
        fitPolynomial = Polynomial(list(solution))
        fitPolynomial.show(-1, 3, points=points, isMatrixMethod=True)

    def fitViaLagrangePoly(self, points: list):
        n = len(points)
        fitPolynomial = Polynomial([])

        for i in range(n):
            Y = Polynomial([])
            for j in range(n):
                if j == i:
                    continue
                Z = Polynomial([-points[j][0], 1]) * \
                    (1 / (points[i][0] - points[j][0]))
                if len(Y.coefs) == 0:
                    Y = Z
                else:
                    Y *= Z
            Y *= points[i][1]
            print(Y)
            fitPolynomial += Y

        fitPolynomial.show(-1, 3, points=points, isMatrixMethod=True, isLagrangeMethod=True)


if __name__ == '__main__':
    p = Polynomial([1, 2, 4])
    print(p)

    p1 = Polynomial([1, 2, 3])
    p2 = Polynomial([3, 2, 1])

    p3 = p1 + p2
    print(p3)

    p4 = p1-p2
    print(p4)

    p5 = 3*p1
    print(p5)

    p6 = Polynomial([-1, 1])*Polynomial([1, 1, 1])
    print(p6)

    print(p1)
    p7 = p1[2]
    print(p7)

    p = Polynomial([1, -1, 1, -1])
    p.show(-1, 2)

    q = Polynomial([])
    q.fitViaMatrixMethod([(1, 4), (0, 1), (-1, 0), (2, 15), (3, 12)])

    l = Polynomial([])
    l.fitViaLagrangePoly([(1, -4), (0, 1), (-1, 4), (2, 4), (3, 1)])
