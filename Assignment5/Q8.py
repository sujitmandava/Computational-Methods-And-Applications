import scipy.fft as fft


def product(a, b):
    A = []
    B = []

    at, bt = a, b
    numDigits = len(str(a)) + len(str(b))
    for i in range(numDigits):
        A.append(at % 10)
        at //= 10
        B.append(bt % 10)
        bt //= 10

    A = fft.fft(A)
    B = fft.fft(B)

    prod = A*B
    prod = fft.ifft(prod)

    currPow = 0
    result = 0
    for p in prod:
        result += (p.real)*(10**currPow)
        currPow += 1
    return result


if __name__ == "__main__":
    a = 31220334
    b = 442721
    print(f"A = {a}")
    print(f"B = {b}")
    print(f"Computed product using fft: {product(a, b)}")
    print(f"Actual Product: {a * b}")
