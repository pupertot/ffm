# Represents a collection of Entities

from Entity import Entity

class Column(object):    
    def __init__(self, col):
        self.column = col
        self.entities = []
        self.entityCount = 0
    
    # Adds an Entity to the top of the Column       
    def addEntity(self, col, char):
        self.entities.append(Entity(self.entityCount, col, char))             
        self.entityCount += 1
    
    # Returns a textual representation of a the column
    def __str__(self):
        output = ''
        for entity in self.entities:
            output = str(entity.type) + '\n' + output
        return output
    
    # Simulates the dropping of everything droppable in the world
    # The attributes of the world and everything in it will be updated accordingly
    def drop_all(self):                
        runs = 0
        while 1:
            runs += 1
            changes = 0            
            for x in range(0, self.entityCount):                
                changes += self.entities[x].modify(self)                            
            if changes == 0:
                break         
        