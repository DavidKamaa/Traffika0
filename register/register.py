
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.properties import ObjectProperty
from kivy.lang import Builder


Builder.load_file('register/register.kv')

class MyLayout(FloatLayout):
    name = ObjectProperty(None)
    regno = ObjectProperty(None)
    course = ObjectProperty(None)
    year = ObjectProperty(None)
    sem = ObjectProperty(None)

class RegisterApp(App):
    def build(self):
        return MyLayout()


if __name__ == '__main__':
    RegisterApp().run()
