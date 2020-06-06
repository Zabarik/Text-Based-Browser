import sys
import os
import requests
import bs4
import colorama
from collections import deque


if len(sys.argv) == 2:
    dir_name = sys.argv[1]
    history = deque()

    # Create target Directory
    try:
        os.mkdir(dir_name)
        print("Directory ", dir_name, " created ")
    except FileExistsError:
        print("Directory ", dir_name, " already exists")

    # main loop
    while True:
        url = input()
        colorama.init()
        print(colorama.Style.RESET_ALL)
        if url == 'exit':
            break
        elif url == 'back':
            try:
                history.pop()
                with open(f"{dir_name}/{history[-1]}.txt", "r", encoding="utf-8") as f:
                    print(f.read())
            except IndexError:
                pass
        elif '.' not in url:
            try:
                with open(f"{dir_name}/{url}.txt", "r", encoding="utf-8") as f:
                    print(f.read())
                history.append(url)
            except FileNotFoundError:
                print("Error: Incorrect URL")
        else:
            try:
                if not url.startswith("https://"):
                    url = "https://" + url
                r = requests.get(url)
                soup = bs4.BeautifulSoup(r.text, 'html.parser')
                content = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'])
                content_text = [el.get_text() for el in content]
                for el in content:
                    if el.name == "a":
                        print(colorama.Fore.BLUE + el.get_text())
                    else:
                        print('\033[39m' + el.get_text())
                url_name = url.lstrip("https://").rsplit(".", 1)[0]
                history.append(url_name)
                with open(f"{dir_name}/{url_name}.txt", "w", encoding="utf-8") as f:
                    f.writelines(content_text)
            except KeyError:
                print("Error: Incorrect URL")
else:
    print("Add folder name")
