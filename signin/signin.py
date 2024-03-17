from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
import hashlib
import mysql.connector
from kivy.lang import Builder


Builder.load_file('signin/signin.kv')
class SigninWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def validate_user(self):
        try:
            # Establish a connection to the MySQL database
            connection = mysql.connector.connect(
                host='localhost',
                user='root',
                password='root',
                database='traffika'
            )

            cursor = connection.cursor()

            # Retrieve user input
            uname = self.ids.username_field.text
            passw = self.ids.pwd_field.text

            self.ids.username_field.text = ''
            self.ids.pwd_field.text = ''

            # Check for empty fields
            if uname == '' or passw == '':
                self.ids.info.text = '[color=#FF0000]username and/or password required[/color]'
            else:
                # Query to retrieve user information from the MySQL database
                query = "SELECT * FROM users WHERE user_name = %s"
                cursor.execute(query, (uname,))
                users = cursor.fetchall()

                if not users:
                    self.ids.info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'
                else:
                    user=users[0]
                    # Hash the entered password and compare with the stored hashed password
                    passw = hashlib.sha256(passw.encode()).hexdigest()
                    print(passw)
                    if passw == user[4]:  # Assuming password is in the third column

                        if user[7]=='admin':

                            self.ids.info.text = ''
                            self.parent.parent.current = 'scrn_admin'
                        else:
                            self.ids.info.text = ''
                            self.parent.parent.current = 'scrn_home'

                    else:
                        self.ids.info.text = '[color=#FF0000]Invalid Username and/or Password[/color]'
                        self.ids.info.text = passw

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            if 'connection' in locals() and connection.is_connected():
                cursor.close()
                connection.close()

class SigninApp(App):
    def build(self):
        return SigninWindow()

if __name__ == "__main__":
    sa = SigninApp()
    sa.run()
