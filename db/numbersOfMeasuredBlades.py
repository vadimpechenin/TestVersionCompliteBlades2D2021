"""
Сущность из БД - порядковые номера лопаток в комплектах
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class NumbersOfMeasuredBlades(Base):
    __tablename__ = 'numbers'
    number_id = sa.Column(sa.Integer(), primary_key=True)
    part_id = sa.Column(sa.Integer, sa.ForeignKey('measure.part_id'), nullable=False)
    type_id = sa.Column(sa.Integer, sa.ForeignKey('nominal.type_id'), nullable=False)
    serial_number = sa.Column(sa.Integer)


    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[number_id="{}", part_id="{}", type_id="{}", serial_number="{}"]>'.format(
            self.number_id, self.part_id, self.type_id, self.serial_number)