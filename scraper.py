# Scraping a Dynamic Webpage from UDN News
# Reference: https://blog.jiatool.com/posts/udn_spider/

# Import necessary modules:
# requests and BeautifulSoup for retrieving webpage data
# json for parsing data to json format
# pandas for compiling news data into a csv format (optional)
import requests
import json
import pandas as pd
from bs4 import BeautifulSoup

class Scraper():
    """
    A class that is used to scrape news data from UDN news.

    Attributes
    ----------
    HEADERS: dict
        Headers needed to scrape the site.
        Some sites will block scraping if headers are not included.
    SITE: str
        The name of the site.
    webpages: list
        Scraped webpage data(type dict) goes here.

    Methods
    -------
    getData(self, searchQuery, pages)
        Retrieves the data of all webpages of the search query.
        Data includes: Title, Link, Category, Time and Context.
    
    export(self, filename)
        Exports the scraped data as a csv format.
    """

    def __init__(self):
        """
        Initializes the scraper.

        Attributes
        ----------
        HEADERS: dict
            Headers needed to scrape the site.
            Some sites will block scraping if headers are not included.
        SITE: str
            The name of the site.
        webpages: list
            Scraped webpage data(type dict) goes here.
        """
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',}
        self.SITE = "https://udn.com/api/more?"
        self.webpages = []

    def getData(self, searchQuery, pages):
        """
        Retrieves the data of all webpages of the search query.
        Data includes: Title, Link, Category, Time and Context.

        Parameters
        ----------
        searchQuery: str
            The search query the scraper is going to find data from.
        pages: int
            The number of pages the scraper is going to scrape.
             (A pages contains 20 news articles)

        Returns
        -------
        self.webpages: list
            The completed list of scraped webpage data.
        """

        # In UDN News, search for a certain query
        # Then right click > Inspect > Network > Scroll down until more content is loaded
        # Click on the website that appears under name > Headers
        # You'll see that there is a request URL and Method (GET) for the website
        for page in range(pages):
            
            # Params are in Headers > "Query String Parameters"
            PARAMS = {
                "page": page,
                "id": f"search:{searchQuery}",
                "channelId": 2,
                "type": "searchword"
            }
        
            # Preview shows the json formatted webpage retrieved by the GET request
            # Here requests.get() returns a string, so another .json() is added to format string to JSON
            webpages = requests.get(self.SITE, params=PARAMS).json()    

            # Use a JSON Online Editor to view the structure of the JSON file
            # Each news article is stored separately inside webpages["lists"]
            for news in webpages["lists"]:
                title = news["title"]
                link = news["titleLink"]
                category = news["cateTitle"]
                time = news["time"]["dateTime"]

                # After obtaining title, link, category and name, format into a dict then store into the list
                self.webpages.append({"title": title, "link": link, "category": category, "time": time})

        for webpage in self.webpages:
            text = ""
            try:
                article = requests.get(webpage["link"])
                soup = BeautifulSoup(article.text, features="lxml")
                context = soup.find("section", {"itemprop": "articleBody"}).find_all("p")

                # There are multiple "p" tags in "articleBody", need to combine all of them       
                for paragraph in context:
                    text += (paragraph.text)
        
            # This works for more than 98% of all webpages.
            # In case of an error, implement a try-except for the code to continue running.
            except:
                print(f'Cannot scrape: {webpage["link"]}')

            # Add text into the dict of the webpage,
            # so that a certain webpage now contains {title, link, category, name, text}
            webpage["text"] = text
    
        # Return the modified webpages list.
        return self.webpages

    def export(self, filename):
        """
        Exports the scraped data as a csv format.

        Attributes
        ----------
        filename: str
            The name of the outputted csv file.
        """
        output = pd.DataFrame()
        output = output.append(self.webpages, ignore_index = True)
        output.to_csv(filename, encoding = "utf-8")
        print(f"News data has been exported to {filename}.csv.")