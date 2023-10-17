import unittest

from cron_parser import CronParser

class CronParserTest(unittest.TestCase):

    def test_validate_cron_expression_with_invalid_number_of_args(self):
        cron_expression = "0 0 * * * /path/to/script.sh 1"

        parser = CronParser(cron_expression)

        with self.assertRaises(ValueError):
            parser.validate_cron_expression()

    def test_parse_string_with_asterisk(self):
        string = "*"

        parser = CronParser("")

        result = parser.parse_string(string, "minute")

        self.assertEqual(result, "0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59")

    def test_parse_string_with_question_mark(self):
        string = "?"

        parser = CronParser("")

        result = parser.parse_string(string, "minute")

        self.assertEqual(result, "Not Specified")

    def test_parse_string_with_range(self):
        string = "1-10"

        parser = CronParser("")

        result = parser.parse_string(string, "minute")

        self.assertEqual(result, "1 2 3 4 5 6 7 8 9 10")

    def test_parse_string_with_interval(self):
        string = "1/5"

        parser = CronParser("")

        result = parser.parse_string(string, "minute")

        self.assertEqual(result, "5 10 15 20 25 30 35 40 45 50 55")

    def test_parse_string_with_list(self):
        string = "1,3,5,7"

        parser = CronParser("")

        result = parser.parse_string(string, "minute")

        self.assertEqual(result, "1 3 5 7")



if __name__ == '__main__':
    unittest.main()
