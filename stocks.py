import wget
from six.moves import urllib
import re
import zipfile
import os


class BhavCopy:
    def __init__(self):
        resp = urllib.request.urlopen("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
        resp_page = str(resp.read())
        url = re.search(r'(?:<a.*Zip" href=")(.*)(?:" target="_self">Equity - [0-9]*)', resp_page)
        self.url = url.groups()[0]

    def download_zip(self):
        print(self.url)
        # resp = urllib.request.urlopen(self.url)
        # z_file = zipfile.ZipFile(wget.download(self.url))
        f_path = wget.download(self.url)
        z_file = zipfile.ZipFile(f_path)
        z_file.extractall('tmp')
        z_file.close()
        os.remove(f_path)


bc = BhavCopy()
bc.download_zip()
