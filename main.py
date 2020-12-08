from scraper import Scraper
# from process import Preprocessor --Not implemented

if __name__ == "__main__":
    scrape = Scraper()
    scrape.getData("台積電", 2)
    scrape.export("test.csv")