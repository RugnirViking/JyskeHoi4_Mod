
stack = []
focuses = []
lines = []
insertPos = 0
locFile = []
class dataObj:
    def __init__(self, name, value):
         self.name = name
         self.value = value
    def __str__(self):
        return self.name+":"+self.value
    def __repr__(self):
        if self.hasVal:
            return self.name+":"+self.value
        else:
            return self.name+":"+self.value
class wordObj:
    def __init__(self, name, value, hasVal):
         self.name = name
         self.value = value
         self.hasVal = hasVal
         self.data = []
    def __str__(self):
        return self.name
    def __repr__(self):
        if self.hasVal:
            return self.name+":"+self.value
        else:
            return self.name
    def addData(self,name,value):
        self.data.append(dataObj(name,value))
class focusObj:
    def __init__(self, focus_id, focus_localisation_name, icon_id, mutually_exclusive_focus_id, prerequisite_focus_id, reward_text, focus_x, focus_y, cost, ai_will_do_factor, focus_localisation_desc):
        self.focus_id=focus_id
        self.focus_localisation_name=focus_localisation_name
        self.icon_id = icon_id
        self.mutually_exclusive_focus_id = mutually_exclusive_focus_id
        self.prerequisite_focus_id = prerequisite_focus_id
        self.reward_text = reward_text
        self.focus_x = focus_x
        self.focus_y = focus_y
        self.cost = cost
        self.ai_will_do_factor = ai_will_do_factor
        self.focus_localisation_desc = focus_localisation_desc
def getNumeric(prompt):
    while True:
        try:
            res = int(input(prompt))
            break
        except (ValueError, NameError):
            print("Numbers only please!")
    return res
def getVars():
    focus_id = raw_input("Enter focus ID: ")
    focus_localisation_name = raw_input("Enter localisation name: ")
    focus_localisation_desc = raw_input("Enter localisation description: ")
    icon = raw_input("Enter icon ID: ")
    mutually_exclusive_focus_id = raw_input("Enter mutually exclusive focus ID: ")
    prerequisite_focus_id = raw_input("Enter prerequisite focus ID: ")
    reward_text = raw_input("Enter reward text: ")
    focus_x = getNumeric("Enter focus x position: ")
    focus_y = getNumeric("Enter focus y position: ")
    cost = getNumeric("Enter focus cost (10 is default): ")
    ai_will_do_factor = getNumeric("AI will do factor (Best leave at 1): ")
    return focusObj(focus_id,focus_localisation_name,icon,mutually_exclusive_focus_id,prerequisite_focus_id,reward_text,focus_x,focus_y,cost,ai_will_do_factor,focus_localisation_desc)
def buildFocus(vars):
    focusString = ""
    focusString+="focus = {\n"
    focusString+="\t\tid = "+vars.focus_id+"\n"
    focusString+="\t\ticon = "+vars.icon_id+"\n"
    focusString+="\t\tai_will_do = { factor = "+str(vars.ai_will_do_factor)+" }\n"
    focusString+="\t\tx = "+str(vars.focus_x)+"\n"
    focusString+="\t\ty = "+str(vars.focus_y)+"\n"

    if not vars.mutually_exclusive_focus_id == "":
        focusString+="\t\tmutually_exclusive = { focus = "+vars.mutually_exclusive_focus_id+" }\n"
    else:
        focusString+="\t\tmutually_exclusive = { }\n"

    if not vars.prerequisite_focus_id == "":
        focusString+="\t\tprerequisite = { focus = "+vars.prerequisite_focus_id+" }\n"
    else: 
        focusString+="\t\tprerequisite = { }\n"

    focusString+="\t\tcost = "+str(vars.cost)+"\n"
    focusString+="\t\tavailable_if_capitulated = yes\n"
    focusString+="\t\tcompletion_reward = { \n"
    focusString+="\t\t\t"+vars.reward_text+"\n"
    focusString+="\t\t}\n"
    focusString+="\t}\n"
    return focusString
