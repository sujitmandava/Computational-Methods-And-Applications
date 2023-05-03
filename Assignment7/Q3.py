def f(x, n, a):
    return x**n - a


def computeNthRoot(n, x, e):
    l, h = 0, x

    while abs(h-l) > e:
        c = (l+h)/2
        if f(c, n, x) == 0:
            return c

        if f(c, n, x)*f(l, n, x) >= 0:
            l = c
        else:
            h = c

    return (l+h)/2

if __name__ == "__main__":
    x = 23
    n = 12
    e = 1e-5
    print(f"The {n}th root of {x} is {computeNthRoot(n, x, e)}")
