from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.lang import Builder
from datetime import datetime

Builder.load_file('register/register.kv')


class RegisterWindow(FloatLayout):
    def __int_(self, **kwargs):
        super().__init__(self, **kwargs)

    def registration(self):
        first_name = self.ids.first_name.text
        last_name = self.ids.last_name.text
        user_name = self.ids.user_name.text
        password = self.ids.password.text
        id_no = self.ids.id_no.text
        date = datetime.now()

    def switch_to_signin(self):
        self.parent.parent.current = 'scrn_si'


class RegisterApp(App):
    def build(self):
        return RegisterWindow()


if __name__ == '__main__':
    RegisterApp().run()
