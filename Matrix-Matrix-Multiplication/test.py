import unittest
import numpy as np


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.m, self.n, self.k = 20, 20, 20
        input_filename = './input/data.txt'

        self.mat_a = np.zeros((self.m, self.n))
        self.mat_b = np.zeros((self.n, self.k))

        with open(input_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                i, j, m = [int(val) for val in values[:3]]

                if values[3][0] == 'A':
                    self.mat_a[i, j] = m
                else:
                    self.mat_b[i, j] = m

    def test_correct_result_via_natural_join(self):
        output_filename = './output/hadoop-python-via-natural-join.txt'
        mat = np.zeros((self.m, self.k))

        with open(output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                i, j, m = [int(val) for val in values]

                mat[i, j] = m

        np.testing.assert_array_equal(mat, np.matmul(self.mat_a, self.mat_b))


if __name__ == '__main__':
    unittest.main()
