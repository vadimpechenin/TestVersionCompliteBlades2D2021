"""
Сущность из БД - номинальные значения параметров
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class NominalParameters(Base):
    __tablename__ = 'nominal'
    type_id = sa.Column(sa.Integer(), primary_key=True)
    thickness_nom = sa.Column(sa.Float) #Номинальное значение толщины без натяга
    thickness = sa.Column(sa.Float) #Номинальное значение толщины, обеспечивающее натяг
    T_thickness_lower = sa.Column(sa.Float) #Допуск на толщину, нижняя граница
    T_thickness_upper = sa.Column(sa.Float) #Допуск на толщину, верхняя граница
    thickness_T = sa.Column(sa.Float) #толщина до точки вращения со стороны корыта
    thickness_B = sa.Column(sa.Float) #толщина до точки вращения со стороны спинки
    thickness_T_nom = sa.Column(sa.Float)
    thickness_B_nom = sa.Column(sa.Float)
    angle = sa.Column(sa.Float) # Угол антивибрационной полки
    T_angle_lower = sa.Column(sa.Float) #Допуск на угол, нижняя граница
    T_angle_upper = sa.Column(sa.Float)  # Допуск на угол, верхняя граница
    # Толщина полки со стороны корыта
    shelf_width_T = sa.Column(sa.Float)
    shelf_width_half_T = sa.Column(sa.Float)  #
    T_shelf_width_half_T_lower = sa.Column(sa.Float) #
    T_shelf_width_half_T_upper = sa.Column(sa.Float)  #

    # Толщина полки со стороны спинки
    shelf_width_B = sa.Column(sa.Float)
    shelf_width_half_B = sa.Column(sa.Float)  #
    T_shelf_width_half_B_lower = sa.Column(sa.Float)  #
    T_shelf_width_half_B_upper = sa.Column(sa.Float)  #

    #%Угол и расстояния для срезов лопаток
    angle_slice = sa.Column(sa.Float)
    slice_B = sa.Column(sa.Float) #со стороны спинки
    slice_T = sa.Column(sa.Float) #со стороны корыта

    measure = relationship('MeasuredParameters', backref='nominal', uselist=False)  # one to one
    number = relationship('NumbersOfMeasuredBlades', backref='nominal', uselist=False)  # one to one

    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[type_id="{}", thickness_nom="{}", thickness="{}"]>'.format(
            self.type_id, self.thickness_nom, self.characteristics_id, self.thickness)