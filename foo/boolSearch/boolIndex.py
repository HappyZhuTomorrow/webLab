
import json
import jieba
from zhon.hanzi import punctuation
# 对于剧情简介字段，将剧情简介视作一个文档,对其进行分词、去停用词处理,将剧情简介表征为一系列关键词集合,同时对于电影类型字
# 段，如“剧情”、“犯罪”，可直接将其加入电影表征后的关键词集

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
        
        allWords = []
        cutWords = []
        setAllWords = []
        cutWords = jieba.cut(movieIntro,cut_all=True)
        allWords.extend(cutWords)
        allWords.extend(movieType)
        setAllWords = set(allWords) #去重

        for word in setAllWords:
            if word not in invertIndex.keys():
                invertIndex[word] = []

            if word in movieIntro or word in movieType:
                invertIndex[word].append(index)
    except KeyError:
        print("这是个空的字典，豆瓣不存在这个电影")
    except Exception as ex:
        print("出现以下异常:",ex)
    
    return invertIndex
        

def delPunctuation():

    






if __name__ == '__main__':
    data = readFile('Movie.json')
    invertIndex = {}
    
    for i in range(len(data['data'])):
        print("此时的索引为:",i)
        invertIndex = makeInvertedIndex(invertIndex,data['data'][i],i)
    writeFile(invertIndex)

    # invertIndex = makeInvertedIndex(invertIndex,data['data'][0],0)
    # invertIndex = makeInvertedIndex(invertIndex,data['data'][1],1)
    # print(invertIndex)

