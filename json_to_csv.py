import json
import csv

f = open(r'C:\Users\tonys\OneDrive\Documents\_Work\random\run1_results.json', 'r')
jsondata = json.load(f)
 
data_file = open(r'C:\Users\tonys\OneDrive\Documents\_Work\random\jsonoutput.csv', 'w', newline='')
headers = "URL,SKU,Title,Village,Retired?,Year Released,Year Retired,Description"
data_file.write(headers)

for data in jsondata['list1']:

    line = ""
    releasedyr = ""
    retiredyr = ""
    retired = ""
    village = "No"
    sku = ""
    title = ""
    description = ""
    fieldnum = 0

    for column in data:
        if column == 'link':
            val = data[column]
            if ',' in val:
                line = "\"" + val + "\""
            else:
                line = val
        else:
            fields = data[column].split('\n')            
            title = fields[1]

            for field in fields:
                
                fieldnum += 1
                
                if fieldnum < 3:
                    continue
                
                if field == "Retired / Discontinued":
                    retired = "Yes"
                    continue
                
                if 'Year Released' in field:
                    releasedyr = field.split(': ')[1]
                    continue
                
                if 'Year Retired' in field:
                    retiredyr = field.split(': ')[1]
                    continue
                
                if 'Village' in field:
                    village = field.split(': ')[1]
                    continue

                if 'SKU#' in field:
                    sku = field.split(': ')[1]
                    continue

                description = description + '\r' + field

            if ',' in description:
                description = "\"" + description + "\""
            else:
                description = "\"" + description + "\""
            
            line = line + "," + sku + "," + title + "," + village + "," + retired + "," + releasedyr + "," + retiredyr + "," + description
            data_file.write(line)
            #print(line)
 
f.close()
data_file.close()