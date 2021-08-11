# _*_coding:utf-8*_
from time import sleep
import requests
from bs4 import BeautifulSoup
from re import search
from re import sub
from re import findall


def get_(url):

    res_ctl_ = requests.get(url)
    res_ctl_.encoding = "utf-8"
    return res_ctl_.text




def analyze_(main_url):
    main_url_anlysis = BeautifulSoup(main_url,"html.parser")
    list_child_href = main_url_anlysis.find("div",attrs={"class":"booklist clearfix"}).find_all("a")
    for i in list_child_href:
        sleep(1)
        child_href = i.get("href")             #得到每个章节的链接

        child_res_ = get_(child_href)           #得到每个章节的返回数据（源代码）
        child_url_anlysis = BeautifulSoup(child_res_,"html.parser")
        list_child_title = child_url_anlysis.find("div",attrs={"class":"chaptertitle clearfix"}).find("h1").get_text()
        list_child_page = child_url_anlysis.find("div",attrs={"class":"bookcontent clearfix"}).get_text()
        save_novel(str(list_child_title),str(list_child_page))

def save_novel(name,contents):
    f = open(file=r"C:\Users\szc\Desktop\xiaoshuo"+"\\"+name+".txt",mode="wt")
    f.write(contents)
    print("已经成功爬取"+":"+name)





def main():
    catalogue_url = "https://www.zanghaihua8.com/guichuideng/jingjuegucheng/"
    main_url = get_(catalogue_url)
    analyze_(main_url)



if __name__ == "__main__":
    main()