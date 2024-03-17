
from kivy.app import App
import mysql.connector
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder


Builder.load_file('home/home.kv')
class HomeWindow(BoxLayout):
    def submit_text(self, instance):
        text_to_submit = self.root.ids.text_input.text
        if text_to_submit:
            self.save_to_database(text_to_submit)
            self.root.ids.text_input.text = ''  # Clear the input after submission
        else:
            self.notify.add_widget(Label(text='[color=#FF0000][b]Submition [/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)

    def killswitch(self, dtx):
                self.notify.dismiss()
                self.notify.clear_widgets()


    def save_to_database(self, text):
        try:

            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='traffika'
            )
            cursor = connection.cursor()


            query = "INSERT INTO reports (text) VALUES (%s)"
            data = (text,)

            cursor.execute(query, data)
            connection.commit()

            print("Text submitted successfully to the database!")

        except mysql.connector.Error as e:
            print(f"Error: {e}")

        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
class Home(App):
    def build(self):

        return HomeWindow()
if __name__ == '__main__':
    Home().run()
