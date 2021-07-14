from handlers.baseCommandHandler import BaseCommandHandler
import numpy as np

class PlacementBladesCommandHandler(BaseCommandHandler):
    def __init__(self):
        pass

    def execute(self, parameters):
        # Расстановка лопаток для равномерного распределения натягов
        # parameters.delta_chord_T_array - Отклонение хорды (площади) на корытах
        # parameters.delta_chord_B_array - Отклонение хорды (площади) на спинках
        # parameters.gap - Отклонение хорды (площади) на спинках
        # Сортировка по значениям толщин
        # Прямая для спинок
        idx_B = np.argsort(parameters.assemblyGaps.delta_chord_B_array)
        # Обратная для корыт
        idx_T = np.argsort(parameters.assemblyGaps.delta_chord_T_array)[::-1]

        idx_new = []
        k1 = 0
        while idx_B.shape[0]>0:
            if (k1==0):
                idx_new.append(idx_B[0])
                idx_obh=np.where(idx_T==idx_B[0])
                idx_T = np.delete(idx_T, idx_obh)
                idx_B = np.delete(idx_B, 0)
                k1 = 1
            else:
                idx_new.append(idx_T[0])
                idx_obh=np.where(idx_B==idx_T[0])
                idx_B = np.delete(idx_B, idx_obh)
                idx_T = np.delete(idx_T, 0)
                k1 = 0

        arrayNumberOfBlades_sort = np.asarray(idx_new, dtype=np.int64)
        return arrayNumberOfBlades_sort
