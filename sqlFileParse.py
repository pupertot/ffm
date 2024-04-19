#Parses a shitty .sql file into a bunch of new files where each is a single CCD
import string
import os

directory = r'Z:\Brookdale\ECW_SQL\full_sql_file'
outPath = r'Z:\Brookdale\ECW_SQL\full_sql_file_converted_april_2021'
outFile = r'\sql_output'
fileCount = 0
for filename in os.listdir(directory):
    filepath = directory + '\\' + filename   
    f = open(filepath, 'r')
    doc = ""
    startFinder = ""
    endFinder = ""
    isReading = 0   
    while 1:       
        # read by character 
        char = f.read(1)                   
        if not char:  
            break

        if isReading == 0:  
            #finding the start of next document          
            startFinder = startFinder + str(char)
            if len(startFinder) > 8:
                #strip first char
                startFinder = startFinder[1:]
                        
            if startFinder == '<return>':
                outFile = r'\sql_output'
                doc = ""
                startFinder = ""
                isReading = 1
        
        else:
            #building document between <return></return> tags
            doc = doc + str(char)
            endFinder = endFinder + str(char)
            if len(endFinder) > 9:
                #strip first char
                endFinder = endFinder[1:]                
            if endFinder == r'</return>':
                outFile = outPath + outFile + str(fileCount) + '.txt'
                output = open(outFile,'a')
                doc = doc[:-9]
                doc = doc.replace('\\"','"')                
                isReading = 0
                output.write('<doc>' + doc + '</doc>' + '\n')
                output.close()
                endFinder = ""
                startFinder = ""
                fileCount += 1
    f.close()
print(fileCount)
