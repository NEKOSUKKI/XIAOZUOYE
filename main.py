import requests
import re
import os.path
import urllib.request
import csv

def main(url, folder_name, csv_file_name,title):
    response = requests.get(url)
    response.encoding = 'utf-8'
    text = response.text
    result = re.findall('<div class="name-group">.*?</div>', text, re.DOTALL)
    result1 = re.findall('<span class="name">.*?</span>', text, re.DOTALL)
    result2 = re.findall('<span class="iden">.*?</span>', text, re.DOTALL)
    result3 = re.findall('<img src="/__local/.*?jpg" alt', text, re.DOTALL)
    names = []
    for item in result1:
        match = re.search('>([\u4e00-\u9fa5]+)<', item)
        if match:
            names.append(match.group(1))

    idens = []
    for item in result2:
        match = re.search('>([\u4e00-\u9fa5]+)<', item)
        if match:
            idens.append(match.group(1))

    titles = []
    imgs = []
    for item in result3:
        start_index = item.index('"') + 1
        end_index = item.index('"', start_index)
        img = "https://sdmda.bupt.edu.cn/" + item[start_index:end_index]
        imgs.append(img)
        titles.append(title)

    folder_path = os.path.join(os.getcwd(), folder_name)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for i, item in enumerate(imgs):
        filename = f"image{i + 1}.jpg"
        save_path = os.path.join(folder_path, filename)
        urllib.request.urlretrieve(item, save_path)

    csv_data = zip(names, idens, titles, imgs)
    csv_file = os.path.join(folder_path, csv_file_name)
    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Name', 'Department', 'Title', 'Image'])
        writer.writerows(csv_data)


main("https://sdmda.bupt.edu.cn/szdw/js.htm", "数媒院教授信息", "professors_information.csv","教授")
main("https://sdmda.bupt.edu.cn/szdw/fjs.htm", "数媒副教授信息", "associate professor_information.csv","副教授")
main("https://sdmda.bupt.edu.cn/szdw/js1.htm", "数媒院讲师信息", "lecturer_information.csv","讲师")