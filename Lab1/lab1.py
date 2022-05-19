from bs4 import BeautifulSoup
from json import dump
import requests

BASE_URL = 'https://lnam.edu.ua/'
URL = f"{BASE_URL}uk/faculty.html"
result = requests.get(URL)
university = BeautifulSoup(result.content, "html.parser")
faculties = []
fac_list = university.find(class_='mod_article')

with open("university.txt", "w", encoding="UTF=8")as file:
    for facult in fac_list.find_all(class_='faculty'):
        facult_name = facult.figure.a['original-title']
        facult_url = facult.figure.a['href']
        file.write(f"Назва факультета: {facult_name}\n")
        file.write(f"Ссилка: {facult_url}\n")

        faculty = {
            "name": facult_name,
            "url": facult_url,
            "departments": []
        }

        for depart in facult.find_all('li'):
            depart_url = BASE_URL + depart.a['href']
            depart_name = depart.a.getText()
            depart_res = requests.get(depart_url)
            department_page = BeautifulSoup(depart_res.content, "html.parser")
            staff_link = BASE_URL + \
                department_page.find('a', title="Колектив кафедри")['href']
            staff_res = requests.get(staff_link)
            staff_page = BeautifulSoup(staff_res.content, "html.parser")
            file.write(f"Назва кафедри: {depart_name}\n")
            file.write(f"Ссилка на кафедру: {depart_url}\n")


            department = {
                "name": depart_name,
                "url": depart_url,
                "staff": []
            }
            for teacher in staff_page.find_all('h4'):
                department["staff"].append(teacher.a.getText())
                file.write(f"Ім'я викладача: {teacher.a.getText()}\n")
                
            faculty["departments"].append(department)
        faculties.append(faculty)


