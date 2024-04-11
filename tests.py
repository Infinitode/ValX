import unittest
from pywebscrapr import scrape_images, scrape_text

class TestPyWebScraper(unittest.TestCase):
    def test_scrape_images(self):
        # Test scraping images using links from a file
        scrape_images(links_file='test_links.txt', save_folder='downloaded_images')

    def test_scrape_text(self):
        # Test scraping text using links directly
        links = ['https://google.com', 'https://github.com']
        scrape_text(links_array=links, output_file='output.txt', csv_output_file='csv_output.csv', remove_extra_whitespace=True)

if __name__ == '__main__':
    unittest.main()
