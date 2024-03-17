from kivy.app import App
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.modalview import ModalView
from kivy.lang import Builder

from collections import OrderedDict

from mysql.connector.django.client import DatabaseClient

from utils.datatable import DataTable
from datetime import datetime
import hashlib
import mysql.connector
import requests
import json


#Builder.load_file('admin/admin.kv')
class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(.5,.3)
class AdminWindow(BoxLayout):
    php_endpoint = 'http://traffika.atwebpages.com/database.php'
    php_endpoint2 = 'http://traffika.atwebpages.com/database2.php'

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        '''self.mydb=mysql.connector.connect(host='localhost', user='root', password='root', database='traffika')
        self.mycursor=self.mydb.cursor()
        

        sql = 'SELECT * FROM violations'
        self.mycursor.execute(sql)
        self.violations = self.mycursor.fetchall()
        vehicle_involved=[]
        violation_type=[]
        spinvals=[]
        for violation in self.violations:
            vehicle_involved.append(violation[1])
            if len(vehicle_involved) > 30:
                pwd = pwd[:30] + '...'
            violation_type.append(violation[2])
        for x in range(len(vehicle_involved)):
            line = " | ".join([vehicle_involved[x],violation_type[x]])
            spinvals.append(line)
        self.ids.target_violation.values=spinvals'''
        self.notify = Notify()

        content=self.ids.scrn_contents
        users=self.get_users()

        userstable=DataTable(table=users)
        content.add_widget(userstable)

        vehicle_scrn = self.ids.scrn_vehicle_contents
        vehicles = self.get_vehicles()
        vehicle_table = DataTable(table=vehicles)
        vehicle_scrn.add_widget(vehicle_table)

        violation_scrn = self.ids.scrn_violations


        violations = self.get_violations()
        violations_table = DataTable(table=violations)
        violation_scrn.add_widget(violations_table)

    def add_user_fields(self):
        target=self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_id = TextInput(hint_text='Id No')
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_user(crud_first.text, crud_last.text, crud_user.text,
                                                                   crud_pwd.text, crud_id.text))
        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_id)
        target.add_widget(crud_submit)

    def add_vehicle_fields(self):
        target = self.ids.ops_fields_veh
        target.clear_widgets()

        crud_plate = TextInput(hint_text='Number Plate')
        crud_owner_id = TextInput(hint_text="Owner's ID")
        crud_model = TextInput(hint_text='Model')
        crud_status = TextInput(hint_text='Vehicle Status')
        crud_submit = Button(text='Add', size_hint_x=None, width=100,
                             on_release=lambda x: self.add_vehicle(crud_plate.text, crud_owner_id.text, crud_model.text,
                                                                crud_status.text))

        target.add_widget(crud_plate)
        target.add_widget(crud_owner_id)
        target.add_widget(crud_model)
        target.add_widget(crud_status)
        target.add_widget(crud_submit)

    def add_user(self, first, last, user, pwd, idno):
        if first == '' or last == '' or user == '' or pwd == '':
            self.notify.add_widget(
                Label(text='[color=#FF0000][b]All Fields are Required![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            table_name = "users"
            designation="user"
            values = [first, last, user, pwd, idno, designation]
            data = {'table': table_name, 'values': values}  # Send values along with the query
            response = requests.post(self.php_endpoint2, json=data)
            print(response.text)

            # No need to execute the SQL query locally anymore
            if response.status_code == 200:
                content = self.ids.scrn_contents
                content.clear_widgets()

                users = self.get_users()
                userstable = DataTable(table=users)
                content.add_widget(userstable)

            else:
                # Handle errors appropriately
                print("Error:", response.text)

    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_vehicle(self, plate, id,model, status):
        if plate=='' or id=='' or model=='' or status =='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields are Required![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            table_name = "vehicles"
            values = [plate, id, model, status]

            data = {'table': table_name, 'values': values}  # Send values along with the query
            response = requests.post(self.php_endpoint2, json=data)
            print(response.text)

            # No need to execute the SQL query locally anymore
            if response.status_code == 200:
                content = self.ids.scrn_contents
                content.clear_widgets()

                users = self.get_users()
                userstable = DataTable(table=users)
                content.add_widget(userstable)

            else:
                # Handle errors appropriately
                print("Error:", response.text)


    def update_user_fields(self):
        target=self.ids.ops_fields
        target.clear_widgets()
        crud_first = TextInput(hint_text='First Name')
        crud_last = TextInput(hint_text='Last Name')
        crud_user = TextInput(hint_text='User Name')
        crud_pwd = TextInput(hint_text='Password')
        crud_id = TextInput(hint_text='Id No')
        crud_submit = Button(text='Update', size_hint_x=None, width=100,on_release=lambda x:self.update_user(crud_first.text,crud_last.text,crud_user.text,crud_pwd.text,crud_id.text))

        target.add_widget(crud_first)
        target.add_widget(crud_last)
        target.add_widget(crud_user)
        target.add_widget(crud_pwd)
        target.add_widget(crud_id)
        target.add_widget(crud_submit)

    def update_vehicle_fields(self):
        target=self.ids.ops_fields_veh
        target.clear_widgets()
        crud_plate = TextInput(hint_text='Number Plate')
        crud_owner_id = TextInput(hint_text="Owner's ID")
        crud_model = TextInput(hint_text='Model')
        crud_status = TextInput(hint_text='Vehicle Status')
        crud_submit = Button(text='Update Vehicle', size_hint_x=None, width=100,
                             on_release=lambda x: self.update_vehicle(crud_plate.text, crud_owner_id.text,
                                                                      crud_model.text, crud_status.text))

        target.add_widget(crud_plate)
        target.add_widget(crud_owner_id)
        target.add_widget(crud_model)
        target.add_widget(crud_status)
        target.add_widget(crud_submit)

    def update_user(self, first, last, user, pwd, id):
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            # Prepare data to be sent to PHP endpoint
            data = {
                'first_name': first,
                'last_name': last,
                'user_name': user,
                'password': pwd,
                'id_no': id
            }
            # Send a POST request to the PHP endpoint
            response = requests.post('http://traffika.atwebpages.com/updateUser.php', data=data)

            # Check if request was successful
            if response.status_code == 200:
                content = self.ids.scrn_contents
                content.clear_widgets()
                users = self.get_users()
                userstable = DataTable(table=users)
                content.add_widget(userstable)
                print(response.text)
            else:
                print("Failed to update user. Status code:", response.status_code)

    def update_vehicle(self, plate, owner_id, model, status):
        if plate == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Number Plate Required![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            # Prepare data for the request
            data = {
                'number_plate': plate,
                'owner_id': owner_id,
                'model': model,
                'status': status
            }

            # Send update request to PHP endpoint
            response = requests.post('http://traffika.atwebpages.com/updateVehicle.php', data=data)
            if response.status_code == 200:
                content = self.ids.scrn_vehicle_contents
                content.clear_widgets()
                # Update successful
                vehicles = self.get_vehicles()
                vehicle_table = DataTable(table=vehicles)
                content.add_widget(vehicle_table)
                print(response.text)
            else:
                # Handle errors appropriately
                print("Error:", response.text)

    def remove_user_fields(self):
        target = self.ids.ops_fields
        target.clear_widgets()
        crud_user = TextInput(hint_text='User Name')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_user(crud_user.text))

        target.add_widget(crud_user)
        target.add_widget(crud_submit)

    def remove_vehicle_fields(self):
        target = self.ids.ops_fields_veh
        target.clear_widgets()
        crud_plate = TextInput(hint_text='Number Plate')
        crud_submit = Button(text='Remove', size_hint_x=None, width=100,
                             on_release=lambda x: self.remove_vehicle(crud_plate.text))

        target.add_widget(crud_plate)
        target.add_widget(crud_submit)

    def remove_user(self, user):
        if user == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            # Prepare data to be sent to PHP endpoint
            data = {'user_name': user}
            # Send a POST request to the PHP endpoint
            response = requests.post('http://traffika.atwebpages.com/removeUser.php', data=data)

            # Check if request was successful
            if response.status_code == 200:
                content = self.ids.scrn_contents
                content.clear_widgets()
                users = self.get_users()
                userstable = DataTable(table=users)
                content.add_widget(userstable)
                print(response.text)
            else:
                print("Failed to remove user. Status code:", response.status_code)

    def remove_vehicle(self, plate):
        if plate == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            # Prepare data to be sent to PHP endpoint
            data = {'number_plate': plate}
            # Send a POST request to the PHP endpoint
            response = requests.post('http://traffika.atwebpages.com/removeVehicle.php', data=data)
            # Check if request was successful
            if response.status_code == 200:
                content = self.ids.scrn_vehicle_contents
                content.clear_widgets()
                vehicles = self.get_vehicles()
                vehicles_table = DataTable(table=vehicles)
                content.add_widget(vehicles_table)
                print(response.text)
            else:
                print("Failed to remove vehicle. Status code:", response.status_code)

    def get_users(self):

        sql = 'SELECT * FROM users'
        data = {'query': sql}
        response = requests.post(self.php_endpoint, json=data)

        if response.status_code == 200:
            users = response.json()

            _user = OrderedDict()
            _user['First Name'] = {}
            _user['Last name'] = {}
            _user['User Name'] = {}
            _user['Password'] = {}
            _user['ID No'] = {}
            _user['DOB'] = {}

            for idx, user in enumerate(users):
                _user['First Name'][idx] = user['first_name']
                _user['Last name'][idx] = user['last_name']
                _user['User Name'][idx] = user['user_name']
                _user['Password'][idx] = user['password']
                _user['ID No'][idx] = user['id_no']
                _user['DOB'][idx] = user.get('date_of_birth', '')

            return _user
        else:
            # Handle the case where the request was not successful
            print("Error:", response.status_code)
            return None


    def get_violations(self):
        sql = 'SELECT * FROM violations'
        data = {'query': sql}
        response = requests.post(self.php_endpoint, json=data)


        if response.status_code == 200:
            violations = response.json()

            _violation = OrderedDict()
            _violation['vehicle_involved'] = {}
            _violation['owner id'] = {}
            _violation['violation_type'] = {}
            _violation['date/time'] = {}
            _violation['witness'] = {}

            for idx, violation in enumerate(violations):
                _violation['vehicle_involved'][idx] = violation['vehicle_plate']
                _violation['owner id'][idx] = violation['violation_id']
                _violation['violation_type'][idx] = violation['violation_type']
                _violation['date/time'][idx] = violation['date_time']
                _violation['witness'][idx] = violation.get('witness', '')

            return _violation
        else:
            # Handle the case where the request was not successful
            print("Error:", response.status_code)
            return None

    def get_vehicles(self):
        sql = 'SELECT * FROM vehicles'
        data = {'query': sql}
        response = requests.post(self.php_endpoint, json=data)

        if response.status_code == 200:
            violations = response.json()

            _vehicle = OrderedDict()
            _vehicle['number_plate'] = {}
            _vehicle['owner id'] = {}
            _vehicle['model'] = {}
            _vehicle['status'] = {}

            for idx, violation in enumerate(violations):
                _vehicle['number_plate'][idx] = violation['number_plate']
                _vehicle['owner id'][idx] = violation['owner_id']
                _vehicle['model'][idx] = violation['model']
                _vehicle['status'][idx] = violation['status']

            return _vehicle
        else:
            # Handle the case where the request was not successful
            print("Error:", response.status_code)
            return None

    def view_stats(self):
        target_violation = self.ids.target_violation.text
        target=target_violation[:target_violation.find(' | ')]
        name=target_violation[target_violation.find(' | '):]

    def change_screen(self, instance):
        if instance.text == 'Manage Vehicles':
            self.ids.scrn_mngr.current='scrn_vehicle_content'
        elif instance.text == 'Manage Users':
            self.ids.scrn_mngr.current = 'scrn_content'
        elif instance.text == 'View Violations':
            self.ids.scrn_mngr.current = 'view_analysis'
        else:
            self.ids.scrn_mngr.current = 'scrn_analysis'


class AdminApp(App):
    def build(self):
        return AdminWindow()


if __name__=="__main__":
    AdminApp().run()