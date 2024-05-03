from modules.to_do_list_base_classes.base import (
    BaseDialog,
    BaseDialogContent,
    ListScreen,
)


class WeeklyTasks(ListScreen):
    def __init__(self, **kw):
        super().__init__(table_name="weekly_tasks", **kw)

    def open_dialog(self):
        if not self.dialog:
            self.dialog = WeeklyTasksDialog()
            self.dialog.bind(on_dismiss=self.dismiss_dialog)
            self.dialog.open()


class WeeklyTasksDialog(BaseDialog):
    def __init__(self):
        self.content = BaseDialogContent(table_name="weekly_tasks_options")
        super().__init__(
            table_name="weekly_tasks_options",
            headline_text="Set your next task",
            screen_name="weekly_tasks",
        )
