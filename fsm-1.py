"""
takes a log file and dumps a Pickle with key fields
main method is process
Author- @mobileraj1
"""
import cPickle as pik

def getStr(l,ty):
 if l.find(ty) > -1 :
  b=l.strip().split(':')[1]
  return b[2:b.find('",')]
 else:
  return ""

def changeState(state,l):
 if (l.find('"deviceId":') >-1):
  return ("seen_device",getStr(l,'"deviceId":'))
 elif (l.find('"model":') >-1) and (state=="seen_device"):
  return ("seen_model",getStr(l,'"model":'))
 elif (l.find('"systemVersion":')>-1) and (state=="seen_model"):
  return ("seen_sys",getStr(l,'"systemVersion":'))
 else:
  return (state,"")

def process(foo):
 gstate=""
 tp=[]
 for l in open(foo,'r'):
  gstate,str = changeState(gstate,l)
  if (gstate=="seen_device" and len(str)>1):
   a=[]
   a.append(str)
  elif (gstate=="seen_model" and len(str)>1):
   a.append(str)
  elif (gstate=="seen_sys" and len(str)>1):
   a.append(str)
   tp.append(a)
 return tp 

print process("../SystemOut.log.SOC.20140929") 
