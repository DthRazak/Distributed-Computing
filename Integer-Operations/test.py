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

    def test_correct_result_for_find_maximum(self):
        output_filename = './output/hadoop-python-find-maximum.txt'

        with open(output_filename, 'r') as file:
            num = int(file.readline())

            self.assertEqual(num, max(self.numbers_set))

    def test_correct_result_for_find_distinct(self):
        output_filename = './output/hadoop-python-find-distinct.txt'

        numbers = list()
        with open(output_filename, 'r') as file:
            for line in file:
                numbers.append(int(line))

        counts = {item: self.numbers.count(item) for item in self.numbers}
        counts = {key: value for key, value in counts.items() if value == 1}

        self.assertTrue(len(set(counts.keys()).difference(set(numbers))) == 0)


if __name__ == '__main__':
    unittest.main()
