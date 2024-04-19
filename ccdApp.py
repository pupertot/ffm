import untangle
from hl7apy.core import Message, Segment, Field, Component, SubComponent
import string
import os
#from hl7apy.parser import parse_message

#with open('XXXX543-2165051.xml') as f:
#f = open('0716630-2170969.xml','r')
filecount = 0
directory = r'Z:\Brookdale\ECW_CCD\testing'
output = open('ECW_MDM_FROM_CCD_20210126.txt','a')
for filename in os.listdir(directory):
   filepath = directory + '\\' + filename
   filecount += 1
   print(str(filepath) + "  -  " + str(filecount))
   f = open(filepath, 'r')
   ccd = untangle.parse(f.read())
   msg = Message()

   cnt = 0
   #msg.msh.msh_3 = "MSH-3"
   #msg.msh.msh_4 = "MSH-4"
   #msg.msh.msh_5 = "ECWSUX"
   #msg.msh.msh_6 = "ECWSUX"
   msg.msh.msh_9 = "MDM^T02"
   msg.msh.msh_11 = "P"
   msg.msh.msh_12 = "2.4"
   pid = msg.add_segment('PID')
   pid.pid_1 = "1"
   txa = msg.add_segment('TXA')

   #PID-1
   pid.pid_1 = '1'

   #PID-3
   for node in ccd.ClinicalDocument.recordTarget.patientRole.id:      
      if node['root'] == '2.16.840.1.113883.4.391.3595.1':
         pid.pid_3 = node['extension'].lstrip('0')
         pid.pid_3.pid_3_5 = 'KJMC'

   #PID-5 
   for node in ccd.ClinicalDocument.recordTarget.patientRole.patient.name.children:
      if cnt == 0:
         pid.pid_5.pid_5_1 = node.cdata
      if cnt == 1:
         pid.pid_5.pid_5_2 = node.cdata      
      cnt += 1

   #TXA-1 / TXA-2
   txa.txa_1 = '1'
   txa.txa_2 = 'OPASTHPRGN'

   #TXA-4
   dt = ccd.ClinicalDocument.effectiveTime['value']
   if '+' in dt:
      dt = dt[:-5]
   txa.txa_4 = dt

   #TXA-5
   cnt = 0
   txa.txa_5.txa_5_1 = 'E1012'
   txa.txa_5.txa_5_9 = 'BHMCSER'
   txa.txa_5.txa_5_13 = 'BHMCSER'

   #TXA-12
   txa.txa_12 = "^^" + str(ccd.ClinicalDocument.id['extension']) 

   #TXA-17 / TXA-19
   txa.txa_17 = 'AU'
   txa.txa_19 = 'AV'

   #TXA-22
   txa.txa_22.txa_22_1 = 'E1012'
   txa.txa_22.txa_22_9 = 'BHMCSER'
   txa.txa_22.txa_22_13 = 'BHMCSER'  
   txa.txa_22.txa_22_15 = dt

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