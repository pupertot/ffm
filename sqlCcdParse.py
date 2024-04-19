import untangle
from hl7apy.core import Message, Segment, Field, Component, SubComponent
import string
import os
#from hl7apy.parser import parse_message

#with open('XXXX543-2165051.xml') as f:
#f = open('0716630-2170969.xml','r')
fileCount = 0
directory = r'Z:\Brookdale\ECW_SQL\full_sql_file_converted_april_2021_datefiltered'
outDir = r'Z:\Brookdale\ECW_SQL\output\converted_hl7'
outFile = r'\hl7_output'
logfile = r'Z:\Brookdale\ECW_SQL\output\log.txt'
log = open(logfile, 'a')
#output = open(outDir,'a')
br = '\\.br\\'
for filename in os.listdir(directory):

   filepath = directory + '\\' + filename
   fileCount += 1
   #print(str(filepath) + "  -  " + str(fileCount))
   print(str(filepath))
   f = open(filepath, 'r')
   outPath = outDir + outFile + str(fileCount) + '.txt'
   output = open(outPath,'a')

   try:
      turd = untangle.parse(f.read())
   except Exception as ex:
      print(ex)
      log.write(str(ex) + ' - ' + str(filepath) + '\n\n')

   #turd = untangle.parse(f.read())
   msg = Message()
   obxText = ''
   rosDetailElements = 'name,value,notes'
   examDetailElements = 'categorySubName,examNotes,examNotes2'
   cnt = 0
   #msg.msh.msh_3 = "MSH-3"
   #msg.msh.msh_4 = "MSH-4"
   #msg.msh.msh_5 = "ECWSUX"
   #msg.msh.msh_6 = "ECWSUX"
   msg.msh.msh_9 = "MDM^T02"
   msg.msh.msh_11 = "P"
   msg.msh.msh_12 = "2.4"
   pid = msg.add_segment('PID')   
   txa = msg.add_segment('TXA')
   elementcnt = 0
   #PID-1
   pid.pid_1 = '1'

   for element in turd.children:

      #PID-3  
      pid.pid_3 = element.ControlNo.cdata.lstrip('0')
      pid.pid_3.pid_3_5 = 'KJMC'       
   
      #PID-5 
      ptName = element.patient.cdata.split(", ")        
      pid.pid_5.pid_5_1 = ptName[0]
      pid.pid_5.pid_5_2 = ptName[1]

      #TXA-1 / TXA-2
      txa.txa_1 = '1'
      txa.txa_2 = 'OPASTHPRGN'

      #TXA-4
      encounterDate = element.encDate.cdata.split(r'/')
      txa.txa_4 = str(encounterDate[2]) + str(encounterDate[0] + str(encounterDate[1]))
      
      #TXA-5
      cnt = 0
      txa.txa_5.txa_5_1 = 'E1012'
      txa.txa_5.txa_5_9 = 'BHMCSER'
      txa.txa_5.txa_5_13 = 'BHMCSER'

      #TXA-12
      txa.txa_12 = "^^" + element.reqNo.cdata

      #TXA-17 / TXA-19
      txa.txa_17 = 'AU'
      txa.txa_19 = 'AV'

      #TXA-22
      txa.txa_22.txa_22_1 = 'E1012'
      txa.txa_22.txa_22_9 = 'BHMCSER'
      txa.txa_22.txa_22_13 = 'BHMCSER'  
      txa.txa_22.txa_22_15 = str(encounterDate[2]) + str(encounterDate[0] + str(encounterDate[1])) + '0000'
      
      for section in element.children:
         for subSection in section.children:                
               #Review of Symptoms section
               obxText = ''
               if subSection._name == 'subItemsName' and subSection.cdata != 'Subjective:' and subSection.cdata != 'Objective:':
                  break    
               if subSection._name == 'ros':
                  obxText = br + br + br + 'Review Of Systems'
                  for category in subSection.children:
                     for node in category.children:
                           if node._name == 'categoryName':
                              obxText = obxText + br + br + str(node.cdata)
                           else:
                              for detail in node.children:
                                 if detail._name in rosDetailElements:
                                       obxText = obxText + br + str(detail.cdata)
                  cnt += 1
                  obx = msg.add_segment('OBX')
                  obx.obx_1 = str(cnt)
                  obx.obx_2 = 'TX'
                  obx.obx_5 = obxText
         
               if subSection._name == 'examination':
                  obxText = br + br + br + 'Physical Examination'
                  for category in subSection.children:
                     for node in category.children:
                           if node._name == 'categoryName':
                              obxText = obxText + br + br + str(node.cdata)
                           else:
                              for detail in node.children:
                                 for catDet in detail.children:                                        
                                    if catDet._name in examDetailElements:
                                       if catDet._name != 'categorySubName' and catDet.cdata != None:
                                          if str(catDet.cdata).find('FONT') == -1:
                                             obxText = obxText + br + str(catDet.cdata)
                                          else:
                                             obxText = obxText + br + str(catDet.cdata.split('>')[1].split('<')[0])
                                       else:
                                          obxText = obxText + br + str(catDet.cdata)
                  cnt += 1
                  obx = msg.add_segment('OBX')
                  obx.obx_1 = str(cnt)
                  obx.obx_2 = 'TX'
                  obx.obx_5 = obxText
   
   for seg in msg.children:      
      if seg.name == 'MSH':
         segOut = '\n' + str(seg.value) + '\r'
      else:
         segOut = str(seg.value) + '\r'
      #print(segOut)
      output.write(segOut)
   
   f.close()
   output.close()
