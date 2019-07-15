# encoding: utf-8
from pft.timeslot.app import App
import csv
import time


# 控制类
class Controller(object):

    def __init__(self, count, start_type):
        self.app = App("com.byton.ice.android.multimedia", "/com.byton.ice.android.multimedia.ui.DRTControlActivity")
        self.counter = count
        self.start_type = start_type
        self.all_data = [("timestamp", "elapsed_time")]
        print("init file done")

    # 获取当前的时间戳
    @staticmethod
    def get_current_time():
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        return current_time

    # 单次测试
    def test_process(self):
        self.app.start_app()
        print("Start app")
        time.sleep(2)
        elapsed_time = self.app.get_launch_time()

        if self.start_type == 'cold':
            self.app.cold_stop_app()
            print("cold stop app")
        elif self.start_type == 'warm':
            self.app.warm_stop_app()
            print("warm stop app")
        time.sleep(2)
        current_time = self.get_current_time()

        self.all_data.append((current_time, elapsed_time))

    # 多次测试
    def run(self):
        while self.counter > 0:
            self.test_process()
            self.counter = self.counter - 1
            print("Hello ", self.counter)

    # 数据的存储
    def save_data_to_csv(self):
        csv_file = open('start_time.csv', 'w', newline="")
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if __name__ == '__main__':
    # import time
    # app = App("com.byton.ice.android.multimedia", "/com.byton.ice.android.multimedia.ui.DRTControlActivity")
    # app.start_app()
    # time.sleep(2)
    # app.cold_stop_app()

    controller = Controller(2, 'cold')
    controller.run()
    controller.save_data_to_csv()
