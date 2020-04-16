from app import App
import utils.config as uc
import time
import os
import re
import csv


cf = uc.Configure()
page = cf.get_config_value("app", "page")
activity = cf.get_config_value("app", "activity")


class Controller(object):
    
    def __init__(self, count, target):
        self.app = App(page, activity)
        self.count = count
        self.target = target
        self.cpu = ""
        self.mem = ""
        self.start_time = ""
        self.all_data = [("time_stamp", "matrix")]
        self.setup() 
    
    def setup(self):
        self.app.start_app()
    
    def tear_down(self):
        self.app.cold_stop()
    
    def get_current_time(self):
        current_time = time.strftime("%Y-%m-%d: %H:%M:%S", time.localtime())
        return current_time
    
    def get_cpu_usage(self):
        cmd = "adb shell dumpsys cpuinfo " + self.app.pagename
        for line in os.popen(cmd).readlines():
            if "TOTAL" in line:
                self.cpu = line.split("%")[0].strip()
        print("CPU Usage is: ", self.cpu)
        return self.cpu
        
    def get_mem_usage(self):
        cmd = "adb shell dumpsys meminfo " + self.app.pagename
        for line in os.popen(cmd).readlines():
            if "TOTAL" in line:
                self.mem = re.split('\s{4}', line)[3].strip()
                break
        print("Mem usage is: ", self.mem)
        return self.mem    
                
    def get_start_time(self):
        print("Start to get the time")
        self.tear_down()
        self.setup()
        for line in self.app.content.readlines():
            if "ThisTime" in line:
                self.start_time = line.split(":")[1].strip()
        print("Start time is:", self.start_time)
        return self.start_time
    
    def run_process(self):
        if self.target == 'cpu':
            self.cpu = self.get_cpu_usage()
            self.all_data.append((self.get_current_time(), self.cpu))
        
        if self.target == 'mem':
            self.mem = self.get_mem_usage()
            self.all_data.append((self.get_current_time(), self.mem))
        
        if self.target == 'start_time':
            self.start_time = self.get_start_time()
            self.all_data.append((self.get_current_time(), self.start_time))
            
    def run(self):
        while self.count > 0:
            self.run_process()
            self.count = self.count - 1
            time.sleep(2)
        self.tear_down()
    
    def save_to_csv(self):
        csv_file = open("matrix.csv", 'w', newline = "")
        writer = csv.writer(csv_file)
        writer.writerows(self.all_data)
        csv_file.close()
        

if __name__ == '__main__':
    controller = Controller(5, 'mem')
    controller.run()
    controller.save_to_csv()
