import requests
import re

url = []
with open('ieee_url', 'r') as file:
    url = file.read().strip().split('\n')
for urlt in url:
    headers = {"user-agent": "Mizilla/5.0"}
    response = requests.get(urlt,headers=headers)
    content = response.text
    # 打开文件
    with open('ieee_abb', 'r', encoding='utf-8') as file:
        # 读取文件内容
        abb = file.read()
    # 分割文本为单独的行
    abb = abb.strip().split('\n')

    with open('key_name', 'r', encoding='utf-8') as file:
        # 读取文件内容
        key_file = file.read()


    # print(content)

    pattern_month = r'"publicationDate":"(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)'
    pattern_year = r'"publicationDate":".*?(\d{4})'
    pattern_volume = r'"volume":"(\d+)"'
    pattern_number = r'issueNum=(\d+)'
    pattern_page = r'startPage=(\d+)&endPage=(\d+)'
    pattern_title = r'"formulaStrippedArticleTitle":"(.*?)"'
    pattern_author = r'"firstName":"(.*?)","lastName":"(.*?)"'
    pattern_pubtitle = r'"publicationTitle":"IEEE (.*?)"'

    # 使用re.search找到匹配项
    match_month = re.search(pattern_month, content)
    match_year = re.search(pattern_year, content)
    match_volume = re.search(pattern_volume, content)
    match_number = re.search(pattern_number, content)
    match_page = re.search(pattern_page, content)
    match_title = re.search(pattern_title, content)
    match_author = re.findall(pattern_author, content)
    match_pubtitle = re.search(pattern_pubtitle, content)

    if match_month:
        # 提取匹配的月份前三个字母
        month_abbr = match_month.group(1)
        # print(month_abbr)
    else:
        print("没有找到匹配的月份。")

    if match_year:
        # 提取匹配的年份
        year = match_year.group(1)
        # print(year)
    else:
        print("没有找到匹配的年份。")

    if match_volume:
        # 提取匹配的volume
        volume = match_volume.group(1)
        # print(volume)
    else:
        print("没有找到匹配的volume。")

    if match_number:
        number = match_number.group(1)
        # print(number)
    else:
        print("没有找到匹配的issueNum。")

    if match_page:
        start_page, end_page = match_page.groups()
        page = f"{start_page}--{end_page}"
        # print(page)
    else:
        result = "没有找到匹配的startPage和endPage。"

    if match_title:
        article_title = match_title.group(1)
        # print(article_title)
    else:
        print("没有找到匹配的Title内容。")

    if match_author:
        formatted_author = " and ".join([f"{last}, {first}" for first, last in match_author])
        # print(formatted_author)
    else:
        print("没有找到匹配的author内容。")

    if match_pubtitle:
        pubtitle = match_pubtitle.group(1)
        # print(pubtitle)
    else:
        print("没有找到匹配的pubtitle。")

    prefix = "IEEE"
    for line in abb:
        # 分割等号两边的全称和缩写
        full_title, abbreviation = line.split(' = ')

        # 去掉等号两边可能存在的空白字符
        full_title = full_title.strip()
        abbreviation = abbreviation.strip()

        # 去掉全称中的"{IEEE}"和缩写中的"{IEEE}"
        full_title_stripped = full_title.replace("{IEEE}", "").strip()
        abbreviation_stripped = abbreviation.replace("{IEEE}", "").strip()

        # 如果找到匹配的标题，则输出对应的缩写
        if full_title_stripped == pubtitle:
            pubtitle = prefix + " " + abbreviation_stripped
            # print(pubtitle)
            break

    # Splitting the text into individual articles
    articles = key_file.split("@article")

    # Searching for the article with the matching author list
    for article in articles:
        if formatted_author in article:
            # Extracting the key from the article
            key = article.split("{")[1].split(",")[0].strip()
            break

    publisher = "IEEE"
    bibtex_entry = (
        "@article{" + key + ",\n"
        "    title={" + article_title + "},\n"
        "    author={" + formatted_author + "},\n"
        "    journal={" + pubtitle + "},\n"
        "    volume={" + volume + "},\n"
        "    number={" + number + "},\n"
        "    pages={" + page + "},\n"
        "    year={" + year + "},\n"
        "    month={" + month_abbr + "},\n"
        "    publisher={" + publisher + "}\n"
        "}\n\n"
    )
    # print(bibtex_entry)
    file_path = 'bib'
    with open(file_path, 'a') as file:
        file.write(bibtex_entry)