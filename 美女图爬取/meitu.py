# _*_coding:utf-8*_
from time import sleep
import requests
from bs4 import BeautifulSoup
from re import search
from re import sub
from re import findall




def main():

    url = "https://www.tupianzj.com/meinv/mm/meituwang/"
    header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                            "Chrome/86.0.4240.198 Safari/537.36"}
    url_text = Geturl(url, header)
    page_Analysis(url_text)


# 获取网页返回的源代码
def Geturl(url, header):
    req = requests.get(url, headers=header)  # 此时网页源代码已经返回给req了
    req.encoding = 'gb2312'  # 转码操作
    return req.text


# 对首页返回数据解析
def page_Analysis(url_str):
    main_page = BeautifulSoup(url_str, "html.parser")  # 用解析器解析当前url并获取为一个列表
    list_con_box = main_page.find("div", attrs={"class": "list_con_box"}).find_all("a")  # 寻找符合属性的a标签
    for x in list_con_box:
        sleep(2)
        href = "https://www.tupianzj.com/" + x.get("href")  # 拼接主网址目录
        requ = requests.get(href)  # 发送请求
        requ.encoding = 'gb2312'
        child_page = BeautifulSoup(requ.text, "html.parser")  # 子页url的解析

        child_page_Analysis(child_page, href)


# 得到每个子页信息
def child_page_Analysis(child_page, child_href):
    text = child_page.find("script", attrs={"language": "javascript"})  # 得到每个子页的页数
    text_str = str(text)
    total_page = search("totalpage=\d+", text_str).group()  # 匹配字符串
    total_page_num_str = findall("\d+", total_page)[0]

    total_page_num_ = int(total_page_num_str)
    for i in range(2, total_page_num_ + 1):
        sleep(1)
        child_url_list = list(child_href)
        child_url_list.insert(-5, "_" + str(i))  # 拼接每个子页从而得到url
        child_url = "".join(child_url_list)
        child_page_req = requests.get(child_url)
        child_page_req.encoding = "gb2312"
        child_page_soup = BeautifulSoup(child_page_req.text, "html.parser")
        child_src = child_page_soup.find("div", attrs={"id": "bigpic"}).find("img").get("src")
        save_document(child_src)


# 保存文件模块
def save_document(pic_scr):
    path = r'C:\Users\szc\Desktop\picture\\' + str(pic_scr).split('/')[-1]     #通过图片url后缀来命名图片
    f = open(file=path, mode='wb')
    f.write(requests.get(pic_scr).content)
    print("恭喜你，已经下载了1张图片")


if __name__ == "__main__":
    main()
