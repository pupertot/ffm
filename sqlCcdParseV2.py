import untangle
from hl7apy.core import Message, Segment, Field, Component, SubComponent
import string
import os
#from hl7apy.parser import parse_message

def remove_html_tags(text):    
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

#with open('XXXX543-2165051.xml') as f:
#f = open('0716630-2170969.xml','r')
fileCount = 0
directory = r'Z:\Brookdale\ECW_SQL\full_sql_file_converted_april_2021_datefiltered'
#directory = r'Z:\Brookdale\ECW_SQL\asssessment_testing'
outDir = r'Z:\Brookdale\ECW_SQL\output\converted_hl7_v3'
outFile = r'\hl7_output'
logfile = r'Z:\Brookdale\ECW_SQL\output\log2.txt'
log = open(logfile, 'a')
#output = open(outDir,'a')
#br = '\\.br\\'
br = '~'
for filename in os.listdir(directory):

   filepath = directory + '\\' + filename
   fileCount += 1
   #print(str(filepath) + "  -  " + str(fileCount))
   #print(str(filepath))
   f = open(filepath, 'r')
   outPath = outDir + outFile + str(fileCount) + '.txt'
   #output = open(outPath,'a')

   try:
      turd = untangle.parse(f.read())
   except Exception as ex:
      print(ex)
      log.write(str(ex) + ' - ' + str(filepath) + '\n')

   #turd = untangle.parse(f.read())
   msg = Message()
   obxText = ''
   assessmentText = ''
   rosDetailElements = 'name,value,notes'
   examDetailElements = 'categorySubName,examNotes,examNotes2'
   build_hl7 = 0
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
         assessmentText = ''         
         for subSection in section.children:                
               #Review of Symptoms section
               obxText = ''
               if subSection._name == 'subItemsName' and subSection.cdata != 'Subjective:' and subSection.cdata != 'Objective:' and subSection.cdata != 'Assessment:':
                  break                  

               if subSection._name == 'ros':
                  #obxText = br + br + br + 'Review Of Systems'
                  for category in subSection.children:
                     for node in category.children:
                           if node._name == 'categoryName':
                              obxText = obxText + br + br + str(remove_html_tags(node.cdata))
                           else:
                              for detail in node.children:
                                 if detail._name in rosDetailElements:
                                       obxText = obxText + br + str(remove_html_tags(detail.cdata))
                  if obxText != '':
                     obxText = br + br + 'Review Of Systems' + br + obxText

               if subSection._name == 'examination':
                  #obxText = br + br + br + 'Physical Examination'
                  for category in subSection.children:
                     for node in category.children:
                           if node._name == 'categoryName':
                              obxText = obxText + br + br + str(node.cdata)
                           else:
                              for detail in node.children:
                                 for catDet in detail.children:                                        
                                    if catDet._name in examDetailElements:
                                       if catDet._name != 'categorySubName' and catDet.cdata != None:
                                          obxText = obxText + br + remove_html_tags(catDet.cdata)                  
                  if obxText != '':
                     obxText = br + br + 'Physical Examination' + br + obxText
                     build_hl7 = 1

               if subSection._name == 'assessment':
                  assessmentText = assessmentText + str(remove_html_tags(subSection.cdata)) + br
               
               if subSection._name == 'notes' or subSection._name == 'notesBR':
                  assessmentText = assessmentText + str(remove_html_tags(subSection.cdata)) + br

               if obxText != '':
                  cnt += 1
                  repNum = 0
                  repList = obxText.split('~')
                  obx = msg.add_segment('OBX')
                  obx.obx_1 = str(cnt)
                  obx.obx_2 = 'TX'
                  for rep in repList:
                     obx.obx_5[repNum] = rep
                     repNum += 1
         
         if assessmentText != '':       
            build_hl7 = 1
            assessmentText = br + br + 'Assessment' + br + br + assessmentText            
            repNum = 0
            repList = assessmentText.split('~')
            obx = msg.add_segment('OBX')
            obx.obx_1 = str(cnt)
            obx.obx_2 = 'TX'
            for rep in repList:
               obx.obx_5[repNum] = rep
               repNum += 1

   if build_hl7 == 1:
      output = open(outPath,'a')
      for seg in msg.children:      
         if seg.name == 'MSH':
            segOut = '\n' + str(seg.value) + '\r'
         else:
            segOut = str(seg.value) + '\r'
         #print(segOut)         
         output.write(segOut)
      output.close()
      
   f.close()   
log.close()

#f.close()
#output.close()