log.close()

#f.close()
#output.close()
"""


   #OBX   
   cnt = 1
   for node in ccd.ClinicalDocument.component.structuredBody.children:
      title = node.section.title.cdata
      obx5 = ''
      if 'ENCOUNTERS' in title and node.section.text.cdata.upper() != 'NO INFORMATION':
         obxRep = 1         
         obx = msg.add_segment('OBX')
         obx.obx_1 = str(cnt)
         obx.obx_2 = 'TX'
         obx.obx_5[0] = title         
         for tblRow in node.section.text.table.tbody.children:
            index = 0
            if obxRep != 1:
               obxRep += 1
               obx.obx_5[obxRep] = ''
            for td in tblRow.children:  
               text = ''             
               header = node.section.text.table.thead.tr.children[index].cdata
               text = td.cdata
               if text != '':                  
                  combined = str(header) + ":  " + str(text)
                  obx.obx_5[obxRep] = combined
                  obxRep += 1
                  obx.obx_5[obxRep] = ''
                  obxRep += 1
               index += 1
         cnt += 1  

      if 'VITAL' in title and node.section.text.cdata.upper() != 'NO INFORMATION':
         obxRep = 1
         obx = msg.add_segment('OBX')
         obx.obx_1 = str(cnt)
         obx.obx_2 = 'TX'
         obx.obx_5[0] = title
         for tblRow in node.section.text.table.tbody.children:   
            text = ''
            obx.obx_5[obxRep] = ''
            obxRep += 1        
            for tblEntry in tblRow.children:              
               obx.obx_5[obxRep] = tblEntry.cdata
               obxRep += 1         
         cnt += 1  

      if title == 'MEDICAL (GENERAL) HISTORY' and node.section.text.cdata.upper() != 'NO INFORMATION':
         obxRep = 1         
         obx = msg.add_segment('OBX')
         obx.obx_1 = str(cnt)
         obx.obx_2 = 'TX'
         obx.obx_5[0] = title
         for tblRow in node.section.text.table.tbody.children:
            index = 0
            if obxRep != 2:
               obxRep += 1
               obx.obx_5[obxRep] = ''
            for td in tblRow.children:
               text = ''            
               header = node.section.text.table.thead.tr.children[index].cdata
               text = td.cdata
               if text != '':                  
                  combined = str(header) + ":  " + str(text)
                  obx.obx_5[obxRep] = combined
                  obxRep += 1
                  obx.obx_5[obxRep] = ''
                  obxRep += 1
               index += 1               
         cnt += 1

      if title == 'ASSESSMENTS' and node.section.text.cdata.upper() != 'NO INFORMATION':         
         obxRep = 1         
         obx = msg.add_segment('OBX')
         obx.obx_1 = str(cnt)
         obx.obx_2 = 'TX'
         obx.obx_5[0] = title
         for tblRow in node.section.text.table.tbody.children:
            index = 0
            if obxRep != 2:
               obxRep += 1
               obx.obx_5[obxRep] = ''
            for td in tblRow.children:      
               text = ''         
               header = node.section.text.table.thead.tr.children[index].cdata
               if header == 'Assessment Notes' or header == 'Treatment Notes' or header == 'Treatment Clinical Notes':
                  for paragraph in td.children:
                     text = paragraph.cdata
               else:
                  text = td.cdata
               if text != '':                  
                  combined = str(header) + ":  " + str(text)
                  obx.obx_5[obxRep] = combined
                  obxRep += 1
                  obx.obx_5[obxRep] = ''
                  obxRep += 1                  
               index += 1               
         cnt += 1      
      
      if title == 'PLAN OF TREATMENT' and node.section.text.cdata.upper() != 'NO INFORMATION':
         obxRep = 1         
         obx = msg.add_segment('OBX')
         obx.obx_1 = str(cnt)
         obx.obx_2 = 'TX'
         obx.obx_5[0] = title         
         for obj in node.section.text.children:
            if obj._name == 'content':
               obx.obx_5[obxRep] = ''
               obxRep += 1
               obx.obx_5[obxRep] = ''
               obxRep += 1
               content = str(obj.cdata) + ":"
               obx.obx_5[obxRep] = content
               obxRep += 1
            else:
               if obxRep != 2:
                  obxRep += 1
                  obx.obx_5[obxRep] = ''
               for tr in obj.tbody.children:
                  index = 0
                  for td in tr.children: 
                     text = ''
                     header = obj.thead.tr.children[index].cdata                     
                     text = td.cdata
                     if text != '':                  
                        combined = str(header) + ":  " + str(text)
                        obx.obx_5[obxRep] = combined
                        obxRep += 1
                        obx.obx_5[obxRep] = ''
                        obxRep += 1
                     index += 1               
               cnt += 1
   f.close()
   #output = open('ECW_MDM_FROM_CCD.txt','a')
   for seg in msg.children:      
      if seg.name == 'MSH':
         segOut = '\n' + str(seg.value) + '\r'
      else:
         segOut = str(seg.value) + '\r'
      output.write(segOut)
output.write('\n')
output.close()
print(filecount)
"""