# Represents a row of Entity objects

from Entity import Entity

class Row(object):    
    def __init__(self, col):
        self.column = col
        self.entities = []
    
    def addEntity(self, pos, char):
        self.entities.append(Entity(pos, char))
    
    def __repr__(self):
        output = ''
        for entity in self.entities:
            output = output + str(entity.type)
        return output
        