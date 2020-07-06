import sys
import os
from collections import deque
import requests
from bs4 import BeautifulSoup
from colorama import init, Fore

init()


def remove_extention(str_):
    str_arr = str_.split('.')
    return '.'.join(str_arr[:-1])


def request_webpage(url):
    correct_url = 'https://'+url
    response = requests.get(correct_url)
    if response.status_code == 200:
        return response.content


def parse_a_page(url_response_text):
    soup = BeautifulSoup(url_response_text, 'html.parser')
    to_display = soup.find_all(['a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'ul', 'ol', 'li'])
    a_tag = soup.find_all('a')

    for el in a_tag:
        el.string = Fore.BLUE + el.get_text() + Fore.RESET

    to_display = '\n'.join([x.get_text() for x in to_display])

    return to_display


args = sys.argv
websites = dict()
web_history = deque()

if len(args) != 2:
    print('One argument needed')
else:
    dir_name = args[1]

    if not os.path.exists(dir_name):
        os.mkdir(dir_name)

    while True:
        user_input = input()

        if user_input == 'exit':
            break

        elif user_input == 'back':
            if len(web_history) >= 1:
                web_history.pop()
                curr_website = web_history.pop()
                web = remove_extention(curr_website)
                file = open('{}/{}.txt'.format(dir_name, web), 'r')
                print(file.read())
                file.close()

        elif user_input not in websites.keys() and user_input not in websites.values():
            if '.' in user_input:
                user_input_arr = user_input.split('.')
                websites[user_input] = '.'.join(user_input_arr[: -1])
                page_to_open = request_webpage(user_input)
                if page_to_open is not None:
                    with open('{}/{}.txt'.format(dir_name, websites[user_input]), 'w', encoding="utf-8") as file:
                        view_page = parse_a_page(page_to_open)
                        web_history.append(user_input)
                        file.write(view_page)
                        print(view_page)

                else:
                    print('Error: Incorrect URL')

            else:
                print('Error: Incorrect URL')

        elif user_input in websites.values():
            web_history.append(user_input)
            file = open('{}/{}.txt'.format(dir_name, user_input), 'r', encoding="utf-8")
            print(file.read())
            file.close()

