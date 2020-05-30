# Python program to implement Runge Kutta method
# A sample differential equation "dy / dx = (x - y)/2"
def dydx(x, y):
    return ((x - y) / 2)


import math


def dydx2(x, y):
    return (math.sin(x - y) / 2)


Y = []
X = []


# Finds value of y for a given x using step size h
# and initial value y0 at x0.
def rungeKutta(dydxfunc, x0, y0, x, h):
    # Count number of iterations using step size or
    # step height h
    n = (int)((x - x0) / h)
    # Iterate for number of iterations
    y = y0
    Y.append(y)
    X.append(x0)
    for i in range(1, n + 1):
        "Apply Runge Kutta Formulas to find next value of y"
        k1 = h * dydxfunc(x0, y)
        k2 = h * dydxfunc(x0 + 0.5 * h, y + 0.5 * k1)
        k3 = h * dydxfunc(x0 + 0.5 * h, y + 0.5 * k2)
        k4 = h * dydxfunc(x0 + h, y + k3)

        # Update next value of y
        y = y + (1.0 / 6.0) * (k1 + 2 * k2 + 2 * k3 + k4)
        Y.append(y)
        # Update next value of x
        x0 = x0 + h
        X.append(x0)
    return y


# Driver method
x0 = 0
y0 = 1
x = 122
h = 0.02
print('The value of y at x is:', rungeKutta(dydx2, x0, y0, x, h))

import matplotlib.pyplot as plt

plt.plot(X, Y)
plt.show()
