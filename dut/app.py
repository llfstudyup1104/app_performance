# _*_ coding: utf-8 _*_
import os


class App(object):
    
    def __init__(self, pagename, activity):
        self.pagename = pagename
        self.activity = activity
        self.content = ""
        self.start_time = ""

    def start_app(self):
        cmd = "adb shell am start -W -n " + self.pagename + self.activity
        self.content = os.popen(cmd)
    
    @staticmethod
    def wart_stop():
        cmd = "adb shell input keyevent 3"
        os.popen(cmd)
        
    def cold_stop(self):
        cmd = "adb shell am force-stop " + self.pagename
        os.popen(cmd)
        
    
if __name__ == '__main__':
    app = App("com.byton.ice.android.multimedia", "/com.byton.ice.android.multimedia.ui.DRTControlActivity")
    app.start_app()
