# Represents a collection of Worlds

from World import World
from Column import Column
from Entity import Entity
import time
import random

class Universe(object):    
    def __init__(self):
        self.worlds = {}        

    # Creates a world and assigns an ID.  The ID of the world is returned to the caller
    def add_world(self, initialState):
        timeVal = int(time.time())
        randomVal = random.randint(1,1000000)
        worldId = str(timeVal) + str(randomVal)
        self.worlds[worldId] = World(worldId, initialState)
        return worldId
    
    # Returns a textual representation of the world associated with the provided world ID
    # The 'state' parameter can be 'end' to show the end state of the given world or 'start' (or anything but 'end') to show the initial state.  The default is 'end'.
    # The 'strFormat' parameter determines the format of the textual string that is returned.   Options:
    #   'html' - Rows are separated by '<br>'
    #   'url' - Rows are separated by '%0A' and spaces are represented by '%20'
    #   'raw' - The end/initial state is returned as-is, which is a comma delimited list of '.', ':', ' ', and/or 'T' characters.
    #   'newline' - Rows are separated by '\n'
    def show_world(self, worldId, state, strFormat):                
        if state == None:
            state = 'end'
        if strFormat == None:
            strFormat = 'raw'
        return self.worlds[worldId].__format__(state, strFormat)
    
    
