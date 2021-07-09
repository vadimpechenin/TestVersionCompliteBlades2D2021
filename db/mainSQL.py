"""
Класс для работы с базой данных
"""
import math
import numpy as np
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from db.supportFunctions import resultproxy_to_dict

from .base import Session, current_session, Base
from .measuredParameters import MeasuredParameters
from .nominalParameters import NominalParameters

class SQLDataBase():

    def __init__(self,name_of_database):
        #name_of_database = 'set_of_blades'
        self.engine = create_engine('sqlite:///' + name_of_database, echo = True)

    def table_create(self):
        #Метод для создания таблиц и базы данных
       Base.metadata.create_all(self.engine)

    def create_session(self):
        #Создание сессии, через которую мапяться объекты
        self.session = sessionmaker(bind=self.engine)()

    def init_repletion_data_base(self):
        # Создание объектов в таблице NominalParameters
        thickness_T_nom =11.1*24.73/25.13
        thickness_B_nom = 24.73 - thickness_T_nom
        type_object = NominalParameters(thickness_nom = 24.73, thickness = 25.13, T_thickness_lower = -0.1,
                                        T_thickness_upper = 0.15, thickness_T = 11.1, thickness_B = 25.13-11.1,
                                        thickness_T_nom = thickness_T_nom, thickness_B_nom = thickness_B_nom,
                                        angle = 30/180*math.pi, T_angle_lower = -1/6/180*math.pi,
                                        T_angle_upper = 1/6/180*math.pi, shelf_width_T = 11.75, shelf_width_half_T = 6,
                                        T_shelf_width_half_T_lower = -0.1, T_shelf_width_half_T_upper = 0.1,
                                        shelf_width_B = 11.5, shelf_width_half_B = 6.8, T_shelf_width_half_B_lower = -0.1,
                                        T_shelf_width_half_B_upper =  0.1, angle_slice = 50/180*math.pi, slice_B = 16.05,
                                        slice_T = 12.7)
        self.session.add(type_object)
        self.session.commit()
    def generated_data_save_data_base(self,delta_thickness,delta_angle):
        # Создание объектов в таблице MeasuredParameters
        #Генерация значений, временно здесь, нужно переносить в отдельную функцию mainHandler-а
        # Добавать в сессию
        for thickness, angle in zip(delta_thickness,delta_angle):
            measured_object = MeasuredParameters(type_id=1, delta_thickness=thickness, delta_angle=angle)
            self.session.add(measured_object)
        self.session.commit()

    def select_all_parans_in_table(self,name):
        # Функция для подачи запроса
        request_str = "SELECT * \
                           FROM \
                           " + str(name)
        s = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s)
        return result_of_query

    def request_delete_of_measured(self,name):
        #Запрос на удаление всего из таблицы measure
        request_str = "DELETE FROM " + str(name) +" \
                           WHERE type_id = 1"
        self.session.execute(request_str)

    def request_count_of_blades(self, name):
        # Запрос на подсчет количества лопаток в базе данных
        request_str = "SELECT count(part_id) AS Количество \
                        FROM " + str(name)
        s = self.session.execute(request_str)
        result_of_query = resultproxy_to_dict(s)
        return result_of_query