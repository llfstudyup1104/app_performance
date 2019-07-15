import os
import time
import re
import csv


# 主程序类
class Manager(object):

    def __init__(self, page_name, target, count):
        self.page_name = page_name
        self.target = target
        self.counter = count
        self.all_data = [("TimeStamp", "Usage")]
        self.content = ""

    @staticmethod
    def get_current_time():
        """获取当前时间"""
        current_time = time.strftime("%Y-%m-%d: %H:%M:%S", time.localtime())
        return current_time

    def send_cmd(self):
        """发送获取usage的命令行"""
        if self.target == 'cpu':
            cmd = "adb shell dumpsys cpuinfo"
        elif self.target == 'mem':
            cmd = "adb shell dumpsys meminfo " + self.page_name
        self.content = os.popen(cmd).readlines()

    def run_process(self):
        """提取usage并存储至列表"""
        if self.target == 'cpu':
            self.send_cmd()
            for line in self.content:
                if "TOTAL" in line:
                    cpu = line.split("%")[0].strip()
                    current_time = self.get_current_time()
                    self.all_data.append((current_time, cpu))

        if self.target == 'mem':
            self.send_cmd()
            for line in self.content:
                if "TOTAL" in line:
                    mem = re.split('\s{4}', line)[3].strip()
                    print("MEM usage is: ", mem)
                    current_time = self.get_current_time()
                    self.all_data.append((current_time, mem))
                    break

    def run(self):
        """运行多次并存储结果"""
        while self.counter > 0:
            self.run_process()
            self.counter = self.counter - 1
            time.sleep(2)

    def save_to_csv(self):
        """存储结果至csv文件"""
        csv_file = open('usage.csv', 'w', newline="")
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()


if __name__ == '__main__':
    controller = Manager("com.byton.ice.android.multimedia", 'mem', 10)
    controller.run()
    controller.save_to_csv()

