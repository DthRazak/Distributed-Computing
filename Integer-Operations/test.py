import unittest


class ResultTestCase(unittest.TestCase):
    def setUp(self):
        input_filename = './input/data.txt'
        data = list()

        with open(input_filename, 'r') as file:
            for num in file:
                data.append(int(num))

        self.numbers = data
        self.numbers_set = set(data)

    def test_correct_result_for_finding_duplicates(self):
        output_filename = './output/hadoop-python-filter-duplicates.txt'
        numbers = list()

        with open(output_filename, 'r') as file:
            for num in file:
                numbers.append(int(num))

        self.assertTrue(len(set(numbers).difference(self.numbers_set)) == 0)


if __name__ == '__main__':
    unittest.main()
