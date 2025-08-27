import requests
import re
import random
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
from lxml import etree
import time
from DownloadFunc import download_novel

# 有效期360天
cookies = {
    'novel_1588': '0%7C1756024188',
    'Hm_lvt_10be35e21d987f3914b28bd338203744': '1755680395,1755940230,1756023718,1756025521',
    'HMACCOUNT': '5CE06F2A663644B5',
    'novel_16241': '0%7C1756025493',
    'novel_94856': '0%7C1756025507',
    'novel_136799': '0%7C1756025512',
    'novel_86441': '0%7C1756025520',
    'novel_23': '0%7C1756025562',
    'novel_26420': '0%7C1756025568',
    'novel_404': '0%7C1756025697',
    'novel_8528': '0%7C1756025705',
    'novel_1041': '0%7C1756025710',
    'novel_100610': '0%7C1756025728',
    'Hm_lpvt_10be35e21d987f3914b28bd338203744': '1756025870',
    'vv': '1756025849',
    'novel_41': '0%7C1756025849',
    'qd_vt': '1756025850',
}

# 网站基础URL
basic_url = "https://www.biqugequ.org"

# 创建全局session对象，用于复用连接
session = requests.session()


def get_proxy_user_agent():
    """
    获取随机的User-Agent和代理IP配置
    返回包含请求头和代理设置的字典
    """
    user_agents = [
        # Mac
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',

        # Windows
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.54',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.63',
        # 2024.09
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.67',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36 Edg/128.0.2739.79',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.65',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.79',
        # 2024.10
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36 Edg/129.0.2792.89',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.46',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.52',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.6099.225 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.86 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.140 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.161 Safari/537.36',
        # 2024.02
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.6167.185 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.58 Safari/537.36',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.70 Safari/537.36',
    ]

    # 代理IP列表
    proxies = [
        {"http": "8.140.235.207:9001"},
        {"http": "103.85.53.62:8080"},
        {"http": "103.85.53.62:8080"},
        {"http": "8.140.235.207:9001"},
        {"http": "121.230.8.229:1080"},
        {"http": "103.158.62.186:8088"},
        {"http": "101.132.222.120:80"},
        {"http": "183.60.141.41:443"},
        {"http": "58.216.109.14:800"},
        {"http": "118.113.133.135:9999"},
        {"http": "119.3.113.150:9094"},
        {"http": "119.3.113.152:9094"},
        {"http": "39.172.97.192:8060"},
        {"http": "123.128.12.93:9055"},
        {"http": "39.105.27.30:3128"},
        {"http": "116.62.230.32:3128"},
        {"http": "60.171.194.50:9300"},
        {"http": "39.172.97.192:8060"},
        {"http": "58.216.109.14:800"},
        {"http": "119.3.113.150:9094"},
        {"http": "8.219.97.248:80"},
        {"http": "118.178.197.213:3128"},
        {"http": "111.3.102.207:30001"},
        {"http": "47.98.123.255:8035"},
        {"http": "58.242.190.79:8095"},
        {"http": "119.3.113.151:9094"},
        {"http": "58.216.109.14:800"},
        {"http": "118.178.197.213:3128"},
        {"http": "58.216.109.17:800"},
        {"http": "101.132.222.120:80"},
        {"http": "103.85.53.62:8080"},
        {"http": "110.80.140.213:443"},
        {"http": "58.216.109.17:800"},
        {"http": "61.158.175.38:9002"},
        {"http": "119.3.113.152:9094"},
        {"http": "115.190.24.138:8080"},
        {"http": "116.62.230.32:3128"},
        {"http": "116.62.230.32:3128"},
    ]

    return {
        "headers": {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "zh-CN,zh;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "priority": "u=0, i",
            "referer": "https://www.biqugequ.org",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": random.choice(user_agents)
        },
        "proxy": random.choice(proxies)
    }


def get_page_num(key):
    """
    根据关键词搜索小说，返回搜索结果页面内容
    :param key: 搜索关键词（小说名或作者名）
    :return: 搜索结果页面的HTML内容
    """
    url = 'https://www.biqugequ.org/search.html'
    data = {
        'searchtype': 'novelname',
        'searchkey': key,
    }

    config = get_proxy_user_agent()
    response = session.post(url,
                            data=data,
                            cookies=cookies,
                            headers=config["headers"],
                            proxies=config["proxy"],
                            timeout=10)
    return response.text


