import unittest
import numpy as np


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        input_filename = './input/data.txt'
        data = list()

        with open(input_filename, 'r') as file:
            for num in file:
                data.append(int(num))

        self.numbers = np.array(sorted(data))

    def test_correct_result(self):
        output_filename = './output/hadoop-python-result.txt'
        numbers = np.zeros(len(self.numbers), 'uint32')

        with open(output_filename, 'r') as file:
            for line in file:
                pos, val = line.split(';')
                pos, val = int(pos), int(val)

                numbers[pos-1] = val

        np.testing.assert_array_equal(numbers, self.numbers)


if __name__ == '__main__':
    unittest.main()
