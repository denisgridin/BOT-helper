from transliterate import translit, get_available_language_codes
from bs4 import BeautifulSoup
import requests

def check_person(text):
    def person(text):
        try:
            text = text.split(' ')
            parse_text = text[1][:1].lower() + text[1][-1:].lower() + text[0].lower()
            parse_text = translit(parse_text, reversed=True)
            url = 'https://sfedu.ru/person/' + parse_text
            return url, parse_text
        except:
            print('Ошибка! Пожалуйста, введите данные в формате << Фамилия И.О >>')
            url = ''
            parse_text = ''
            return url, parse_text
    def parse_info():
        url, parse_text = person(text)
        if url != '' and parse_text != '':
            request = requests.get(url).text
            html = BeautifulSoup(request, "html.parser")
            #print(html2text.HTML2Text().handle(request))
            try:
                name = html.select('.about_employee h2')[0].getText()
                attachment = 'https://sfedu.ru' + html.select('.about_employee img')[0]['src']
                print(attachment)
                phones =  html.select('.about_employee .card .text .phones')[0].getText()
                structure = html.select('.about_employee .card .text p a')[0].getText()
                address =  html.select('.about_employee .card .text .address p')[0].getText()
                contacts =  'Email: ' + parse_text + '@sfedu.ru'
                personal_page = 'Персональная страница: ' + 'https://sfedu.ru/person/' +  parse_text

            # subjects = 'Преподаваемые дисциплины: \n' + html.select('.about_employee .dis_list')[0].getText()
                message = name + "\n" + phones + '\n' + structure + '\n' + address + '\n' + contacts + '\n' + personal_page
                return message, attachment
            except:
                message = 'Ошибка! Не удалось получить информацию о преподавателе'
                attachment = ''
                return message, attachment
    message, attachment = parse_info()
    #print(message, attachment)
    return message, attachment