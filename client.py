import pickle
import socket
import copy
import pandas as pd
import matplotlib.pyplot as plt


def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8080))

    received_data = client_socket.recv(2048)
    received_books = pickle.loads(received_data)

    # print("Received books:", received_books)

    received_books_copy = copy.deepcopy(received_books)

    while True:

        def Book_Cost():
            for book in received_books_copy:
                book[2] = int(book[2] * 0.6)
            Marketing_Calculator()
            Minimum_Profit()
            Final_Price_Calculator()
            Shipping_Price_Add()
            Competetive_Range()

        def Marketing_Calculator():
            for book in received_books_copy:
                Marketing_cost = (book[2]//100)*5
                book.append(Marketing_cost)

        def Minimum_Profit():
            for book in received_books_copy:
                Minimum_Profit = (book[2]//100)*15
                book.append(Minimum_Profit)

        def Final_Price_Calculator():
            for book in received_books_copy:
                Final_Price = book[2]+book[5]+book[4]
                book.append(Final_Price)

        def Shipping_Price_Add():
            for book in received_books_copy:
                book[-1] = book[-1]+35000

        def Competetive_Range():
            for o_book in received_books:
                for book in received_books_copy:
                    if o_book[0] == book[0] and o_book[3] == book[3]:
                        book.append((book[-1], o_book[2]))
                        if o_book[2] >= book[-2]:
                            book.append("YES")
                        else:
                            book.append("NO")

        def plot_data():
            plt.figure(figsize=(6, 8))
            plt.bar(ndf.iloc[:, 0], ndf.iloc[:, 6])
            plt.title('price of products')
            plt.xlabel('product')
            plt.ylabel('price')
            plt.xticks(rotation=90)
            plt.savefig('price_chart.png')

            plt.figure(figsize=(6, 8))
            plt.bar(ndf.iloc[:, 0], ndf.iloc[:, 5])
            plt.title('Product profit')
            plt.xlabel('product')
            plt.ylabel('profit')
            plt.xticks(rotation=90)
            plt.savefig('profit_chart.png')

            plt.figure(figsize=(6, 8))
            ndf['param1'] = ndf['price range(minimum price, competitor price)'].apply(
                lambda x: x[0])
            ndf['param2'] = ndf['price range(minimum price, competitor price)'].apply(
                lambda x: x[1])
            ndf['difference'] = ndf['param2'] - ndf['param1']
            plt.bar(ndf.iloc[:, 0], ndf['difference'])
            plt.title('Price difference with competitors')
            plt.xlabel('product')
            plt.ylabel('price difference')
            plt.xticks(rotation=90)
            plt.savefig('price_diff_chart.png')

        x_in = input(
            "To generate an excel dataset press 1\nTo generate analysis charts press 2\nTo exit the program press 0")
        if x_in == "1":
            Book_Cost()
            df = pd.DataFrame(received_books_copy, columns=[
                "name", "author", "provider price", "competitor name", "marketing cost", "minimum profit", "minimum price", "price range(minimum price, competitor price)", "can we compete?"])
            df.to_excel("dataset.xlsx", index=False)
            ndf = df.groupby("name").max().reset_index()

        elif x_in == "2":
            plot_data()

        elif x_in == "0":
            break
        else:
            print("Wrong input")

    client_socket.close()


if __name__ == '__main__':
    client_program()
