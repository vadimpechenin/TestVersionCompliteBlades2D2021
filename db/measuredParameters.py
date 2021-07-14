"""
Сущность из БД - номинальные измеренные значения параметров
"""

import sqlalchemy as sa

from .base import Base
from sqlalchemy.orm import relationship

class MeasuredParameters(Base):
    __tablename__ = 'measure'
    part_id = sa.Column(sa.Integer(), primary_key=True)
    type_id = sa.Column(sa.Integer, sa.ForeignKey('nominal.type_id'), nullable=False)
    delta_thickness = sa.Column(sa.Float)
    delta_angle = sa.Column(sa.Float)
    measure = relationship('NumbersOfMeasuredBlades', backref='measure', uselist=False)

    def __repr__(self):
        # для печати строки и отладки
        return '<Characteristics[type_id="{}", delta_thickness="{}", delta_angle="{}"]>'.format(
            self.type_id, self.delta_thickness, self.delta_angle)