from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore
from datetime import datetime

class HomeScreen(Screen):
    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        self.task_input = TextInput(hint_text='Enter task', multiline=False)
        self.due_date_input = TextInput(hint_text='Enter due date (optional)', multiline=False)
        add_button = Button(text='Add Task', on_press=self.add_task)
        delete_button = Button(text='Delete Task', on_press=self.delete_task)
        complete_button = Button(text='Complete Task', on_press=self.complete_task)
        show_undeleted_button = Button(text='Show Undeleted Tasks', on_press=self.show_undeleted_tasks)
        show_deleted_button = Button(text='Show Deleted Tasks', on_press=self.show_deleted_tasks)

        self.layout.add_widget(self.task_input)
        self.layout.add_widget(self.due_date_input)
        self.layout.add_widget(add_button)
        self.layout.add_widget(delete_button)
        self.layout.add_widget(complete_button)
        self.layout.add_widget(show_undeleted_button)
        self.layout.add_widget(show_deleted_button)

        self.add_widget(self.layout)

    def add_task(self, instance):
        new_task = self.task_input.text
        due_date = self.due_date_input.text

        if new_task:
            task_info = {'task': new_task,
                         'created_at': str(datetime.now()),
                         'due_date': due_date,
                         'completed': False}

            self.app.store.put(new_task, **task_info)
            self.task_input.text = ''
            self.due_date_input.text = ''

    def delete_task(self, instance):
        task_name = self.task_input.text
        if task_name in self.app.store:
            task_info = self.app.store.get(task_name)
            self.app.deleted_store.put(task_name, **task_info)
            self.app.store.delete(task_name)


    def complete_task(self, instance):
        task_name = self.task_input.text
        if task_name in self.app.store:
            task_info = self.app.store.get(task_name)
            task_info['completed'] = True
            self.app.store.put(task_name, **task_info)

    def show_undeleted_tasks(self, instance):
        self.manager.current = 'undeleted_tasks'

    def show_deleted_tasks(self, instance):
        self.manager.current = 'deleted_tasks'


class UndeletedTasksScreen(Screen):
    def __init__(self, **kwargs):
        super(UndeletedTasksScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        show_home_button = Button(text='Back to Home', on_press=self.show_home, size_hint=(0.15,0.08))
        self.task_list_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        self.layout.add_widget(show_home_button)
        self.layout.add_widget(self.task_list_layout)

        self.add_widget(self.layout)

    def show_home(self, instance):
        self.manager.current = 'home'

    def on_pre_enter(self):
        self.show_tasks()

    def show_tasks(self):
        self.task_list_layout.clear_widgets()
        for task_name in self.app.store.keys():
            task_info = self.app.store.get(task_name)
            task_label = Label(text=f'{task_name} (Created: {task_info["created_at"]}, Due: {task_info["due_date"]})'
                                   f'{" - Completed" if task_info["completed"] else ""}',
                               size_hint_y=None, height=30)
            self.task_list_layout.add_widget(task_label)


class DeletedTasksScreen(Screen):
    def __init__(self, **kwargs):
        super(DeletedTasksScreen, self).__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        show_home_button = Button(text='Back to Home', on_press=self.show_home, size_hint=(0.15,0.08))
        self.deleted_task_list_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)
        self.layout.add_widget(show_home_button)
        self.layout.add_widget(self.deleted_task_list_layout)

        self.add_widget(self.layout)

    def show_home(self, instance):
        self.manager.current = 'home'

    def on_pre_enter(self):
        self.show_deleted_tasks()

    def show_deleted_tasks(self):
        self.deleted_task_list_layout.clear_widgets()
        for task_name in self.app.deleted_store.keys():
            task_info = self.app.deleted_store.get(task_name)
            task_label = Label(text=f'{task_name} (Created: {task_info["created_at"]}, Due: {task_info["due_date"]})'
                                   f'{" - Completed" if task_info["completed"] else ""}',
                               size_hint_y=None, height=30)
            self.deleted_task_list_layout.add_widget(task_label)


class TodoApp(App):
    def build(self):
        self.store = JsonStore('tasks.json')
        self.deleted_store = JsonStore('deleted_tasks.json')

        # Create ScreenManager
        self.sm = ScreenManager()

        # Create screens
        home_screen = HomeScreen(name='home')
        undeleted_tasks_screen = UndeletedTasksScreen(name='undeleted_tasks')
        deleted_tasks_screen = DeletedTasksScreen(name='deleted_tasks')

        # Set the app reference for screens to access the app
        home_screen.app = self
        undeleted_tasks_screen.app = self
        deleted_tasks_screen.app = self

        # Add screens to the ScreenManager
        self.sm.add_widget(home_screen)
        self.sm.add_widget(undeleted_tasks_screen)
        self.sm.add_widget(deleted_tasks_screen)

        return self.sm

if __name__ == '__main__':
    TodoApp().run()
