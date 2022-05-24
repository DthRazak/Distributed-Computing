import unittest
import numpy as np


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.n = 20
        self.input_filename = './input/mat_20.txt'
        self.output_filename = './output/hadoop-python-result-striping.txt'

        self.mat = np.zeros((self.n, self.n))
        self.vec = np.zeros(self.n)
        self.res_vec = np.zeros(self.n)

        with open(self.input_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                if len(values) == 3:
                    i, j, m = [int(val) for val in values]
                    self.mat[i, j] = m
                else:
                    j, v = [int(val) for val in values]
                    self.vec[j] = v

        with open(self.output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                j, v = [int(val) for val in values]
                self.res_vec[j] = v

    def test_correct_result(self):
        np.testing.assert_array_equal(self.res_vec, np.matmul(self.mat, self.vec))


if __name__ == '__main__':
    unittest.main()