def writeFile():
    global insertPos
    vars = getVars()
    with open("common/national_focus/jylland.txt","w") as f:
        num = 0
        for line in lines:
            #print(line)#
            num+=1
            
            if not num==insertPos-1:
                f.write(line)
            else:
                focusString = buildFocus(vars)
                f.write("\t}\n\t"+focusString)
    print("EGGS2")
    writeToLocalisation(vars.focus_id, vars.focus_localisation_name,vars.focus_localisation_desc)
def writeToLocalisation(focus_id,focus_localisation_name,focus_localisation_desc):
    with open("localisation/focus_l_english.yml","r") as f:
        for line in f:
            locFile.append(line)
    with open("localisation/focus_l_english.yml","w") as f:
        for line in locFile:
            f.write(line)
        f.write("\n")
        f.write(" "+focus_id+":0 \""+focus_localisation_name+"\"")
        f.write("\n")
        f.write(" "+focus_id+"_desc:0 \""+focus_localisation_desc+"\"")
        
def appendWord(word):
    if len(word)>0:
        wordObject = None
        if "=" in word:
            parts = word.split("=")
            if len(parts)==2:
                wordObject = wordObj(parts[0],parts[1],True)
            elif len(parts)==1:
                word = word.replace("=","")
                wordObject = wordObj(word,None,False)
            stack.append(wordObject) 

def readLine(a):
    global insertPos
    lines.append(line)
    word=""
    addedToStack = False
    for char in line:
        if char == "#":
            break
        else:
            if char == " ":
                pass
            elif char == "{":
                word = word.replace("\n","").replace("\t","")
                appendWord(word)
                word=""
                addedToStack = True
            elif char == "}":
                finalData = stack.pop()
                if finalData.name == "focus":
                    focuses.append(finalData)
                if finalData.name == "focus_tree":
                    insertPos = a
                #print(finalData)
                #for dataPoint in finalData.data:
                #    print("data: "+str(dataPoint))
            else:
                word += char
    word = word.replace("\n","").replace("\t","")
    #appendWord(word)
    if "=" in word and not addedToStack:
        #appendWord(word)
        if len(word)>0:
            wordObject = None
            if "=" in word:
                parts = word.split("=")
                if len(parts)==2:
                    stack[len(stack)-1].addData(parts[0],parts[1])
        
    #if addedToStack and len(word)>1:
        #print("a: "+str(stack)+" word: "+word+" \n\n")     
    word=""  
    
with open("common/national_focus/jylland.txt","r") as f:
    a = 0
    for line in f:
        a+=1
        strippedLine = line.strip()
        #if strippedLine.startswith("#"):
        #    continue
        readLine(a)
    xSize = 0
    ySize = 0    
    for focus in focuses:
        #print("-------  FOCUS: "+str(focus))
        for dataPoint in focus.data:
            if dataPoint.name=="x":
                if int(dataPoint.value)>xSize:
                    xSize = int(dataPoint.value)
            elif dataPoint.name=="y":
                if int(dataPoint.value)>ySize:
                    ySize = int(dataPoint.value)
            #print("data: "+str(dataPoint))
    #print("final x size: "+str(xSize))
    #print("final y size: "+str(ySize))
    gridTop = "+"
    for x in range(0,xSize+1):
        gridTop+="-"
    gridTop+="+"
    print(gridTop)
    for y in range(0,ySize+1):
        gridLine = "|"
        for x in range(0,xSize+1):
            focusFound = False
            for focus in focuses:
                xMatches = False
                yMatches = False
                for dataPoint in focus.data:
                    
                    if dataPoint.name=="x":
                        if int(dataPoint.value)==x:
                            xMatches = True
                    if dataPoint.name=="y":
                        if int(dataPoint.value)==y:
                            yMatches = True
                if xMatches and yMatches:
                    gridLine += "X"
                    focusFound = True
            if not focusFound:
                gridLine += " "
        print(gridLine+"|")
    print(gridTop)
    writeFile()