def get_content_list(page_content):
    """
    解析搜索结果页面，提取小说列表信息
    :param page_content: 搜索结果页面的HTML内容
    :return: 包含小说标题和URL的字典列表
    """
    page = etree.HTML(page_content)
    li_list = page.xpath('//div[@id="newscontent"]/div[@class="l"]/ul/li')
    list_information = []
    for li in li_list:
        title = li.xpath('./span[1]/a/@title')[0]
        url = basic_url + li.xpath('./span[1]/a/@href')[0]
        novel_map = {title: url}
        list_information.append(novel_map)
    return list_information


def fetch_single_novel(novel_map):
    """
    获取单本小说的详细信息
    :param novel_map: 包含小说标题和URL的字典
    :return: 包含小说详细信息的字典
    """
    try:
        config = get_proxy_user_agent()
        title = list(novel_map.keys())[0]
        url = novel_map[title]

        novel_page = session.get(url, headers=config["headers"], proxies=config["proxy"], timeout=10)
        content_page = etree.HTML(novel_page.text)

        writer = content_page.xpath('//*[@id="info"]/p[1]/a/text()')[0]  # 作者
        sort = content_page.xpath('//*[@id="info"]/p[2]/a/text()')[0]  # 类别
        characters = content_page.xpath('//*[@id="info"]/p[3]/text()')[0]  # 角色
        character = re.search(r'色：(.*)', characters, re.S)
        if character:
            character = character.group(1)
        else:
            character = ""

        info = content_page.xpath('//div[@id="intro"]/text()')[0]  # 简介
        chapters_list = content_page.xpath('//*[@id="list"]/dl/dd')
        chapters = []

        for chapter in range(min(10, len(chapters_list))):  # 防止章节数不足
            chapter_name = chapters_list[chapter].xpath('./a/text()')[0]
            chapter_url = basic_url + chapters_list[chapter].xpath('./a/@href')[0]
            chapter_info = {
                "chapter_name": chapter_name,
                "chapter_url": chapter_url
            }
            chapters.append(chapter_info)

        novel_info = {
            "title": title,
            "url": url,
            "writer": writer,
            "sort": sort,
            "characters": character,
            "info": info,
            "chapters": chapters
        }
        return novel_info
    except Exception as e:
        # 出错时返回基本信息
        title = list(novel_map.keys())[0]
        url = novel_map[title]
        return {
            "title": title,
            "url": url,
            "writer": "获取失败",
            "sort": "获取失败",
            "characters": "",
            "info": "获取失败",
            "chapters": [],
            "error": str(e)
        }


def get_novel_information(list_information):
    """
    使用并发方式获取所有小说信息，但保持原始顺序
    :param list_information: 小说URL列表
    :return: 按原始顺序排列的小说信息列表
    """
    # 初始化固定长度的列表以保持顺序
    novels = [None] * len(list_information)

    # 使用线程池并发获取小说信息
    with ThreadPoolExecutor(max_workers=10) as executor:
        # 提交所有任务，并保存future和索引的映射
        future_to_index = {
            executor.submit(fetch_single_novel, list_information[i]): i
            for i in range(len(list_information))
        }

        # 使用tqdm显示进度
        with tqdm(total=len(list_information), desc="获取小说信息", unit="本") as pbar:
            # 处理完成的任务
            for future in as_completed(future_to_index):
                index = future_to_index[future]
                novel_info = future.result()
                novels[index] = novel_info  # 按原始顺序放置结果
                # 显示当前处理的小说名称
                pbar.set_postfix({"当前小说": novel_info["title"][:15] + "..." if len(novel_info["title"]) > 15 else
                novel_info["title"]})
                pbar.update(1)

    return novels


def display_novels(novels):
    """
    显示小说列表供用户选择
    :param novels: 小说信息列表
    """
    print("\n找到以下小说:")
    print("-" * 80)
    for i, novel in enumerate(novels, 1):
        print(f"{i}. {novel['title']}")
        print(f"   作者: {novel['writer']}")
        print(f"   分类: {novel['sort']}")
        print("-" * 80)


def get_user_choice(novels):
    """
    获取用户选择的小说序号
    :param novels: 小说列表
    :return: 用户选择的小说信息或None（如果用户选择退出）
    """
    while True:
        try:
            choice = input(f"\n请选择小说序号 (1-{len(novels)})，或输入 'q' 退出: ").strip()
            if choice.lower() == 'q':
                return None
            choice = int(choice)
            if 1 <= choice <= len(novels):
                return novels[choice - 1]
            else:
                print(f"请输入有效的序号 (1-{len(novels)})")
        except ValueError:
            print("请输入有效的数字")


