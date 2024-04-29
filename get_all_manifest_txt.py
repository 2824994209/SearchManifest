#所有子链接
sub_link=[]
sub_link_mail=[]
from lxml import html
import re
import os
import requests
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "^cookie": "_octo=GH1.1.37633861.1683954157; _device_id=1e7a719fe59b812acaca53b727dd46ed; fs_uid=^#o-1FH3DA-na1^#5172100399509504:6252144043634688:::^#/1732107891; GHCC=Required:1-Analytics:1-SocialMedia:1-Advertising:1; MicrosoftApplicationsTelemetryDeviceId=6c1be9b9-986d-4237-a812-428ba2093af1; saved_user_sessions=130024830^%^3AqiRYa_YfW0PCvYKhr9jDGp-32Hek2RVDWItqE8-nTMAuXf4n; user_session=qiRYa_YfW0PCvYKhr9jDGp-32Hek2RVDWItqE8-nTMAuXf4n; __Host-user_session_same_site=qiRYa_YfW0PCvYKhr9jDGp-32Hek2RVDWItqE8-nTMAuXf4n; logged_in=yes; dotcom_user=2824994209; has_recent_activity=1; color_mode=^%^7B^%^22color_mode^%^22^%^3A^%^22auto^%^22^%^2C^%^22light_theme^%^22^%^3A^%^7B^%^22name^%^22^%^3A^%^22light^%^22^%^2C^%^22color_mode^%^22^%^3A^%^22light^%^22^%^7D^%^2C^%^22dark_theme^%^22^%^3A^%^7B^%^22name^%^22^%^3A^%^22dark^%^22^%^2C^%^22color_mode^%^22^%^3A^%^22dark^%^22^%^7D^%^7D; preferred_color_mode=light; tz=Asia^%^2FShanghai; _gh_sess=8xlIoY0mVYrSWTCmCPpAdxlyV^%^2BxV3BNEhR1Q0oOpUiwc1P1B8YX7BgzHzPw6N9RLgbA^%^2BeKtfN6Og9UTm8txXYlBjmYB0H930Om1NYo1p8d17LQTXOF8W^%^2F3WAbgAWlEma8cBLSdrG1kAWvhS2Rbz0r3utCKXgkygOCJwsgBHEGKtZ^%^2BJplWJ^%^2BcR0XFOBFZM^%^2B7Fo24u9YVcchUmmzh5Ayk8lcJcO8b8INsPpaCuEJq8RUaKnKYfpxF6HUJl1EreGQ4pAkDlnJHeyyORdtHmj1yTtW9EbfN^%^2FG77bqAsBl^%^2F4WDUW8WdRM9oxco6e9LP4^%^2FaMnwyG9FSOJE5^%^2B2sRk3VDjIaK18jfSemxOyzpdpTghQLbswGcf4e1Of9V7EsvNtUlLeg--OEFC3e3Gx37CxxGi--56RSPTEaIIk9POTy2cAnhQ^%^3D^%^3D^",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "^sec-ch-ua": "^\\^Chromium^^;v=^\\^124^^, ^\\^Google",
    "sec-ch-ua-mobile": "?0",
    "^sec-ch-ua-platform": "^\\^Windows^^^",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
}
proxies ={
    'http':'http://192.168.10.4:10809',
    'https':'http://192.168.10.4:10809',
}
# 请求网页
head_url = 'https://github.com/pjy612/SteamManifestCache/discussions'



def get_url(url,page_count):
    global proxies
    params = {
        "page": f"{page_count}"
    }
    response = requests.get(url, headers=headers, params=params,proxies=proxies)
    # 解析HTML文档
    tree = html.fromstring(response.content)


    xpath = '//*[@id="repo-content-pjax-container"]/div/div[3]/div[2]/ul/li//a[@data-hovercard-type="discussion"]'
    a_elements = tree.xpath(xpath)

    # 遍历并打印每个<a>标签的链接和文本
    for element in a_elements:
        link = element.get('href')
        text = element.text_content().strip()
        print(f"Text: {text}, Link: {link}")
        sub_link.append('https://github.com'+link)

def frequency(url):
    for page_count in range(1,21):
        print(f'第{page_count}次--------------------------')
        get_url(url,page_count)
    print('--------所有子链接----------')
    print(sub_link)
    with open('all_url.txt','w') as f:
        f.write(str(sub_link))



