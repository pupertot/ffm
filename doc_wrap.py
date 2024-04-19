import string
import os
import datetime

directory = r'Z:\Brookdale\ECW_SQL\output_04172021'
outPath = r'Z:\Brookdale\ECW_SQL\output\20210419\hl7_output'
fileCount = 0

for filename in os.listdir(directory):
    fileCount += 1
    filepath = directory + '\\' + filename   
    #f = open(filepath, 'r')    

    outFile = outPath + str(fileCount) + '.txt'
    output = open(outFile,'a')

    with open(filepath,'r') as f:
        with open(outFile,'w') as f2: 
            f2.write('<doc>')
            old_text = f.read()
            new_text = old_text.replace('\\"','"')            
            f2.write(new_text)
            f2.write('</doc>')
            f.close()
            f2.close()

print(fileCount)

