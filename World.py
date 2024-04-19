# Represents a collection of Columns

from Column import Column
from Entity import Entity

# The following is an example of how the initial list of entities must be formatted:
#       '   .,. . , :T.,. . ,. . '
# Each repetition is separated by a comma, and the order they are listed in the string will be the order they are inserted into the world.  
# Meaning, the first repetition is the first/bottom row.   And they are stacked consecutively as they are extracted from the list.  
class World(object):    
    def __init__(self, worldId, entities):
        self.id = worldId
        self.initialState = entities
        self.endState = None
        self.columns = []
        self.width = 0
        self.height = 0
        self.updated = 0

        self._build_columns()
        self.set_end_state()    

    # Populates the appropriate number of Columns with Entities based on the data provided when creating the world
    def _build_columns(self): 
        width = 0       
        rowList = self.initialState.split(',')
        self.height = len(rowList)        
        self.width = len(rowList[0])       

        for x in range(0, self.width):
            self.columns.append(Column(x))            

        for row in rowList:
            for x in range(0, self.width):                        
                rowNum = self.columns[x].entityCount            
                if x > len(row):            
                    self.columns[x].addEntity(x, ' ')
                else:
                    self.columns[x].addEntity(x, row[x])                      
    
    # Adds a row of Entities to the world.
    # New rows cannot be wider than the existing world because reasons.
    def add_row(self, row):               
        for x in range(0, self.width):                        
            rowNum = self.columns[x].entityCount            
            if x > len(row):            
                self.columns[x].addEntity(x, ' ')
            else:
                self.columns[x].addEntity(x, row[x])
        self.height += 1        
    
    # Initiates the end days
    def set_end_state(self):        
        for column in self.columns:
            column.drop_all()
        
        rows = ''
        for x in range(0, self.height):
            for column in self.columns:  
                rows += str(column.entities[x].type)
            rows += ','        
        self.endState = rows    
    
    # Returns a textual representation of either the initial state of the world, or the end state after everything has fallen.  
    # The first parameter should be "end" to see the end state, and anything else to see the initial state.
    # The second parameter determines the format of the textual string that is returned.   Options:
    #   'html' - Rows are separated by '<br>'
    #   'url' - Rows are separated by '%0A' and spaces are represented by '%20'
    #   'raw' - The end/initial state is returned as-is, which is a comma delimited list of '.', ':', ' ', and/or 'T' characters.
    #   'newline' - Rows are separated by '\n'
    def __format__(self, state, strFormat):
        output = ''
        if state == 'end':
            rows = self.endState.split(',')
        else:
            rows = self.initialState.split(',')
        for row in rows:
            if strFormat == 'raw':                
                output = self.endState
            elif strFormat == 'newline':
                output = row + '\n' + output
            elif strFormat == 'html':
                output = row + '<br>' + output
            elif strFormat == 'url':
                output = row + '%0A' + output.replace(' ', '%20')
            else:
                output = 'Invalid format requested.'
        return output  