def display_novel_details(novel):
    """
    显示小说详细信息
    :param novel: 小说信息字典
    """
    print("\n" + "=" * 80)
    print("小说详细信息:")
    print("=" * 80)
    print(f"书名: {novel['title']}")
    print(f"作者: {novel['writer']}")
    print(f"分类: {novel['sort']}")
    print(f"角色: {novel['characters']}")
    print(f"简介: {novel['info']}")
    print("\n相关章节:")
    for i, chapter in enumerate(novel['chapters'], 1):
        print(f"  {i}. {chapter['chapter_name']}")
    print("=" * 80)


def ask_download_novel(novel):
    """
    询问用户是否要下载选中的小说
    :param novel: 小说信息字典
    :return: True表示用户选择下载，False表示用户取消下载
    """
    while True:
        choice = input(f"\n是否要下载小说《{novel['title']}》? (y/n): ").strip().lower()
        if choice in ['y', 'yes', '是']:
            print(f"\n开始下载小说《{novel['title']}》...")
            # 调用下载函数
            result = download_novel(novel['url'], novel['title'])
            if result:
                print(f"小说《{novel['title']}》下载完成！")
            else:
                print(f"小说《{novel['title']}》下载失败！")
            return True
        elif choice in ['n', 'no', '否']:
            return False
        else:
            print("请输入 y(是) 或 n(否)")


def show_other_novels(novels, current_novel):
    """
    显示其他搜索到的小说信息
    :param novels: 所有已搜索的小说列表
    :param current_novel: 当前查看的小说
    :return: True表示成功显示其他小说，False表示返回上一级
    """
    # 过滤掉当前正在查看的小说
    other_novels = [novel for novel in novels if novel != current_novel]
    if not other_novels:
        print("没有其他小说可查看")
        return False

    print("\n其他搜索到的小说:")
    print("-" * 80)
    for i, novel in enumerate(other_novels, 1):
        print(f"{i}. {novel['title']}")
        print(f"   作者: {novel['writer']}")
        print(f"   分类: {novel['sort']}")
        print("-" * 80)

    while True:
        choice = input(f"\n请选择查看的小说序号 (1-{len(other_novels)})，或输入 'b' 返回: ").strip()
        if choice.lower() == 'b':
            return False
        try:
            choice = int(choice)
            if 1 <= choice <= len(other_novels):
                display_novel_details(other_novels[choice - 1])
                return True
            else:
                print(f"请输入有效的序号 (1-{len(other_novels)})")
        except ValueError:
            print("请输入有效的数字")


def search_novel(searched_novels=None):
    """
    搜索小说的主函数
    :param searched_novels: 已搜索的小说列表（用于累积历史记录）
    :return: True表示程序正常结束，False表示搜索失败
    """
    # 如果没有传入已搜索小说列表，则初始化为空列表
    if searched_novels is None:
        searched_novels = []

    key = input("请输入小说名或者作者名：")
    print("正在搜索小说...")
    page_content = get_page_num(str(key))

    print("正在获取小说列表...")
    novel_list = get_content_list(page_content)
    if not novel_list:
        print("未找到相关小说")
        return False

    print(f"找到 {len(novel_list)} 本相关小说")

    print("正在获取小说详细信息...")
    novels = get_novel_information(novel_list)

    # 将新搜索的小说添加到已搜索列表中
    searched_novels.extend(novels)

    # 显示小说列表供用户选择
    display_novels(novels)

    # 获取用户选择
    selected_novel = get_user_choice(novels)

    if selected_novel:
        # 显示选中小说的详细信息
        display_novel_details(selected_novel)

        # 询问是否下载
        if ask_download_novel(selected_novel):
            return True
        else:
            # 用户选择不下载，提供其他选项
            while True:
                print("\n请选择操作:")
                print("1. 查看其他搜索过的小说")
                print("2. 搜索新的小说")
                print("3. 退出程序")

                choice = input("请输入选项 (1/2/3): ").strip()
                if choice == '1':
                    # 查看其他搜索过的小说
                    if show_other_novels(searched_novels, selected_novel):
                        continue  # 显示完后继续循环
                    else:
                        break  # 返回上一级菜单
                elif choice == '2':
                    # 搜索新的小说
                    return search_novel(searched_novels)  # 递归调用继续搜索
                elif choice == '3':
                    # 退出程序
                    print("已退出程序")
                    return True
                else:
                    print("请输入有效的选项 (1/2/3)")
    else:
        print("已退出程序")
        return True


if __name__ == '__main__':
    # 程序入口点
    search_novel()
