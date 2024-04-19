# Represents a rock (.), stack (:), table (T), or air ( )

class Entity(object):    
    def __init__(self, row, col, char):
        self.row = row
        self.column = col      
        self.type = char
        self.droppable = True
        self.changeable = True        
        if self.row == 0 or self.type == ' ':
            self.droppable = False            
        if self.type == 'T':
            self.droppable = False
            self.changeable = False
        if self.row == 0 and self.type == ':':
            self.changeable = False
    
    # Returns row, column, and char for current Entity in this format:   [<row>, <col>] <character>
    def __str__(self):
        return ('[' + str(self.row) + ',' + str(self.column) + '] ' + str(self.type))
    
    # Simulates the dropping of the entity directly above the current entity.  Various attributes of the current entity
    #   as well as the entity above it are updated if appropriate.
    # Returns:   integer
    #       1 - If any changes were made
    #       0 - If no changes were made
    #
    def modify(self, column):         
        status = self.can_change_or_drop(column)        
        self.droppable = status['drop']
        self.changeable = status['change']

        if self.changeable == False or self.row == (column.entityCount - 1):            
            return 0

        else:            
            if self.type == '.':
                if column.entities[self.row + 1].type == '.':
                    self.type = ':'
                    column.entities[self.row + 1].type = ' '
                else:
                    self.type = ':'
                    column.entities[self.row + 1].type = '.'
            else:
                self.type = column.entities[self.row + 1].type
                column.entities[self.row + 1].type = ' '
            return 1

    # Determines if the entity can be changed/dropped based on it's corrent row, type, and the Entity directly above/below it
    # Returns:   dictionary
    #       ['change'] = 1 if the entity can be changed, 0 otherwise
    #       ['drop'] = 1 if the entity can be dropped, 0 otherwise
    #           'drop' is mostly pointless at the moment, but it helps keep the Entity's attributes up to date
    #                     
    def can_change_or_drop(self, column):
        ret = {}        
        if self.type == '.':
            if self.row == (column.entityCount - 1):
                ret['change'] = True
            elif column.entities[self.row + 1].type == ':':
                ret['change'] = True
            elif column.entities[self.row + 1].type == '.':
                ret['change'] = True
            elif column.entities[self.row + 1].type == ' ':
                ret['change'] = False
            elif column.entities[self.row + 1].type == 'T':
                ret['change'] = False
            if self.row > 0:
                if column.entities[self.row - 1].type == ':':
                    ret['drop'] = False
                elif column.entities[self.row - 1].type == '.':
                    ret['drop'] = True
                elif column.entities[self.row - 1].type == ' ':
                    ret['drop'] = True
                elif column.entities[self.row - 1].type == 'T':
                    ret['drop'] = False            
            else:
                ret['drop'] = False

        elif self.type == ':':
            if self.row == (column.entityCount - 1):
                ret['change'] = False
            elif column.entities[self.row + 1].type == ':':
                ret['change'] = False
            elif column.entities[self.row + 1].type == '.':
                ret['change'] = False
            elif column.entities[self.row + 1].type == ' ':
                ret['change'] = False
            elif column.entities[self.row + 1].type == 'T':
                ret['change'] = False
            if self.row > 0:
                if column.entities[self.row - 1].type == ':':
                    ret['drop'] = False
                elif column.entities[self.row - 1].type == '.':
                    ret['drop'] = True
                elif column.entities[self.row - 1].type == ' ':
                    ret['drop'] = True
                elif column.entities[self.row - 1].type == 'T':
                    ret['drop'] = False
            else:
                ret['drop'] = False  
    
        elif self.type == 'T':          
            ret['change'] = False
            ret['drop'] = False
    
        elif self.type == ' ':
            if self.row == (column.entityCount - 1):
                ret['change'] = True
            elif column.entities[self.row + 1].type == ':':
                ret['change'] = True
            elif column.entities[self.row + 1].type == '.':
                ret['change'] = True
            elif column.entities[self.row + 1].type == ' ':
                ret['change'] = False
            elif column.entities[self.row + 1].type == 'T':
                ret['change'] = False
            if self.row > 0:
                if column.entities[self.row - 1].type == ':':
                    ret['drop'] = False
                elif column.entities[self.row - 1].type == '.':
                    ret['drop'] = False
                elif column.entities[self.row - 1].type == ' ':
                    ret['drop'] = False
                elif column.entities[self.row - 1].type == 'T':
                    ret['drop'] = False
            else:
                ret['drop'] = False        
        return ret 


                