import os
from datetime import datetime, timedelta

from kivy.properties import BooleanProperty
from kivy.storage.jsonstore import JsonStore
from kivymd.uix.screen import MDScreen


class Timer(MDScreen):
    time_store = JsonStore(f"{os.path.dirname(__file__)}/time_store.json")
    timer_is_running = BooleanProperty(False)
    initial_state_of_timer_in_seconds = 1500

    def __init__(self, **kw):
        timer_initiation_unix_time = 0
        if not self.time_store.exists("timer"):
            self.time_store.put(
                "timer",
                timer_initiation_unix_time=timer_initiation_unix_time,
                initial_state_of_timer_in_seconds=self.initial_state_of_timer_in_seconds,
                timer_is_running=self.timer_is_running,
            )
        super().__init__(**kw)

    def on_pre_enter(self):
        self.refresh_timer()

    def start_timer(self):
        # Current seconds from unix time
        timer_initiation_unix_time = datetime.now().timestamp()
        self.timer_is_running = True

        # Put these values into json store
        self.time_store.put(
            "timer",
            timer_initiation_unix_time=timer_initiation_unix_time,
            initial_state_of_timer_in_seconds=self.time_store.get("timer")[
                "initial_state_of_timer_in_seconds"
            ],
            timer_is_running=self.timer_is_running,
        )

    def stop_timer(self):
        # First refresh the timer to update the current time label
        self.refresh_timer()

        # Stop timer
        self.timer_is_running = False
        self.time_store.put(
            "timer",
            timer_initiation_unix_time=self.time_store.get("timer")[
                "timer_initiation_unix_time"
            ],
            initial_state_of_timer_in_seconds=self.time_store.get("timer")[
                "initial_state_of_timer_in_seconds"
            ],
            timer_is_running=False,
        )

    def restart_timer(self):
        self.timer_is_running = False
        self.time_store.put(
            "timer",
            timer_initiation_unix_time=self.time_store.get("timer")[
                "timer_initiation_unix_time"
            ],
            initial_state_of_timer_in_seconds=self.initial_state_of_timer_in_seconds,
            timer_is_running=self.timer_is_running,
        )

        # Reset the timer label back to the default 25:00
        mins, secs = divmod(int(abs(self.initial_state_of_timer_in_seconds)), 60)
        time_format_for_label = "{:02d}:{:02d}".format(mins, secs)
        self.ids.current_time_label.text = time_format_for_label

    # Refresh the timer to update the current time label based on elapsed time
    def refresh_timer(self):
        # Getting values from store, because app could have been closed
        timer_initiation_unix_time = self.time_store.get("timer")[
            "timer_initiation_unix_time"
        ]
        initial_state_of_timer_in_seconds = self.time_store.get("timer")[
            "initial_state_of_timer_in_seconds"
        ]
        self.timer_is_running = self.time_store.get("timer")["timer_is_running"]

        if self.timer_is_running:
            timer_refreshed_unix_time = datetime.now().timestamp()
            passed_time_in_seconds = (
                timer_refreshed_unix_time - timer_initiation_unix_time
            )
            new_time_in_seconds = (
                initial_state_of_timer_in_seconds - passed_time_in_seconds
            )
            self.time_store.put(
                "timer",
                timer_initiation_unix_time=timer_refreshed_unix_time,
                initial_state_of_timer_in_seconds=new_time_in_seconds,
                timer_is_running=self.timer_is_running,
            )

        else:
            new_time_in_seconds = initial_state_of_timer_in_seconds

        mins, secs = divmod(int(abs(new_time_in_seconds)), 60)
        time_format_for_label = "{:02d}:{:02d}".format(mins, secs)
        if new_time_in_seconds < 0:
            time_format_for_label = "-" + time_format_for_label

        # Update the current time label with the new formatted time
        self.ids.current_time_label.text = time_format_for_label
