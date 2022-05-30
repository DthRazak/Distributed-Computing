import unittest
import numpy as np


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        self.n = 20
        self.input_filename = './input/mat_20.txt'
        self.striping_output_filename = './output/hadoop-python-result-striping.txt'
        self.blocking_output_filename = './output/hadoop-python-result-blocking.txt'
        self.pyspark_striping_output_filename = './output/pyspark-result-striping.csv'
        self.pyspark_blocking_output_filename = './output/pyspark-result-striping.csv'

        self.mat = np.zeros((self.n, self.n))
        self.vec = np.zeros(self.n)
        self.striping_res_vec = np.zeros(self.n)
        self.pyspark_striping_res_vec = np.zeros(self.n)
        self.blocking_res_vec = np.zeros(self.n)
        self.pyspark_blocking_res_vec = np.zeros(self.n)

        with open(self.input_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                if len(values) == 3:
                    i, j, m = [int(val) for val in values]
                    self.mat[i, j] = m
                else:
                    j, v = [int(val) for val in values]
                    self.vec[j] = v

        with open(self.striping_output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                j, v = [int(val) for val in values]
                self.striping_res_vec[j] = v

        with open(self.blocking_output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                j, v = [int(val) for val in values]
                self.blocking_res_vec[j] = v

        with open(self.pyspark_striping_output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                j, v = [int(val) for val in values]
                self.pyspark_striping_res_vec[j] = v

        with open(self.pyspark_blocking_output_filename, 'r') as file:
            for line in file:
                values = line.split(';')
                j, v = [int(val) for val in values]
                self.pyspark_blocking_res_vec[j] = v

    def test_hadoop_striping_correct_result(self):
        np.testing.assert_array_equal(self.striping_res_vec, np.matmul(self.mat, self.vec))

    def test_pyspark_striping_correct_result(self):
        np.testing.assert_array_equal(self.pyspark_striping_res_vec, np.matmul(self.mat, self.vec))

    def test_blocking_correct_result(self):
        np.testing.assert_array_equal(self.blocking_res_vec, np.matmul(self.mat, self.vec))

    def test_pyspark_blocking_correct_result(self):
        np.testing.assert_array_equal(self.pyspark_blocking_res_vec, np.matmul(self.mat, self.vec))


if __name__ == '__main__':
    unittest.main()
