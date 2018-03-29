import requests, re, configparser
from bs4 import BeautifulSoup
from urllib.parse import urlparse


config = configparser.ConfigParser()
config.read('info.ini')

headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}

user_data = {
    'IPT_LOGINUSERNAME': config['Information']['username'],
    'IPT_LOGINPASSWORD': config['Information']['password']
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
# 此处需要遍历全部树节点保证全部下载

# 测试代码

resource_page_url = ''    # 资源页
resource_page = session.get(resource_page_url).text

source_download_preview_url = 'http://learn.upc.edu.cn/meol/common/script/'
source_url = 'http://learn.upc.edu.cn'

# 代码过于耦合 待优化
download_soup = BeautifulSoup(resource_page, 'html.parser')
download_pages = download_soup.find_all(href=re.compile('preview/download_preview.jsp?'))
for download_page in download_pages:
    download_preview_page = source_download_preview_url + download_page['href']
    download_preview_html = session.get(download_preview_page).text
    download_preview_page_soup = BeautifulSoup(download_preview_html, 'html.parser')
    h2_tag = download_preview_page_soup.find('h2')
    if h2_tag.p.a == None:    # 存在无法下载的文件 跳过循环
        continue
    download_url = source_url + h2_tag.p.a['href']
    file_name = h2_tag.find('span').text
    data = session.get(download_url, headers=headers)
    with open('download/' + file_name, 'wb') as f:
        f.write(data.content)
    print('\"' + file_name + '\"' + ' 下载完成！')    # 人性化提示
