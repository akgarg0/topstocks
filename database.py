import redis
import pickle
import os

import parseFile


class DataBase:
    def __init__(self):
        """
        Initialising connection to redis database
        """
        with open('credentials.cred', 'rb') as cred:
            self.redis_cred = pickle.load(cred)
        self.r = redis.Redis(**self.redis_cred, charset="utf-8", decode_responses=True)

    def load_csv_to_db(self, path='tmp'):
        """
        loads data from CSV file to Redis DB
        """
        r = self.r
        csv_handle = ''
        for root, dirs, files in os.walk(path):
            file = files[0]
            file_path = os.path.join('tmp', file)
            csv_handle = parseFile.CSVFile(file_path)
        data = csv_handle.csv_to_obj()
        print(data)
        pipe = r.pipeline()
        n = 1
        for row in data:
            data_key = row.pop('NAME')
            pipe.hmset(data_key, row)
            n = n + 1
            if (n % 1024) == 0:
                pipe.execute()
                pipe = r.pipeline()
        pipe.execute()
        # for row in data:
        #     data_key = row.pop('NAME')
        #     r.hmset(data_key, row)

    def get_top_10_or_searched(self, name=''):
        """
        Generates list of data rows with or without searched name up-to 10 rows at most.
        :param name:
        :return list:
        """
        r = self.r
        data_keys = r.keys()
        data = []
        count = 0
        for index in range(len(data_keys)):
            if count == 10:
                break
            if name.lower() not in str(data_keys[index]).lower():
                continue
            count = count + 1
            row = r.hgetall(data_keys[index])
            row['NAME'] = data_keys[index]
            data.append(row)
        return data

    def delete_all(self):
        """
        Clears all the data from redis db
        """
        r = self.r
        pipe = r.pipeline()
        n = 1
        for data_key in r.keys():
            pipe.delete(data_key)
            n = n + 1
            if (n % 1024) == 0:
                pipe.execute()
                pipe = r.pipeline()
        pipe.execute()


# red = DataBase()
# red.delete_all()
# print(red.get_top_10_or_searched())
