import requests, re
from bs4 import BeautifulSoup

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

# 测试代码


# 下载
'''
download_url = ''

with open('', 'wb') as f:
    f.write()
'''