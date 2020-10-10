#  test rk4
def f(t, y):
    p = (1 - y[0] ** 2) * y[1] - y[0]
    return np.array([y[1], p])