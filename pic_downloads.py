import requests
import re
import time
import random
from orm.sql import manager


class pic_downloads(object):
    def __init__(self):
        master = manager(
            "postgresql://inspyder:No996icu@127.0.0.1:5432/insdata")
        self.pic_list = master.get_pic_list()
        master.close()
        self.sharedHeader = {
            "Cache-Control": "no-cache",
            "User-Agent":
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:67.0) Gecko/20100101 Firefox/67.0",
            "Accept-Language": "zh-CN,zh;q=0.8"
        }
        self.con = requests.Session()
        self.con.headers.update(self.sharedHeader)

    def run(self):
        total = len(self.pic_list)
        for starter in range(0, total, 12):
            end = starter + 12
            if end > total:
                end = total
            sub_list = self.pic_list[starter:end]
            print("downloading picture {0} ~ {1}".format(starter, end))
            for pic in sub_list:
                pic_ext = re.search(r'\.\w+\?', pic[1]).group()
                pic_ext = pic_ext[0:-1]
                pic_name = pic[0] + pic_ext
                pic_rt = self.con.get(pic[1], stream=True)
                with open("pic/" + pic_name, "wb") as target:
                    for chunk in pic_rt.iter_content(256):
                        target.write(chunk)
            time.sleep(1 + random.randint(0, 2))
        self.con.close()


if __name__ == "__main__":
    downloader = pic_downloads()
    downloader.run()
