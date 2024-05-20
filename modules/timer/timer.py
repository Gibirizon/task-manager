from datetime import datetime, timedelta

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen


class Timer(MDScreen):
    # text on button: start/stop
    start_stop_button_text = StringProperty("Start")

    # variable to check has timer started
    started_timer = None

    def __init__(self, **kw):
        self.service = None
        super().__init__(**kw)

    def start_timer(self, text):
        if text == "Start":
            # save current time
            self.started_timer = datetime.now()
            self.label_time = timedelta(
                minutes=int(self.ids.current_time_label.text[:2]),
                seconds=int(self.ids.current_time_label.text[3:]),
            )

            # change button text
            self.start_stop_button_text = "Stop"

        else:
            self.stop_timer()

    def stop_timer(self):
        # first refresh the timer
        self.refresh_timer()

        # stop timer
        self.started_timer = None

        # change button text
        self.start_stop_button_text = "Start"

    def restart_timer(self):
        # change button text
        self.start_stop_button_text = "Start"

        # stop timer
        self.started_timer = None

        # back to 25 minutes
        self.ids.current_time_label.text = "25:00"

    # timer will only refresh after this method, so that you can leave this app working in background  and then come back to it and refresh
    def refresh_timer(self):
        # compare current time with self.started_time_at
        if self.started_timer:
            stopped_timer = datetime.now()
            passed_time = stopped_timer - self.started_timer
            if self.label_time > passed_time:
                new_time = self.label_time - passed_time
            else:
                new_time = passed_time - self.label_time
            new_mins, new_secs = divmod(new_time.seconds, 60)
            label_timeformat = "{:02d}:{:02d}".format(new_mins, new_secs)

            # new text
            self.ids.current_time_label.text = label_timeformat

            # minus as first character if passed time > 25 min
            if passed_time > self.label_time:
                self.ids.current_time_label.text = (
                    "-" + self.ids.current_time_label.text
                )
