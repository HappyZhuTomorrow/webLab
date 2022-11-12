import json

class Stack:
    def __init__(self):
        self.stackArray = []
        self.top = 0
        self.base = 0
    def push(self,elem):
        self.top += 1
        self.stackArray.append(elem)
    def pop(self):

        elem = None
        if(self.top != 0 ):
            elem = self.stackArray[-1]
            del self.stackArray[-1]
            self.top -= 1
        
        return elem

    def reverStack(self):
        self.stackArray = list(reversed(self.stackArray))


    def empty(self):
        # 1空 2不空
        #栈是否为空
        if(self.top == 0):
            return 1
        else:
            return 0

    def printStack(self):
        print(self.stackArray)
        

class CMDBoolean:

    def __init__(self,cmd:str):
        cmdSplitArray = cmd.strip().split(" ")
        # cmdSplitArray = list(reversed(cmdSplitArray))

        self.elemStack = Stack()
        self.symbolStack = Stack()

        f = open("./lab1/docs/boolIndex.json","r",encoding="utf8")
        invertIndex = json.load(f)
        
        # for i in range(len(cmdSplitArray)):

        setAll = set([i for i in range(1000)])
        i = 0
        while i < len(cmdSplitArray):
            index = cmdSplitArray[i]
            if index == 'and' or index == 'or' or index == 'AND' or index == 'OR':
                self.symbolStack.push(index)
            elif index == 'not' or index == 'NOT':
                #如果是not则直接和后面一个作not操作 not优先级最高
                i += 1
                notResultArray = list(setAll.difference(set(invertIndex[cmdSplitArray[i]][1:])))
                self.elemStack.push(notResultArray)
            else:
                self.elemStack.push(invertIndex[index][1:])

            i += 1

        self.elemStack.reverStack()
        self.symbolStack.reverStack()

        
        
        

    def cmdAnalysis(self):
        while True:
            cmd = self.symbolStack.pop()
            # if cmd == 'not' or cmd == 'NOT':
            #     elemNode = self.elemStack.pop()
            #     elemArray = set(elemNode)
            #     elemNode = list(self.setAll.difference(elemArray)) #求补集
            #     self.elemStack.push(elemNode)
            
            if cmd == 'and' or cmd == 'AND':
                elemNode1 = self.elemStack.pop()
                elemNode2 = self.elemStack.pop()
                elemArray1 = set(elemNode1)
                elemArray2 = set(elemNode2)
                elemResult = elemArray1 & elemArray2
                self.elemStack.push(list(elemResult))


            if cmd == 'or' or cmd == 'OR':
                elemNode1 = self.elemStack.pop()
                elemNode2 = self.elemStack.pop()  
                elemArray1 = set(elemNode1)
                elemArray2 = set(elemNode2)
                elemResult = elemArray1 | elemArray2
                self.elemStack.push(list(elemResult))
            
            if self.symbolStack.empty() == 1: #符号栈已经为控
                #此时elem栈的元素为最终的结果
                return self.elemStack.pop()

            
                

                







    def printCMD(self):
        self.elemStack.printStack()
        self.symbolStack.printStack()


    

if __name__ == "__main__":
    # cmd = CMDBoolean("1940 and 斧头帮 or 上行 and 人头")
    # print(cmd.cmdAnalysis())
    while True:
        cmd = input(">>>")
        if cmd == 'exit':
            break
        else:
            print(CMDBoolean(cmd).cmdAnalysis())