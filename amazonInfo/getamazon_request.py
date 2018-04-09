import requests, random, time, traceback
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from email_manager import EmailManager
from excel_file_util import write_excel_de, write_excel_uk
from get_config import get_emailFromSend, get_emailPassword, get_smtpServer, get_emailTo, get_emailCc, get_emailSubject


# retries重试次数
def getIp(retries=5):
    urlip = 'http://dynamic.goubanjia.com/dynamic/get/42db2545aa8eb940cd4f310407e1189c.html'
    s = requests.Session()
    # 设置重试次数
    s.mount('http://', HTTPAdapter(max_retries=5))
    s.mount('https://', HTTPAdapter(max_retries=5))
    try:
        response = s.get(urlip, timeout=30)
    except Exception as e:
        print(traceback.print_exc())
        if retries > 0:
            time.sleep(0.5)
            return getIp(retries=retries - 1)
        else:
            print('GET Failed')
            return ''
    ip = response.content.strip()
    ip = str(ip, encoding='utf-8')
    return ip


def check_ip():
    ipt = getIp()
    iswork = True
    proxies = {
        'http': 'http://' + ipt
    }
    url = 'https://www.baidu.com/'
    try:
        requests.get(url, proxies=proxies,
                     timeout=30)
        iswork = True
    except Exception as e:
        print('aa')
        iswork = False
        pass
    while not iswork:
        ipt = getIp()
        proxies2 = {
            'http': 'http://' + ipt
        }
        try:
            requests.get(url, proxies=proxies2,
                         timeout=30)
            iswork = True
        except Exception as e:
            print('aa')
            iswork = False
            pass
    return ipt


def request_url(url):
    agent_list = [
        "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
        "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
        "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
        "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
        "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
        "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
        "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:52.0) Gecko/20100101 Firefox/51.0']

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Upgrade-Insecure-Requests": "1",
        'User-Agent': random.choice(agent_list)
    }
    proxies = {
        "http": "http://" + check_ip()
    }
    html = requests.get(url, proxies=proxies, headers=headers)
    cc = html.content
    html_doc = str(cc, encoding='utf-8')
    return html_doc


def getInfo(url, more):
    html_doc = request_url(url)
    nextpageurl = parseHtmlInfo(html_doc, more)
    if 'More' in more:
        return 'https://www.amazon.co.uk' + nextpageurl
    else:
        return 'https://www.amazon.de' + nextpageurl


uk_anis = []
de_anis = []


def parseHtmlInfo(htmlpage, more):
    ans = []
    # 有多个的ans
    ansmore = []
    soup = BeautifulSoup(htmlpage, 'lxml')
    # 获取页数
    # pageNum = soup.find(attrs={'class': 'pagnDisabled'}).string
    # print(pageNum)
    try:
        pagnNextLink = soup.find(attrs={'id': 'pagnNextLink'}).attrs['href']
        print(pagnNextLink)
    except Exception as e:
        pagnNextLink = ""

    css_class = soup.find_all(attrs={'class': 's-item-container'})

    for cc in css_class:
        cs = cc.find(attrs={'class': 'a-row a-spacing-mini'})
        # 取得更多的
        try:
            mmtext = cc.find(attrs={'class': 'a-box-inner a-padding-mini'}).string
            print(mmtext)
            if 'More' in mmtext or 'Weitere' in mmtext:
                ansmore.append(cs.find('a').attrs['href'])
        except Exception as e:
            pass
        try:
            href = cs.find('a').attrs['href']
            # print(href)
            ans.append(href)
        except Exception as e:
            pass
    # 去掉重复的
    ans = list(set(ans))
    ansmore = list(set(ansmore))
    print(len(ans), ansmore)
    for a in ans:
        anis = a.split('/dp/')[1].split('/')[0]
        if 'More' in more:
            uk_anis.append(anis)
        else:
            de_anis.append(anis)
    print(uk_anis, de_anis)
    # 从更多的里面获取
    for am in ansmore:
        parseMore(am, more)
        time.sleep(1)
    return pagnNextLink


def parseMore(url, more):
    html_more = request_url(url)
    soup = BeautifulSoup(html_more, 'lxml')
    try:
        lis = soup.find(attrs={'id': 'variation_color_name'}).find_all('li')
    except Exception as e:
        return

    for li in lis:
        print('more', li.attrs['data-defaultasin'])
        if 'More' in more:
            uk_anis.append(li.attrs['data-defaultasin'])
        else:
            de_anis.append(li.attrs['data-defaultasin'])


def write_txt(txtname, anis):
    with open(txtname, "w") as f:
        for pp in anis:
            f.write(pp + '\n')


def send_email(server_username, server_pwd, smtp_server, msg_to, msg_cc, msg_subject, msg_content, file_name):
    mail_cfg = {
        # 邮箱登录设置，使用SMTP登录
        'server_username': server_username,
        'server_pwd': server_pwd,
        'smtp_server': smtp_server,
        # 邮件内容设置
        'msg_to': [msg_to],  # 可以在此添加收件人
        'msg_cc': msg_cc,
        'msg_subject': msg_subject,
        'msg_date': time.strftime('%Y-%m-%d %X', time.localtime()),
        'msg_content': msg_content,

        # 附件
        'attach_file': file_name
    }

    email_manager = EmailManager(**mail_cfg)

    email_manager.run()


def getinfo_sendemail():
    file_name = time.strftime('%Y-%m-%d', time.localtime(time.time())) + '-amazonInfo.xls'
    base_url = [
        'https://www.amazon.co.uk/s?marketplaceID=A1F83G8C2ARO7P&me=ANZYLS5IXG3VI&merchant=ANZYLS5IXG3VI&redirect=true',
        'https://www.amazon.de/s?marketplaceID=A1PA6795UKMFR9&me=ANZYLS5IXG3VI&merchant=ANZYLS5IXG3VI&redirect=true']
    for index, u in enumerate(base_url):
        if index == 0:
            flag = True
            while flag:
                linktext = getInfo(u, 'More')
                u = linktext
                print('=======================================' + linktext)
                if 'https://www.amazon.co.uk' == linktext:
                    flag = False
            # write_txt('amazonInfo_uk.txt', uk_anis)
            write_excel_uk(file_name, uk_anis)
        else:
            flag2 = True
            while flag2:
                linktext2 = getInfo(u, "Weitere")
                u = linktext2
                print('=======================================' + linktext2)
                if 'https://www.amazon.de' == linktext2:
                    flag2 = False
            # write_txt('amazonInfo_de.txt', de_anis)
            write_excel_de(file_name, de_anis)
    # 发送邮件
    send_email(get_emailFromSend(), get_emailPassword(), get_smtpServer(),
               get_emailTo(), get_emailCc(), get_emailSubject(),
               'amazoninfo',
               file_name)


if __name__ == '__main__':
    getinfo_sendemail()
