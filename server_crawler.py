import requests
import pandas as pd
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from threading import Thread
import socket
import pickle


class Book:
    def __init__(self, name, author, price, seller):
        self.name = name
        self.author = author
        self.price = price
        self.seller = seller

    def __str__(self):
        return f"Name : {self.name}\nAuthor : {self.author}\nPrice : {self.price}\nSeller : {self.seller}"

    def info(self):
        return [self.name, self.author, self.price, self.seller]

    def book_csv(self):
        return f"{self.name},{self.author},{self.price},{self.seller}\n"


def iranketab_crawler(url: str):
    global books
    book_store = "iranketab.ir"
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    respond = requests.get(url, headers=headers)
    if respond.status_code == 200:
        soup = BeautifulSoup(respond.content, "html.parser")
        try:
            book_name = soup.find('h1', class_="product-name").text.strip()
        except AttributeError:
            book_name = "N/A"

        try:
            book_price_str = soup.find("span", class_="price").text.strip()
            book_price = ""
            for i in book_price_str:
                if i.isdigit():
                    book_price += i
            book_price = int(book_price)
        except AttributeError:
            book_price = "N/A"

        try:
            tmp = soup.find_all("span", class_="prodoct-attribute-item")
            book_author = tmp[3].text.strip()
        except (IndexError, AttributeError):
            book_author = "N/A"

        book = Book(book_name, book_author, book_price, book_store)
        books.append(book)
    else:
        print("Failed to Crawl")


def shahreketab_crawler(url: str):
    global books
    book_store = "shahreketabonline.com"
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    respond = requests.get(url)
    if respond.status_code == 200:
        soup = BeautifulSoup(respond.content, "html.parser")
        try:
            book_name = soup.find('h1', class_='ProductTitle').text.strip()
            # book_name = book_name.encode("utf-8")
            # book_name = book_name.decode("utf-8")
            # book_name = book_name[::-1]
        except AttributeError:
            book_name = 'N/A'

        try:
            book_price_str = soup.find('div', {'class': "Price"}).text.strip()
            rial = soup.find('div', {'class': "Price"}
                             ).find('span').text.strip()
            book_price = ""
            for i in book_price_str:
                if i.isdigit():
                    book_price += i
            book_price = int(book_price)//10
        except AttributeError:
            book_price = "N/A"
        try:
            book_author = soup.find('div', class_='Details').find_all(
                'div', class_="Attribute")[2].find('div', class_='d-flex').text.strip()
            # book_author = book_author.encode("utf-8")
        except AttributeError:
            book_author = "N/A"

        book = Book(book_name, book_author, book_price, book_store)
        books.append(book)

    else:
        print("Failed to Crawl")


iranketab_books = [
    Book('قهوه ی سرد آقای نویسنده', 'روزبه معین', 190000, 'iranketab.ir'),
    Book('مارشال اروین رومل(سالار نبرد صحرا)',
         'لویی سورل', 75000, 'iranketab.ir'),
    Book('صدای راه پله می آید', 'حسین صفا', 100000, 'iranketab.ir'),
    Book('فلسفه فاشیسم', 'ماریو پالمیری', 280000, 'iranketab.ir'),
    Book('پذیرفتن', 'گروس عبدالمالکیان', 95000, 'iranketab.ir'),
    Book('سپید دندان', 'جک لندن', 135000, 'iranketab.ir'),
    Book('ضد', 'فاضل نظری', 125000, 'iranketab.ir'),
    Book('گریه های امپراتور', 'فاضل نظری', 140000, 'iranketab.ir'),
    Book('نقش 81', 'سهیلا بسکی', 85000, 'iranketab.ir'),
    Book('هدیه هومبولت', 'سال بلو', 165000, 'iranketab.ir'),
    Book('شاهد خاموش', 'کیسی واتسون', 175000, 'iranketab.ir'),
    Book('یاشماق', 'نادر ساعی ور', 170000, 'iranketab.ir'),
    Book('مرگ در ونیز', 'توماس مان', 155000, 'iranketab.ir')
]
unique_books = [
    Book("انتقال جرم", "تریبال", 400000, "SVC Book Store"),
    Book("انتقال حرارت", "هولمن", 350000, "SVC Book Store"),
    Book("اصول ترمودینامیک", "ون وایلن", 650000, "SVC Book Store"),
    Book("اصول شیمی پلیمر", "هژیر بهرامی", 325000, "SVC Book Store"),
    Book("مکانیک سیالات", "استریتر", 500000, "SVC Book Store")
]
books = []
# books.extend(iranketab_books)
books.extend(unique_books)

