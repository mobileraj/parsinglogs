import cPickle as pik

def getStr(l,ty):
 if l.find(ty) > -1 :
  b=l.strip().split(':')[1]
  return b[2:b.find('",')]
 else:
  return ""

def changeState2(fsm,curState,l):
 startState = fsm['startState']
 trans = fsm['transitions']
 val = (curState,"")
 for key in trans.keys(): 
  #print key,curState
  if (l.find(key) >-1) and (curState in trans[key]['prevStates']):
    val=(trans[key]['state'],getStr(l,key))
 return val 


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
 #fsm={'startState':'seen_device','triggers':('"deviceId":','"model":','"systemVersion":'),'states':('seen_device','seen_model','seen_sys'),'transitions':({'initState':"",'trigger':'"deviceId":','finalState':'seen_device'},{'initState':'seen_device','trigger':'"model":','finalState':'seen_model'},{'initState':'seen_model','trigger':'"systemVersion":','finalState':'seen_sys'})}

 transitions={'"deviceId":':{'prevStates':("","seen_sys"),'state':"seen_device"},'"model":':{'prevStates':("seen_device"),'state':"seen_model"},'"systemVersion":':{'prevStates':("seen_model"),"state":"seen_sys"}}
 states = ("seen_device","seen_sys","seen_model")
 fsm={'startState':"seen_device","transitions":transitions,'endState':"seen_sys"}
 gstate=""
 tp=[]
 for l in open(foo,'r'):
  gstate,str = changeState2(fsm,gstate,l)
  if (gstate==fsm['startState']) and (len(str)>1):
   a=[]
   a.append(str)
  elif (gstate in states) and (len(str)>1):
   a.append(str)
  elif (gstate==fsm['endState']):
   if len(a) > 1: 
    tp.append(a)
   a=[]
 return tp 

print process("testdata")

