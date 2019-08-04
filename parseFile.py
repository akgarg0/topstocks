import csv

DEFAULT_FIELDS = {
                'SC_CODE': 'CODE',
                'SC_NAME': 'NAME',
                'OPEN': 'OPEN',
                'HIGH': 'HIGH',
                'LOW': 'LOW',
                'CLOSE': 'CLOSE'
}


class CSVFile:
    def __init__(self, path):
        """
        Initialising CSV file object
        :param path:
        """
        csv_file = open(path, 'r')
        self.data_file = csv.DictReader(csv_file, delimiter=',')

    def csv_to_obj(self, fields=DEFAULT_FIELDS):
        """
        Required Data is converted to object
        :param fields:
        :return list:
        """
        data = []
        for row in self.data_file:
            new_row = {}
            for field in row:
                if field in fields:
                    new_row[fields[field]] = row[field].trim()
            data.append(new_row)
        return data
