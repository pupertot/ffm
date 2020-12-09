def iterDict(d):
  for k,v in d.items():        
     if isinstance(v, dict):
         iterDict(v)
     else:            
         print (k,":",v)