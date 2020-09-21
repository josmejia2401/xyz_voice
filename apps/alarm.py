import time
import schedule 
import threading
"""
schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)
schedule.every(5).to(10).minutes.do(job)
schedule.every().monday.do(job)
schedule.every().wednesday.at("13:15").do(job)
schedule.every().minute.at(":17").do(job)
"""
class Alarm(object):

    def __init__(self):
        super().__init__()
        self.schedstop = threading.Event()
        self.schedthread = None
        self.running_thread = True

    def job(self) -> None:
        print("Sonando alarma")

    def stop(self):
        self.running_thread = False
        schedule.clear()
        self.schedthread.raise_exception() 
    
    """def build_seconds(self) -> None:
        schedule.every(10).seconds.do(self.job)"""

    def build_minutes(self, min) -> None:
        schedule.every(min).minutes.do(self.job)

    def build_hours(self, hour) -> None:
        schedule.every(hour).hours.do(self.job)

    def build_day(self, day = "", tx = "07:00") -> None:
        schedule.every()[day].at(tx).do(self.job)

    def build_all_day(self, tx = "07:00") -> None:
        schedule.every().day.at(tx).do(self.job)

    def build_week(self, tx = "07:00") -> None:
        schedule.every().monday.at(tx).do(self.job)
        schedule.every().tuesday.at(tx).do(self.job)
        schedule.every().wednesday.at(tx).do(self.job)
        schedule.every().thursday.at(tx).do(self.job)
        schedule.every().friday.at(tx).do(self.job)

    def get_list(self) -> None:
        pass

    def timer(self):
        while self.running_thread:
            schedule.run_pending()
            time.sleep(5)

    def run(self) -> None:    
        self.schedthread = threading.Thread(target=self.timer)
        self.schedthread.start()
        #self.schedthread.join()



