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
from utils.datatable import DataTable
from datetime import datetime
import hashlib
import mysql.connector


Builder.load_file('admin/admin.kv')
class Notify(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint=(.5,.3)
class AdminWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.mydb=mysql.connector.connect(host='localhost', user='root', password='root', database='traffika')
        self.mycursor=self.mydb.cursor()
        self.notify=Notify()

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
        self.ids.target_violation.values=spinvals

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

    def add_user(self,first,last,user,pwd,id):
        if first=='' or last=='' or user=='' or pwd=='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields are Required![/b][/color]',markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch,1)
        else:
            sql='INSERT INTO users(first_name, last_name, user_name, password, id_no,date) VALUES(%s,%s,%s,%s,%s,%s)'
            values=[first,last,user,pwd,id,datetime.now()]

            self.mycursor.execute(sql, values)
            self.mydb.commit()
            content = self.ids.scrn_contents
            content.clear_widgets()

            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

    def killswitch(self,dtx):
        self.notify.dismiss()
        self.notify.clear_widgets()

    def add_vehicle(self, plate, id,model, status):
        if plate=='' or id=='' or model=='' or status =='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]All Fields are Required![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            sql = 'INSERT INTO vehicles(number_plate, owner_id, model, status) VALUES(%s,%s,%s,%s)'
            values = [plate, id, model, status]

            self.mycursor.execute(sql, values)
            self.mydb.commit()

            content = self.ids.scrn_vehicle_contents
            content.clear_widgets()

            vehicles = self.get_vehicles()
            vehicle_table = DataTable(table=vehicles)
            content.add_widget(vehicle_table)


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

    def update_user(self, first, last, user, pwd,id):
        pwd = hashlib.sha256(pwd.encode()).hexdigest()
        if user=='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            sql = 'UPDATE users SET first_name=%s,last_name=%s,user_name=%s,password=%s,id_no=%s WHERE user_name=%s'
            values = [first, last, user, pwd, id, user]
            content = self.ids.scrn_contents
            content.clear_widgets()
            self.mycursor.execute(sql, values)
            self.mydb.commit()

            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

    def update_vehicle(self, plate, owner_id, model, status):
        if plate=='':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Number Plate Required![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            content = self.ids.scrn_vehicle_contents
            content.clear_widgets()
            sql = 'UPDATE vehicles SET number_plate=%s,owner_id=%s,model=%s,status=%s WHERE number_plate=%s'
            values = [plate, owner_id, model, status, plate]

            self.mycursor.execute(sql, values)
            self.mydb.commit()

            vehicles = self.get_vehicles()
            vehicle_table = DataTable(table=vehicles)
            content.add_widget(vehicle_table)

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
            content = self.ids.scrn_contents
            content.clear_widgets()
            sql = 'DELETE FROM users WHERE user_name = %s'
            values = [user]
            self.mycursor.execute(sql, values)
            self.mydb.commit()

            users = self.get_users()
            userstable = DataTable(table=users)
            content.add_widget(userstable)

    def remove_vehicle(self, plate):
        if plate == '':
            self.notify.add_widget(Label(text='[color=#FF0000][b]Invalid Username![/b][/color]', markup=True))
            self.notify.open()
            Clock.schedule_once(self.killswitch, 1)
        else:
            content = self.ids.scrn_vehicle_contents
            content.clear_widgets()
            sql = 'DELETE FROM vehicles WHERE number_plate = %s'
            values = [plate]
            self.mycursor.execute(sql, values)
            self.mydb.commit()

            vehicles = self.get_users()
            vehicles_table = DataTable(table=vehicles)
            content.add_widget(vehicles_table)


    def get_users(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='traffika'
        )
        mycursor = mydb.cursor()
        _users = OrderedDict()
        _users['First Name'] = {}
        _users['Last Name'] = {}
        _users['User Name'] = {}
        _users['Password'] = {}
        _users['ID No'] = {}
        first_names = []
        last_names = []
        user_names = []
        passwords = []
        id_no = []

        sql = 'SELECT * FROM users'
        mycursor.execute(sql)
        users = mycursor.fetchall()
        for user in users:
            first_names.append(user[1])
            last_names.append(user[2])
            user_names.append(user[3])
            pwd = user[4]
            if len(pwd) > 10:
                pwd = pwd[:10] + '...'
            passwords.append(pwd)
            id_no.append(user[5])

        users_length = len(first_names)
        idx = 0
        while idx < users_length:
            _users['First Name'][idx] = first_names[idx]#These(the names in the quotes) could bring an issue later on
            _users['Last Name'][idx] = last_names[idx]#These(the names in the quotes) could bring an issue later on
            _users['User Name'][idx] = user_names[idx]#These(the names in the quotes) could bring an issue later on
            _users['Password'][idx] = passwords[idx]#These(the names in the quotes) could bring an issue later on
            _users['ID No'][idx] = id_no[idx]#These(the names in the quotes) could bring an issue later on

            idx += 1

        return _users

    def get_violations(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='traffika'
        )
        mycursor = mydb.cursor()
        _violation = OrderedDict()
        _violation['vehicle_involved'] = {}
        _violation['owner id'] = {}
        _violation['violation_type'] = {}
        _violation['date/time'] = {}
        _violation['witness'] = {}

        vehicle_involved=[]
        owner_id = []
        violation_type=[]
        date_time=[]
        witness=[]

        sql = 'SELECT * FROM violations'
        mycursor.execute(sql)
        violations = mycursor.fetchall()
        for violation in violations:
            vehicle_involved.append(violation[1])
            owner_id.append(violation[0])
            violation_type.append(violation[2])
            date_time.append(violation[3])
            try:
                witness.append(violation[4])
            except KeyError:
                witness.append('')

        vehicles_length = len(owner_id)
        idx = 0
        while idx < vehicles_length:
            _violation['vehicle_involved'][idx] = vehicle_involved[idx]
            _violation['owner id'][idx] = owner_id[idx]
            _violation['violation_type'][idx] = violation_type[idx]
            _violation['date/time'][idx] = date_time[idx]
            _violation['witness'][idx] = witness[idx]

            idx += 1

        return _violation

    def get_vehicles(self):
        mydb = mysql.connector.connect(
            host='localhost',
            user='root',
            password='root',
            database='traffika'
        )
        mycursor = mydb.cursor()
        _vehicle = OrderedDict()
        _vehicle['number_plate'] = {}
        _vehicle['owner id'] = {}
        _vehicle['model'] = {}
        _vehicle['status'] = {}

        number_plate = []
        owner_id = []
        model = []
        status = []

        sql = 'SELECT * FROM vehicles'
        mycursor.execute(sql)
        vehicles = mycursor.fetchall()
        for vehicle in vehicles:
            number_plate.append(vehicle[0])
            owner_id.append(vehicle[1])
            model.append(vehicle[2])
            status.append(vehicle[3])

        vehicles_length = len(number_plate)
        idx = 0
        while idx < vehicles_length:
            _vehicle['number_plate'][idx] = number_plate[idx]
            _vehicle['owner id'][idx] = owner_id[idx]
            _vehicle['model'][idx] = model[idx]
            _vehicle['status'][idx] = status[idx]

            idx += 1

        return _vehicle

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