#----
def get_suburl(url):
    global headers
    global proxies
    response = requests.get(url=url,proxies=proxies)
    tree = html.fromstring(response.content)
    # 使用XPath找到第一个值（id）
    td_element = tree.xpath('//td[1]')
    if td_element:
    # 获取<td>元素中的所有文本内容
        text_content = td_element[0].xpath('.//text()')
        all_text = ' '.join(text_content)  # 将所有文本拼接成一个字符串

        # 使用正则表达式提取Steam游戏ID（假设为纯数字，出现在"Steam 游戏ID"后面）
        id_pattern = r'(Steam\s+游戏ID|appid|APPID)\s*[:：]?\s*(\d+)'
        app_id = re.search(id_pattern, all_text, re.IGNORECASE)
        id_value = app_id.group(2) if app_id else 'not found'
        
        # 使用正则表达式提取密钥列表（假设为数字;后跟十六进制字符串）
        key_pattern = r'(\d+;\w{64})'
        keys = re.findall(key_pattern, all_text)
        keys_value = ' '.join(keys) if keys else 'not found'
        
        # 提取附件链接
        link_result = td_element[0].xpath('.//p[@dir="auto"]/a/@href')
        link_value = link_result[0] if link_result else 'not found'
        # 打印结果
        print("ID:", id_value)
        print("Keys:", keys_value)
        print("Links", link_value)
        # 保存
        if id_value != 'not found' and keys_value != 'not found' and link_value != 'not found':
            # 设置文件名
            filename = f"{id_value}.txt"
            # 打开文件并写入数据
            if "https" in link_value:
                with open(f"./Manifest/{filename}", 'w', encoding='utf-8') as file:
                    file.write(f"{id_value}\n")  # 写入清理后的ID
                    file.write(f"{keys_value}\n")  # 写入格式化后的密钥列表
                    file.write(f"{link_value.strip()}\n")  # 写入链接，同时移除任何额外的空白字符
            
                print(f"Data saved to {filename}")
            elif "mailto" in link_value:
                with open('filter_mail.txt', 'a+', encoding='utf-8') as f:
                    f.write(f"{url}\n")
            else:
                return
        else:
            print("Invalid ID, cannot save the file.")
            print(url)
            with open('error_url.txt', 'a+', encoding='utf-8') as f:
                f.write(f"{url}\n")
    else:
        print("No <td> element found.")

#sub_link_mail
def mail_a():
    with open('./filter_mail.txt','r') as file:
        for line in file:
            clean_line = line.strip()
            if clean_line:  # 确保不添加空行
                sub_link_mail.append(clean_line)
                print(sub_link_mail)

def filter_mail(url):
    global headers
    global proxies
    response = requests.get(url=url,proxies=proxies)
    tree = html.fromstring(response.content)
    # 使用XPath找到第一个值（id）
    td_element = tree.xpath('//td[1]')
    if td_element:
    # 获取<td>元素中的所有文本内容
        text_content = td_element[0].xpath('.//text()')
        all_text = ' '.join(text_content)  # 将所有文本拼接成一个字符串

        # 使用正则表达式提取Steam游戏ID（假设为纯数字，出现在"Steam 游戏ID"后面）
        id_pattern = r'(Steam\s+游戏ID|appid|APPID)\s*[:：]?\s*(\d+)'
        app_id = re.search(id_pattern, all_text, re.IGNORECASE)
        id_value = app_id.group(2) if app_id else 'not found'
        
        # 使用正则表达式提取密钥列表（假设为数字;后跟十六进制字符串）
        key_pattern = r'(\d+;\w{64})'
        keys = re.findall(key_pattern, all_text)
        keys_value = ' '.join(keys) if keys else 'not found'
        
        # 提取附件链接
        link_result = td_element[0].xpath('.//a/@href')
        http_links = next((link for link in link_result if link.startswith('http')), 'not found')
        # print(http_links)]]
        # 打印结果
        print("ID:", id_value)
        print("Keys:", keys_value)
        print("Links", http_links)
        # 保存
        if id_value != 'not found' and keys_value != 'not found' and http_links != 'not found':
            # 设置文件名
            filename = f"{id_value}.txt"
            # 打开文件并写入数据
            if "https" in http_links:
                with open(f"./Manifest/{filename}", 'w', encoding='utf-8') as file:
                    file.write(f"{id_value}\n")  # 写入清理后的ID
                    file.write(f"{keys_value}\n")  # 写入格式化后的密钥列表
                    file.write(f"{http_links.strip()}\n")  # 写入链接，同时移除任何额外的空白字符
                print(f"Data saved to {filename}")
            else:
                return
        else:
            print("Invalid ID, cannot save the file.")
    else:
        print("No <td> element found.")


def main():
    if not os.path.exists("./Manifest"):
        os.makedirs("./Manifest")
    a=1
    frequency(head_url)

    for i in sub_link:
        a+=1
        get_suburl(i)
        print(f'完成第{a}个子页面')

    #---------处理页面没有获取到zip只有mail的url-------------
    # mail_a()
    # for i in sub_link_mail:
    #     filter_mail(i)
main()