threads = []

raw_data = []


iranketab_urls = [
    'https://www.iranketab.ir/book/2126-mr-author-s-cold-coffee',
    'https://www.iranketab.ir/book/71854-rommel',
    'https://www.iranketab.ir/book/141089-the-philosophy-of-fascism',
    'https://www.iranketab.ir/book/11622-white-fang',
    'https://www.iranketab.ir/book/3435-accepting',
    'https://www.iranketab.ir/book/6369-collected-poems',
    'https://www.iranketab.ir/book/9260-counter',
    'https://www.iranketab.ir/book/18904-gerye-haye-emperatour',
    'https://www.iranketab.ir/book/28300-naghsh-e-81',
    'https://www.iranketab.ir/book/75-humboldt-s-gift',
    'https://www.iranketab.ir/book/20638-the-silent-witness',
    'https://www.iranketab.ir/book/39620-yashmaq',
    'https://www.iranketab.ir/book/149-death-in-venice'
]


shahreketab_urls = [
    'https://shahreketabonline.com/Products/Details/266037/%D8%A7%DA%A9%D9%86%D9%88%D9%86',
    'https://shahreketabonline.com/Products/Details/108171/%D8%B5%D8%AF%D8%A7%DB%8C-%D8%B1%D8%A7%D9%87-%D9%BE%D9%84%D9%87-%D9%85%DB%8C-%D8%A2%DB%8C%D8%AF',
    'https://shahreketabonline.com/Products/Details/300039/%D8%B6%D8%AF',
    'https://shahreketabonline.com/Products/Details/63499/%D9%85%D8%B1%DA%AF-%D8%AF%D8%B1-%D9%88%D9%86%DB%8C%D8%B2',
    'https://shahreketabonline.com/Products/Details/275323/%D9%85%D8%A7%D8%B1%D8%B4%D8%A7%D9%84-%D8%A7%D8%B1%D9%88%DB%8C%D9%86-%D8%B1%D9%88%D9%85%D9%84-%D8%B3%D8%A7%D9%84%D8%A7%D8%B1-%D9%86%D8%A8%D8%B1%D8%AF-%D8%B5%D8%AD%D8%B1%D8%A7',
    'https://shahreketabonline.com/Products/Details/265210/%D9%82%D8%A7%D9%86%D9%88%D9%86-%D8%A2%D8%B2%D8%A7%D8%AF%DB%8C-%D9%88-%D8%A7%D8%AE%D9%84%D8%A7%D9%82-%D8%AF%D8%B1%D8%A2%D9%85%D8%AF%DB%8C-%D8%A8%D9%87-%D9%81%D9%84%D8%B3%D9%81%D9%87-%D8%AD%D9%82%D9%88%D9%82-%DA%A9%DB%8C%D9%81%D8%B1%DB%8C-%D9%88-%D8%B9%D9%85%D9%88%D9%85%DB%8C',
    'https://shahreketabonline.com/Products/Details/245699/%DA%AF%D8%B1%DB%8C%D9%87-%D9%87%D8%A7%DB%8C-%D8%A7%D9%85%D9%BE%D8%B1%D8%A7%D8%AA%D9%88%D8%B1',
    'https://shahreketabonline.com/Products/Details/36469/%D8%B3%D9%BE%DB%8C%D8%AF-%D8%AF%D9%86%D8%AF%D8%A7%D9%86',
    'https://shahreketabonline.com/Products/Details/348344/%D9%81%D8%B1%D9%82%D9%87-%D8%AA%D8%B1%D8%A7%D9%85%D9%BE',
    'https://shahreketabonline.com/Products/Details/171816/%D9%82%D9%87%D9%88%D9%87-%DB%8C-%D8%B3%D8%B1%D8%AF-%D8%A2%D9%82%D8%A7%DB%8C-%D9%86%D9%88%DB%8C%D8%B3%D9%86%D8%AF%D9%87'
]


def server_program():
    global threads
    global raw_data

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 8080))
    server_socket.listen(1)

    conn, addr = server_socket.accept()
    print("Connected from:", str(addr))

    for i in shahreketab_urls:
        thread = Thread(target=shahreketab_crawler, args=(i,))
        threads.append(thread)

    # for i in iranketab_urls:
    #     thread = Thread(target=iranketab_crawler, args=(i,))
    #     threads.append(thread)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    for book in books:
        raw_data.append(book.info())

    data = pickle.dumps(raw_data)
    conn.send(data)
    conn.close()


if __name__ == '__main__':
    server_program()
