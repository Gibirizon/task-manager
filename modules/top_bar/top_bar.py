from kivy.uix.screenmanager import Screen


class Navigation(Screen):
    def __init__(self, **kw):
        super().__init__(**kw)

    # change top bar title after changing screen
    def adjust_top_bar_title(self, top_bar_title):
        self.ids.top_bar.title = top_bar_title

