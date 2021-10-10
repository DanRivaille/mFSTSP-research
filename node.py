class Node():
    def __init__(self, data_row, nodeId):
        self.id = nodeId
        self.type = int(data_row['nodeType'])
        self.x = data_row['latDeg']
        self.y = data_row['lonDeg']
        self.z = data_row['altMeters']
        self.weight = data_row['parcelWtLbs']

    def __str__(self):
        string = f'Id: {self.id} - Type: {self.type}'
        string += f' - Pos(x,y,z): ({round(self.x, 4)}, {round(self.y, 4)}, {round(self.z, 4)})'
        string += f' - Weight: {self.weight}'
        return string

    def __repr__(self):
        return self.__str__()

