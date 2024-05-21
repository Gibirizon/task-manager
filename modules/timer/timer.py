from datetime import datetime, timedelta

from kivy.properties import StringProperty
from kivymd.uix.screen import MDScreen


class Timer(MDScreen):
    # Text on the start/stop button: "Start" or "Stop"
    start_stop_button_text = StringProperty("Start")

    # Variable to check if the timer has started
    started_timer = None

    def __init__(self, **kw):
        self.service = None
        super().__init__(**kw)

    def start_timer(self, text):
        # If the button text is "Start", initialize the timer
        if text == "Start":
            # Save the current time as the start time
            self.started_timer = datetime.now()

            # Parse the current time label to get the initial minutes and seconds
            self.label_time = timedelta(
                minutes=int(self.ids.current_time_label.text[:2]),
                seconds=int(self.ids.current_time_label.text[3:]),
            )

            # Change button text to "Stop"
            self.start_stop_button_text = "Stop"

        # If the button text is "Stop", stop the timer
        else:
            self.stop_timer()

    def stop_timer(self):
        # First refresh the timer to update the current time label
        self.refresh_timer()

        # Stop the timer by resetting the start time
        self.started_timer = None

        # Change button text back to "Start"
        self.start_stop_button_text = "Start"

    def restart_timer(self):
        # Change button text back to "Start"
        self.start_stop_button_text = "Start"

        # Stop the timer by resetting the start time
        self.started_timer = None

        # Reset the timer label back to the default 25:00
        self.ids.current_time_label.text = "25:00"

    # Refresh the timer to update the current time label based on elapsed time
    def refresh_timer(self):
        # Compare the current time with the saved start time
        if self.started_timer:
            stopped_timer = datetime.now()
            passed_time = stopped_timer - self.started_timer

            # Calculate the new remaining time
            if self.label_time > passed_time:
                new_time = self.label_time - passed_time
            else:
                new_time = passed_time - self.label_time

            # Convert the new time to minutes and seconds
            new_mins, new_secs = divmod(new_time.seconds, 60)
            label_timeformat = "{:02d}:{:02d}".format(new_mins, new_secs)

            # Update the current time label with the new formatted time
            self.ids.current_time_label.text = label_timeformat

            # Add a minus sign if the elapsed time exceeds the initial timer value (25 minutes)
            if passed_time > self.label_time:
                self.ids.current_time_label.text = (
                    "-" + self.ids.current_time_label.text
                )
