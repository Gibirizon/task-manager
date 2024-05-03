from modules.to_do_list_base_classes.base import (
    BaseDialog,
    BaseDialogContent,
    ListScreen,
)


class Goals(ListScreen):
    def __init__(self, **kw):
        super().__init__(table_name="goals", **kw)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = GoalsDialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()


class GoalsDialog(BaseDialog):
    def __init__(self):
        self.content = BaseDialogContent(table_name="goals_options")
        super().__init__(
            table_name="goals_options",
            headline_text="Set your next goal",
            screen_name="goals",
        )
