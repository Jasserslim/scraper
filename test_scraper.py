from fastapi.testclient import TestClient
import psycopg2
from scraper import app

client = TestClient(app)


def test_scrape():
    response = client.post(
        "/scraper",
        json={"page_name":"RealMadrid","number_pages":3},
    )
    assert response.status_code == 200
    assert type(response.json()) == str
    assert response.json() == "scraped page with success"

def test_query():
    connection = psycopg2.connect(user="jass",
                                password="jass",
                                host="localhost",
                                port="5432",
                                database="scraper_db")
    cursor = connection.cursor()
    postgreSQL_select_Query = 'SELECT * FROM public."Data"'
    cursor.execute(postgreSQL_select_Query)
    Data = cursor.fetchall()
    assert(type(Data)==list)
    assert(type(Data[0])==tuple)
    assert(Data[0][1]=='RealMadrid')

