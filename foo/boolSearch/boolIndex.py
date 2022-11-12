
import json
import jieba
from zhon.hanzi import punctuation
import string
import re
# 对于剧情简介字段，将剧情简介视作一个文档,对其进行分词、去停用词处理,将剧情简介表征为一系列关键词集合,同时对于电影类型字
# 段，如“剧情”、“犯罪”，可直接将其加入电影表征后的关键词集

#加载近义词表
f = open("./lab1/docs/dict_synonym.txt",'r',encoding='utf8')
lines = f.readlines()
synonym = [line.strip().split(" ")[1:]  for line in lines ]

def readFile(fileName):
    with open('./lab1/docs/{}'.format(fileName),'r',encoding='utf8') as file:
        data = json.load(file)
    return data

def writeFile(data):
    with open('./lab1/docs/boolIndex.json','w',encoding='utf8') as file:
        json.dump(data,file,ensure_ascii=False)
    file.close()

def makeInvertedIndex(invertIndex:dict,movieData,index): #index为当前的索引
    #剧情简介   电影类型
    try:
        movieIntro = movieData['剧情简介']
        movieType = movieData['基本信息']['类型:']

        #删去符号和英文字母
        movieIntro = re.sub(r"[! ?:;$#^&*()@+\-\\|=_—…%￥！《》.,<>？。，：；’“【】、]+", "", movieIntro)
        movieIntro = re.sub(r'([^a-z]*)[a-z]([^a-z]*)', '\g<1>\g<2>', movieIntro, flags=re.I)

        allWords = []
        cutWords = []
        setAllWords = []

        cutWords = jieba.cut(movieIntro,cut_all=True) #分词
        allWords.extend(cutWords)
        allWords.extend(movieType)
        setAllWords = set(allWords) #去重

            
        for word in setAllWords:
            synonymIndex = -2
            synonymKey = ""
            for i in range(len(synonym)):
                if word in synonym[i]: ####如果在同义词中,flag为同义词索引
                    synonymIndex = i

            if(synonymIndex != -2):    
            #如果有同义词
                for key in invertIndex.keys():
                    if synonymIndex == invertIndex[key][0]:
                        #如果和某一个key是同义词
                        synonymKey = key
                if synonymKey != "":
                    #如果和某一个key是同义词
                    invertIndex[synonymKey].append(index)
                else:
                    #如果不和某一个key是同义词
                    invertIndex[word] = [synonymIndex]
                    invertIndex[word].append(index)
            else:
            #如果没有同义词

                #是否存在相同word
                flag = 0
                for key in invertIndex.keys():
                    if key == word:
                        flag = 1
                
                if flag == 1:
                    invertIndex[word][0] = -1
                    invertIndex[word].append(index)
                else:
                    invertIndex[word] = []
                    invertIndex[word].append(-1)
                    invertIndex[word].append(index)
                    
    except KeyError:
        print("这是个空的字典，豆瓣不存在这个电影")
    # except Exception as ex:
    #     print("出现以下异常:",ex)
    
    return invertIndex
        

def singleANDmore():
    data = readFile('boolIndex.json')
    result = ""
    for key in data.keys():
        # if len(data[key]) >= 40 and len(key) == 1:
        if len(key) == 1:
            result += key
    return result

def trimBoolIndex():
    data = readFile('boolIndex.json')
    dataNoPunctuation = {}
    # print(punctuation,' and ',string.punctuation)
    single = singleANDmore() #获取单个字符但出现次数>40的字符
    for key in data.keys():
        if key not in punctuation and key not in string.punctuation:  #删除标点符号
            if key not in single:
                dataNoPunctuation[key] = data[key]
            

    
    writeFile(dataNoPunctuation)
    






if __name__ == '__main__':
    data = readFile('Movie.json')
    print(data['data'][900])
    # print(data['的'])
    # trimBoolIndex()
    # f = open("./lab1/docs/dict_synonym.txt",'r',encoding='utf8')
    # lines = f.readlines()
    # synonym = [line.strip().split(" ")[1:]  for line in lines ]
    # print(synonym[0])
    # print(len(synonym))

    # data = readFile('Movie.json')
    # invertIndex = {}
    # for i in range(len(data['data'])):
    #     print("此时的索引为:",i)
    #     invertIndex = makeInvertedIndex(invertIndex,data['data'][i],i)
    # writeFile(invertIndex)
    
    
    # trimBoolIndex()
    # invertIndex = makeInvertedIndex(invertIndex,data['data'][0],0)
    # invertIndex = makeInvertedIndex(invertIndex,data['data'][1],1)
    # print(invertIndex)

