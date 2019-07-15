# _*_ coding: utf-8 _*_
import os
import time


class App(object):

    def __init__(self, page_name, first_activity):
        """"构造方法"""
        self.page_name = page_name
        self.first_activity = first_activity
        self.content = ""
        self.start_time = ""

    def start_app(self):
        """开启APP"""
        cmd = "adb shell am start -W -n " + self.page_name + self.first_activity
        self.content = os.popen(cmd)

    def cold_stop_app(self):
        """冷停止APP"""
        cmd = "adb shell am force-stop " + self.page_name
        os.popen(cmd)

    @staticmethod
    def warm_stop_app():
        """热停止app"""
        cmd = "adb shell input keyevent 3"
        os.popen(cmd)

    def get_launch_time(self):
        """获取启动时间"""
        for line in self.content.readlines():
            if "ThisTime" in line:
                self.start_time = line.split(":")[1].strip()
                break
        return self.start_time


if __name__ == '__main__':
    app = App("com.byton.ice.android.multimedia", "/com.byton.ice.android.multimedia.ui.DRTControlActivity")
    app.start_app()
    time.sleep(2)
    app.cold_stop_app()
    print("It costs " + app.get_launch_time() + "ms to start this activity")
