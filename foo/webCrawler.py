import requests
import time

urlMovie = 'https://movie.douban.com/subject/{}/'
urlBook = 'https://book.douban.com/subject/{}/'

def getMovieURL():
    # with open('1.txt','r') as movieFile:
    #     print(movieFile.readline())
    file = open('1.txt','r',encoding='utf-8')
    print(file.readline())
    file.close()
def getBookURL():
    pass



if __name__ == '__main__':
    getMovieURL()