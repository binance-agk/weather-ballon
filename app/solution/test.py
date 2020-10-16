#  test rk4
def f(t, y):
    p = (1 - y[0] ** 2) * y[1] - y[0]
    return np.array([y[1], p])


bname = (
    'TA 200', 'TA 300', 'TA 350', 'TA 450', 'TA 500', 'TA 600', 'TA 700'
    , 'TA 800', 'TA 1000', 'TA 1200', 'TA 1500',
    'TA 2000', 'TA 3000', 'TX 800', 'TX 1000', 'TX 1200', 'TX 2000', 'TX 3000')

print(bname.index(('TA 200')))