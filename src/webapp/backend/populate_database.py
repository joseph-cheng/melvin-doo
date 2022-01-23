import os

if os.environ['HOME'] == '/home/joe':
    import mysql

    import sys
    sys.path.insert(0, "../../../")

else:
    import src.webapp.backend.mysql
from src.scraper.vote_data_parser import get_all_bills


def populate_database():
    conn = mysql._open_connection()

    for bill in get_all_bills():
        print(bill.title)
        mysql.process_vote(conn, bill)


    

    mysql._close_connection(conn)



if __name__ == "__main__":
    populate_database()
