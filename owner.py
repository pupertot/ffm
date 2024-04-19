from utils import json_parsing

class Owner(object):    
    def __init__(self, data):
        self.first_name = json_parsing(data, 'firstName')    
        self.last_name = json_parsing(data, 'lastName')
        self.full_name = self.first_name + " " + self.last_name        
        self.ownerId = json_parsing(data, 'id')
        self.userName = json_parsing(data,'displayName')        

    def __repr__(self):
        return {'first_name':self.first_name, 'last_name':self.last_name, 'full_name':self.full_name, 'ownerId':self.ownerId, 'displayName':self.userName}
    
    def __str__(self):
        return 'Owner( Name = ' + self.full_name + ', ID = ' + self.ownerId + ', Display Name = ' + self.userName + ' )'