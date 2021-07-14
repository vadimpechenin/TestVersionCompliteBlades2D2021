
class ApplicationSettings():
    number_of_blades_name = 'number_of_blades' # Количество лопаток
    T_thickness_name = 'T_thickness' # Допуск на толщину
    T_angle_name = 'T_angle'  # Допуск на угол
    delta_thickness_name = 'delta_thickness' # Отклонения толщины
    delta_angle_name = 'delta_angle'   # Отклонения углов
    thickness_name = 'thickness'    # Номинальное значение толщины, обеспечивающее натяг
    thickness_T_name = 'thickness_T' # толщина до точки вращения со стороны корыта
    thickness_B_name = 'thickness_B' # толщина до точки вращения со стороны спинки
    thickness_T_nom_name = 'thickness_T_nom'    # Номинальное значение толщины, обеспечивающее натяг
    thickness_B_nom_name = 'thickness_B_nom' # толщина до точки вращения со стороны корыта
    angle_name = 'angle' # Угол антивибрационной полки
    # Толщина полки со стороны корыта
    shelf_width_T_name = 'shelf_width_T'
    shelf_width_half_T_name = 'shelf_width_half_T'
    T_shelf_width_half_T_name = 'T_shelf_width_half_T'
    # Толщина полки со стороны спинки
    shelf_width_B_name = 'shelf_width_B'
    shelf_width_half_B_name = 'shelf_width_half_B'
    T_shelf_width_half_B_name = 'T_shelf_width_half_B'
    # Угол и расстояния для срезов лопаток
    angle_slice_name = 'angle_slice'
    slice_B_name = 'slice_B'
    slice_T_name = 'slice_T'
    # Название файда базы данных
    filedb_name = 'filedb'
    # Производные параметры
    pointsBackThroughParams_name = 'pointsBackThroughParams'
    # Порядок лопаток
    arrayNumberOfBlades_name = 'arrayNumberOfBlades'

    # Сборочные параметры
    assemblyChord_name = 'assemblyChord'
    assemblyGaps_name = 'assemblyGaps'
    values = {}

    def __init__(self):
        self.initEmptySettings()

    def initEmptySettings(self):
        #Создание всех имен переменных
        self.values[self.number_of_blades_name] = None
        self.values[self.T_thickness_name] = None
        self.values[self.T_angle_name] = None
        self.values[self.delta_thickness_name] = None
        self.values[self.delta_angle_name] = None
        self.values[self.thickness_name] = None
        self.values[self.thickness_T_name] = None
        self.values[self.thickness_B_name] = None
        self.values[self.thickness_T_nom_name] = None
        self.values[self.thickness_B_nom_name] = None
        self.values[self.angle_name] = None
        self.values[self.shelf_width_T_name] = None
        self.values[self.shelf_width_half_T_name] = None
        self.values[self.T_shelf_width_half_T_name] = None
        self.values[self.shelf_width_B_name] = None
        self.values[self.shelf_width_half_B_name] = None
        self.values[self.T_shelf_width_half_B_name] = None
        self.values[self.angle_slice_name] = None
        self.values[self.slice_B_name] = None
        self.values[self.slice_T_name] = None
        self.values[self.filedb_name] = ''
        self.values[self.pointsBackThroughParams_name] = None
        self.values[self.arrayNumberOfBlades_name] = None
        self.values[self.assemblyChord_name] = None
        self.values[self.assemblyGaps_name] = None

    def getNames(self):
        #Возвращает все названия параметров, необходимых для приложения
        keys=[]
        for key, value in self.values.items():
            keys.append(key)
        return keys

    def GetValue(self,name):
        #Метод для получения значения параметра
        value = self.values[name]
        return value

    def SetValue(self,name,value):
        #Метод для изменения значения параметра
        for key, v in self.values.items():
            if name==key:
                self.values[name] = value