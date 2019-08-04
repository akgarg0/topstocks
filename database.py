import redis
import pickle


class DataBase:
    def __init__(self):
        """
        Initialising connection to redis database
        """
        with open('credentials.cred', 'rb') as cred:
            self.redis_cred = pickle.load(cred)
        self.r = redis.Redis(**self.redis_cred)

    def load_csv_to_db(self):
        """
        loads data from CSV file to Redis DB
        """
        r = self.r
        data = [{'NAME': 'ALPHA', 'CODE': 12452, 'open': '1234.6'}]
        for row in data:
            data_key = row.pop('NAME')
            r.hmset(data_key, row)

    def get_top_10_or_searched(self, name=''):
        """
        Generates list of data rows with or without searched name up-to 10 rows at most.
        :param name:
        :return list:
        """
        r = self.r
        data_keys = r.keys()
        data = []
        for index in range(min(10, len(data_keys))):
            if name not in str(data_keys[index]):
                continue
            row = r.hgetall(data_keys[index])
            row['NAME'] = data_keys[index]
            data.append(row)
        return data

    def delete_all(self):
        """
        Clears all the data from redis db
        """
        r = self.r
        for data_key in r.keys():
            print(data_key, r.hgetall(data_key))
            r.delete(data_key)


red = DataBase()
# red.load_csv_to_db()
# red.delete_all()
# print(red.get_top_10_or_searched())
