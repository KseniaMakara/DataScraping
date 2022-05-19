import scrapy
from bs4 import BeautifulSoup
from projlab3.items import FacultItem, DepartmentItem, StaffItem
from requests import get


class LnamSpider(scrapy.Spider):
    name = "lnam"
    BASE_URL = "https://lnam.edu.ua/uk/faculty.html"
    BASE_URL1 = 'https://lnam.edu.ua/'
    start_urls = ["https://lnam.edu.ua/uk/faculty.html"]

    def parse(self, response):
        result = get(self.BASE_URL)
        university = BeautifulSoup(result.content, "html.parser")
        fac_list = university.find(class_='mod_article')

        for facult in fac_list.find_all(class_='faculty'):
            facult_name = facult.figure.a['original-title']
            facult_url = facult.figure.a['href']

            yield FacultItem(
                name = facult_name,
                url = facult_url
            )
            for depart in facult.find_all('li'):
                depart_url = self.BASE_URL1 + depart.a['href']
                depart_name = depart.a.getText()
                depart_res = get(depart_url)
                department_page = BeautifulSoup(depart_res.content, "html.parser")
                staff_link = self.BASE_URL1 + \
                             department_page.find('a', title="Колектив кафедри")['href']
                staff_res = get(staff_link)
                staff_page = BeautifulSoup(staff_res.content, "html.parser")
                yield DepartmentItem(
                    name = depart_name,
                    url = depart_url,
                )
                for teacher in staff_page.find_all('h4'):
                    yield StaffItem(
                        name = teacher.a.getText()
                    )