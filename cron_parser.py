import sys

class CronParser:
    def __init__(self, cron_str):
        self.cron_str = cron_str
        self.initialize_values()

    def initialize_values(self):
        self.values = {
            'week': list(range(1, 8)),
            'month': list(range(1, 13)),
            'hour': list(range(0, 24)),
            'day': list(range(1, 32)),
            'minute': list(range(0, 60))
        }

        self.months = [
            'JAN', 'FEB', 'MAR',
            'APR', 'MAY', 'JUN',
            'JUL', 'AUG', 'SEP',
            'OCT', 'NOV', 'DEC'
        ]

        self.days = [
            'SUN', 'MON', 'TUE',
            'WED', 'THU', 'FRI',
            'SAT'
        ]

    def validate_cron_expression(self):
        if len(self.cron_str.split(" ")) != 6:
            raise ValueError("Invalid number of args in cron expression")

    def parse_string(self, string, datatype):
        if string == "*":
            return ' '.join(map(str, self.values[datatype]))
        if string == "?":
            return 'Not Specified'

        if "-" in string:
            values = self.days if datatype == "week" else self.months
            return self.parse_range(string, values, datatype)

        if "/" in string:
            return self.parse_interval(string, self.values[datatype], datatype)

        if "," in string:
            if datatype in ['month', 'week']:
                sub = self.days if datatype == "week" else self.months
                return self.parse_lists(string, self.values[datatype], datatype, sub)
            else:
                return self.parse_lists(string, self.values[datatype], datatype)

        if string.isdigit() and int(string) in self.values[datatype]:
            return string

        raise ValueError(f'Invalid input for {datatype}: {string}')

    def parse_range(self, string, values, datatype):
        start, end = string.split('-')
        try:
            start, end = int(start), int(end)
        except ValueError:
            try:
                start, end = values.index(start), values.index(end)
                return ' '.join(values[start:end + 1])
            except ValueError:
                raise ValueError(f'Invalid {datatype} input combination: {string}. Please use either string or number syntax.')

        return ' '.join(map(str, [i for i in range(start, end + 1)]))

    def parse_interval(self, string, values, datatype):
        try:
            first, second = string.split("/")
            if first == "*":
                return ' '.join(map(str, [i for i in values if i % int(second) == 0]))

            first, second = int(first), int(second)

            if first < 0 or second <= 0:
                raise ValueError(f'Invalid input for {datatype}: {string}. Both values must be positive.')

            if first > values[-1]:
                raise ValueError(f'Invalid input for {datatype}: {string}. First value exceeds the maximum allowed value.')

            return ' '.join(map(str, [i for i in range(first, values[-1] + 1) if i % second == 0]))
        except ValueError as e:
            return str(e)


    def parse_lists(self, string, values, datatype, sub=None):
        inputs = string.split(',')
        type_value = None
        v = None
        try:
            for i in inputs:
                try:
                    v = int(i)
                except ValueError:
                    v = i

                if type_value is None:
                    type_value = type(v)
                elif type_value != type(v):
                    raise ValueError(f'Invalid {datatype} input combination: {string}. Please use either string or number syntax.')

                if type(v) == str and v not in sub:
                    raise ValueError(f'Invalid {datatype} data provided: {string}')
                if type(v) == int and v not in values:
                    raise ValueError(f'Invalid {datatype} data provided: {string}')
        except ValueError as e:
            return str(e)

        return string.replace(",", " ")



    def parse_cron(self):
        self.validate_cron_expression()
        minute, hour, day, month, week, cmd = self.cron_str.split()
        descriptions = [
            "Minutes: {}".format(self.parse_string(minute, 'minute')),
            "Hours: {}".format(self.parse_string(hour, 'hour')),
            "Day of month: {}".format(self.parse_string(day, 'day')),
            "Month: {}".format(self.parse_string(month, 'month')),
            "Day of Week: {}".format(self.parse_string(week, 'week')),
            "Command: {}".format(cmd)
        ]

        return '\n'.join(descriptions)


if __name__ == '__main__':
    cron_expression = sys.argv[1]
    parser = CronParser(cron_expression)
    description = parser.parse_cron()
    print(description)
