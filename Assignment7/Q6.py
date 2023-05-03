import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad
import math
import random


class Polynomial:
    def __init__(self, coefficients):
        self.coefs = coefficients[:]
        self.degree = max(0, len(self.coefs) - 1)

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
            plt.plot(xp, yp, 'o', color='red')
        plt.title(plotTitle)
        plt.plot(x, y, color='blue', label='Polynomial')
        plt.legend()
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

        fitPolynomial.show(-1, 3, points=points,
                           isMatrixMethod=True, isLagrangeMethod=True)

    def derivative(self):
        d = []
        for i in range(1, len(self.coefs)):
            d.append(self.coefs[i]*i)

        return Polynomial(d)

    def integrate(self):
        integral = [0]
        for i in range(0, len(self.coefs)):
            integral.append(self.coefs[i]/(i+1))

        return Polynomial(integral)

    def area(self, a, b):
        integral = self.integrate()
        area = integral.evaluate(b) - integral.evaluate(a)
        return area

    def __detSin(self, i):
        if i % 8 == 0 or i % 8 == 4:
            return 0
        elif i % 8 == 1 or i % 8 == 3:
            return 1/(2**(1/2))
        elif i % 8 == 2:
            return 1
        elif i % 8 == 5 or i % 8 == 7:
            return (-1)/(2**(1/2))
        elif i % 8 == 6:
            return -1

    def approxArea(self):
        '''
        We use the Taylor series to estimate the function y(x) = exp(x)*sin(x)
        '''
        currFactorial = 1
        approxPolynomial = []
        n = 100

        nList = list(range(1, n+1))
        areaList = []
        actualArea = np.exp(1/2)*(np.sin(1/2) - np.cos(1/2)) - \
            np.exp(0)*(np.sin(0) - np.cos(0))
        actualArea /= 2

        for i in range(n):
            currSin = self.__detSin(i)
            coef = (2**(i/2))*currSin/currFactorial
            approxPolynomial.append(coef)
            if i != 0:
                currFactorial *= (i+1)
            pTemp = Polynomial(approxPolynomial)
            areaList.append(pTemp.area(0, 1/2))

        approxPolynomial = Polynomial(approxPolynomial)
        approxArea = approxPolynomial.area(0, 1/2)
        approximationError = abs(actualArea - approxArea)

        print(f'Actual Area under the curve: {actualArea}')
        print(f"Computed Area using Taylor's Series Expansion: {approxArea}")
        print(f'Approximation error(n = {n}): {approximationError}')

        plt.title('Actual v/s Approximated Area as a function of n')
        plt.plot(nList, areaList, color='blue', label='Approximated area')
        plt.axhline(actualArea, color='red', label='Actual Area')
        plt.legend(loc='best')
        plt.grid()
        plt.show()

    def bestFitPolynomialPoint(self, points, n):
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")

        if type(points) != list or len(points) == 0 or type(points[0]) != tuple:
            raise Exception("points must a list of (x,y) tuples only.")

        for i in range(len(points)):
            if len(points[i]) != 2 or (type(points[i][0]) != int and type(points[i][0]) != float) or (type(points[i][1]) != int and type(points[i][1]) != float):
                raise Exception("points must a list of (x,y) tuples only.")

        m = len(points)
        print(type(points[0]))
        x = [point[0] for point in points]
        y1 = [point[1] for point in points]

        b = []
        for j in range(0, n + 1):
            currSum = 0
            for i in range(m):
                currSum += y1[i] * (x[i] ** j)
            b.append(currSum)

        S = []
        for j in range(0, n + 1):
            currRow = []
            for k in range(0, n + 1):
                currSum = 0
                for i in range(m):
                    currSum += x[i] ** (j + k)
                currRow.append(currSum)
            S.append(currRow)

        A = Polynomial(list(np.linalg.solve(S, b)))

        x2 = np.linspace(min(x), max(x), 1000)
        y2 = [A[xp] for xp in x2]
        plt.title('Best Fit Polynomial')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.plot(x, y1, '.', color='red', label='Points to be fitted')
        plt.plot(x2, y2, color='blue', label='Fitted Polynomial')
        plt.legend()
        plt.grid()
        plt.show()

        return A

    def bestFitPolynomialInterval(self, n):
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")

        x = np.linspace(0, np.pi, 100)
        y = [(np.sin(xp) + np.cos(xp)) for xp in x]

        S = []
        for j in range(0, n+1):
            currRow = []
            for k in range(0, n+1):
                currRow.append(((np.pi)**(j+k+1))/(j+k+1))
            S.append(currRow)

        b = []
        for j in range(0, n+1):
            b.append(
                quad((lambda x: (x**j)*(np.sin(x) + np.cos(x))), 0, np.pi)[0])

        A = Polynomial(list(np.linalg.solve(S, b)))

        x2 = np.linspace(min(x), max(x), 1000)
        y2 = [A[xp] for xp in x2]
        plt.title('Approximating f(x) = sin(x) + cos(x)')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.plot(x, y, '.', color='red',
                 label='Points on f(x)')
        plt.plot(x2, y2, color='blue', label='Approximated Function')
        plt.legend()
        plt.grid()
        plt.show()

        return A

    def nLegendre(self, n):
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")

        coefficient = 1/(math.factorial(n)*(2**n))
        if n == 0:
            p = Polynomial([1])
        else:
            p = Polynomial([-1, 0, 1])

        for i in range(1, n):
            p = p*p

        for i in range(n):
            p = p.derivative()

        p = coefficient*p

        return p

    def _nLegendreFuncS(self, n, power=0):
        # Converts polynomial to a function that can be integrated by quad
        p = self.nLegendre(n)
        for i in range(1, n+power):
            p = p*p
        f = (lambda x: p.evaluate(x))
        return f

    def _nLegendreFuncB(self, n):
        p = self.nLegendre(n)
        for i in range(1, n):
            p = p*p
        f = (lambda x: p.evaluate(x)*np.exp(x))
        return f

    def estimateExp(self, n):
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")

        x = np.linspace(-1, 1, 100)
        y = list(np.exp(xp) for xp in x)

        lPolynomialCoef = []
        for j in range(n+1):
            cj = quad(lambda x: self.nLegendre(
                j)[x] * self.nLegendre(j)[x], -1, 1)[0]
            aj = (1/cj) * \
                (quad(lambda x: self.nLegendre(j)[x]*np.exp(x), -1, 1))[0]
            lPolynomialCoef.append(aj)

        pOut = Polynomial([0])
        for i in range(len(lPolynomialCoef)):
            aj = lPolynomialCoef[i]
            pOut = pOut + (aj*self.nLegendre(i))

        plt.plot(x, y, '.', color='red', label='Actual Points')
        plt.legend()
        pOut.show(-1, 1, 1000)
        return pOut

    def nChebyshev(self, n):
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")

        T0 = Polynomial([1])
        T1 = Polynomial([0, 1])
        T_next = Polynomial([0, 1])

        if n == 0:
            return T0

        if n == 1:
            return T1

        for i in range(2, n+1):
            T_next = Polynomial([0, 2])*T1 - T0
            T0 = Polynomial(T1.coefs)
            T1 = Polynomial(T_next.coefs)

        return T_next

    def verifyChebyshevOrthogonality(self):
        T0 = self.nChebyshev(0)
        T1 = self.nChebyshev(1)
        T2 = self.nChebyshev(2)
        T3 = self.nChebyshev(3)
        T4 = self.nChebyshev(4)

        def w(x): return 1/np.sqrt(1-x**2)

        def f(x, i, j): return w(x) * \
            (self.nChebyshev(i)[x])*(self.nChebyshev(j)[x])

        orthogonalityMatrix = []

        for i in range(5):
            currRow = []
            for j in range(5):
                integral = quad(lambda x: f(x, i, j), -1, 1)[0]
                # print(
                #     f'M[{i}][{j}] = { integral }')
                # Round off really small values
                if integral <= 1e-10:
                    integral = 0
                currRow.append(integral)
            orthogonalityMatrix.append(currRow)

        for row in orthogonalityMatrix:
            print(row)

    def fourierApproximation(self, n=10):
        '''
        Approximates exp(x) using Fourier series in the range [-pi, pi]
        '''
        if type(n) != int or n < 0:
            raise Exception("n must be a non-negative integer.")
        A = []
        B = []

        m = (-1)*math.pi
        M = math.pi

        def Ak(k):
            return (1/math.pi)*(quad(lambda x: ((math.exp(x))*(math.cos(k*x))), m, M)[0])

        def Bk(k):
            return (1/math.pi)*(quad(lambda x: ((math.exp(x))*(math.sin(k*x))), m, M)[0])

        # def evalFourier(p, A, B):
        #     sum = 0
        #     for k in range(1, len(A)):
        #         sum += ((A[k](p))*math.cos(k*p))
        #         sum += ((B[k](p))*math.sin(k*p))
        #     sum += (A[0]/2)
        #     return sum

        for k in range(0, n+1):
            A.append(lambda x: Ak(k))
            B.append(lambda x: Bk(k))

        x = np.linspace(m, M, 100)
        y1 = [math.exp(xp) for xp in x]
        # y2 = [evalFourier(xp, A, B) for xp in x]
        y2 = []
        for xp in x:
            sum = 0
            for k in range(1, len(A)):
                sum += ((Ak(k))*math.cos(k*xp))
                sum += ((Bk(k))*math.sin(k*xp))
            sum += (Ak(0)/2)
            y2.append(sum)

        plt.title('Fourier Approximation')
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.plot(x, y1, color='blue', label='Actual value of f(x)')
        plt.plot(x, y2, color='red',
                 label='Approximated value by Fourier Series')
        plt.legend(loc='best')
        plt.grid()
        plt.show()

    def printRoots(self, eps=1e-3):

        upperBound = 1 + 1 / abs(self.coefs[-1]) * max(
            abs(self.coefs[i]) for i in range(len(self.coefs) - 1)
        )
        lowerBound = abs(self.coefs[0]) / (
            abs(self.coefs[0]) + max(abs(self.coefs[i])
                                     for i in range(1, len(self.coefs)))
        )

        roots = []
        for _ in range(self.degree):
            t = random.uniform(lowerBound, upperBound)
            theta = random.uniform(0, 2 * np.pi)
            root = complex(t * np.cos(theta), t * np.sin(theta))
            roots.append(root)

        sd = self.derivative()

        def converge(roots):
            for root in roots:
                if abs(self[root] / sd[root]) > eps:
                    return False
            return True

        while not converge(roots):
            w = []
            for i in range(self.degree):
                t = self[roots[i]] / sd[roots[i]]
                d = 0
                for j in range(self.degree):
                    if i != j:
                        d += 1 / (roots[i] - roots[j])
                d = 1 - t * d
                wi = t / d
                w.append(wi)

            for i in range(self.degree):
                roots[i] -= w[i]

        return roots


def aberthMethod(A, e=1e-3):
    p = Polynomial([1])
    for a in A:
        p = p*(Polynomial([-a, 1]))
    roots = p.printRoots(eps=e)
    print(roots)
    # print(abs(p[roots[0]]))
    # print(abs(p[roots[1]]))
    # print(abs(p[roots[2]]))
    return roots


if __name__ == "__main__":
    p = Polynomial([])
    # print(p.evaluate(complex(2*np.cos(np.pi/4), 2*np.sin(np.pi/4))))
    roots = aberthMethod([1, 2, 3])
