import string
import os
import datetime

directory = r'Z:\Brookdale\ECW_SQL\full_sql_file_converted_april_2021_datefiltered'
fileCount = 0
threshold_date = datetime.datetime(2020, 1, 1)
bleh = 0
for filename in os.listdir(directory):
    filepath = directory + '\\' + filename   
    f = open(filepath, 'r')
    wholedoc = f.read()
    doc = ""
    startFinder = ""
    endFinder = ""
    isReading = 0 
    deleted = 0
    datefound = 0
    charIndex = 0
    if bleh == 1:
        break
    
    while 1:       
        if bleh == 1:
            break

        if deleted == 1 or datefound == 1:            
            break

        if wholedoc.find('<encDate>') == -1:            
            os.remove(filepath)            
            print('Removing (no encDate)' + str(filepath))        
            break

        # read by character
        char = wholedoc[charIndex]
        charIndex += 1                
        if not char:  
            print('not char breakpoint')
            break

        if isReading == 0:  
            #finding the start of next document          
            startFinder = startFinder + str(char)                        
            if len(startFinder) > 9:
                #strip first char
                startFinder = startFinder[1:]
                        
            if startFinder == '<encDate>':
                outFile = r'\sql_output'
                doc = ""
                startFinder = ""
                isReading = 1
        
        else:
            #building document between <return></return> tags
            doc = doc + str(char)
            endFinder = endFinder + str(char)
            if len(endFinder) > 10:
                #strip first char
                endFinder = endFinder[1:]                
            if endFinder == r'</encDate>':
                doc = doc[:-10]
                isReading = 0
                dateinfo = doc.split('/')
                docDate = datetime.datetime(int(dateinfo[2]), int(dateinfo[0]), int(dateinfo[1]))
                if docDate < threshold_date:
                    print('too old;  deleting - ' + str(filepath))
                    f.close()
                    os.remove(filepath)       
                    deleted = 1             
                else:
                    print('recent;  keeping')
                    datefound = 1
                    f.close()
                    fileCount += 1                
                
                endFinder = ""
                startFinder = ""
                fileCount += 1
    
print(fileCount)

