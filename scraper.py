import uvicorn
from fastapi import FastAPI, Response
from pydantic import BaseModel
import pandas as pd
import json
from facebook_scraper import get_posts
from sqlalchemy import create_engine

app = FastAPI()

class Body(BaseModel):
    page_name = "RealMadrid"
    number_pages= 3

@app.post('/scraper')
def scrape(body:Body):
    page_name = body.page_name # name of the scrapped facebook page.
    number_pages = body.number_pages # number of pages to scrape
    if number_pages <= 0:
        return Response(json.dumps('number of pages must be greater than 0'),media_type='application/json')
    
    data_columns = ['Name_page','Date_post','Likes','Comments','Shares'] # columns names to scrape
    data =  pd.DataFrame(columns = data_columns) # create an empty dataframe to store data.
    
    for post in get_posts(page_name, pages=number_pages):
        dict = {'Name_page':page_name,'Date_post': post['time'].strftime('%Y-%m-%d %H:%M:%S') ,
         'Text': post['text'], 'Likes': post['likes'],
         'Comments': post['comments'],'Shares': post['shares'] }
        # create a dict for each post to be added to the dataframe.
        data = data.append(dict, ignore_index = True) # add each post to the dataframe.
        
    
    table_name = "Data" # table name
    engine = create_engine('postgresql://jass:jass@host.docker.internal:5432/scraper_db') # create the postgres engine
    data.to_sql(table_name, engine, if_exists='append') # add values to postgres.    
    return Response(json.dumps('scraped page with success'),media_type='application/json')

if __name__ == '__main__':
    uvicorn.run("scraper:app", host="0.0.0.0", port=1902)