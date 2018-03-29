import requests, re
from bs4 import BeautifulSoup
from urllib.parse import urlparse

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

user_data = {
    'IPT_LOGINUSERNAME': '1505040309',
    'IPT_LOGINPASSWORD': '040034'
}


session = requests.session()
login_url = 'http://learn.upc.edu.cn/meol/loginCheck.do'
response = session.post(login_url, data=user_data, headers=headers)

list_url = 'http://learn.upc.edu.cn/meol/lesson/blen.student.lesson.list.jsp'
h = session.get(list_url)
html = h.text

courseIds = []
soup = BeautifulSoup(html, 'html.parser')
aes = soup.find_all(href=re.compile('init_course.jsp?'))
for a in aes:
    courseId = re.findall('\d+', str(a['href']))[0]    # 提取数字
    courseIds.append(courseId)

url = 'http://learn.upc.edu.cn/meol/common/script/listview.jsp?'
params = {
    'groupid': '4',
    'lid': courseIds[0],
    'folderid': '0'
}

rr = session.get(url, params=params).text
# 此处需要遍历树节点保证全部下载

# 测试代码

basic_url = 'http://learn.upc.edu.cn/meol/common/script/listview.jsp?acttype=enter&folderid=179548&lid=18700'
download_urls = []
ht = session.get(basic_url).text
source_download_url = 'http://learn.upc.edu.cn/meol/common/script/download.jsp?'

download_soup = BeautifulSoup(ht, 'html.parser')
download_pages = download_soup.find_all(href=re.compile('preview/download_preview.jsp?'))
for download_page in download_pages:
    nurl = download_page['href']
    file_name = download_page.text
    param = urlparse(nurl).query
    download_url = source_download_url + param
    data = session.get(download_url, headers=headers)
    with open(file_name, 'wb') as f:
        f.write(data.content)
