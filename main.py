from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from admin.admin import AdminWindow
from home.home import HomeWindow
from signin.signin import SigninWindow

class MainWindow(Screen):
    signin_widget = SigninWindow()
    admin_widget = AdminWindow()
    home_widget = HomeWindow()
    def __init__(self, **kwargs):
        super(MainWindow, self).__init__(**kwargs)

        self.ids.scrn_si.add_widget(self.signin_widget)
        self.ids.scrn_admin.add_widget(self.admin_widget)
        self.ids.scrn_home.add_widget(self.home_widget)

class MainApp(App):
    def build(self):
        return MainWindow()

if __name__ == '__main__':
    MainApp().run()
