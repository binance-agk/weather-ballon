import unittest

from solution import Solution
from matplotlib import pyplot as plt


def test_something(self):
    class Emmiter(object):

        def error(self):
            pass


class MyTestCase(unittest.TestCase):
    def test_something(self):

        year = 2020
        month = 10
        day = 6
        hour = 12
        lat0 = 12
        lon0 = 122

        filename = "GFS_Global_0p5deg_ana_{0}{1}{2:0=2d}_{3}00.grib2.nc" \
            .format(year, month, day, hour)
        print(filename)
        emmiter = lambda h: print(h)
        solution = Solution(emmiter,emmiter, lat0, lon0, day, month, year, hour, 0, filename, 1, 10, None, None, 0, 22000,
                            15000)
        t, y = solution.solveballoonpart()
        iend = solution.iend
        plt.plot(t[0:iend], -y[0:iend, 2], 'g.')
        plt.show()
        plt.plot(t[0:iend], -y[0:iend, 5], 'g.')
        plt.show()

        solution.solveparachutepart()
        k = solution.kend
        plt.plot(solution.Tpar[0:k], -solution.Xpar[0:k, 2], 'r.')
        plt.show()
        plt.plot(solution.Tpar[0:k], -solution.Xpar[0:k, 5], 'r.')
        plt.show()

        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
