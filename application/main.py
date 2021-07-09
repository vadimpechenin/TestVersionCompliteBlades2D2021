"""
Тестовая программа для запуска приложения
по комплектации лопаток компрессора
"""
#Кkассы для работы приложения
from handlers.mainHandler import MainHandler

from forms.mainForm import MainForm

from model.applicationSettings import ApplicationSettings

mainHandler= MainHandler()
appSettings = ApplicationSettings()
"""
from db.mainSQL import SQLDataBase
data_base = SQLDataBase('set_of_blades')
data_base.table_create()
data_base.create_session()
data_base.init_repletion_data_base()
"""

app = MainForm(mainHandler,appSettings)
app.show()