import pandas as pd
from scraper import Scraper
from preprocess import Preprocessor

if __name__ == "__main__":
    COMPANY = "台積電"
    STOCK_DATA = "2330_history.csv"
    scrape = Scraper()
    data = scrape.getData(COMPANY, 500)
    scrape.export(f"{COMPANY} news.csv")

    preprocessor = Preprocessor()
    stock = preprocessor.loadStockData(STOCK_DATA)
    data = pd.read_csv(f"{COMPANY} news.csv")
    news = preprocessor.processNews(data)
    combine = preprocessor.combine(news, stock)
    combine.to_csv(f"{COMPANY}.csv", index = False)