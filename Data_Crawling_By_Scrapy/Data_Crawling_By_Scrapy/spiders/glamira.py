import csv
import os
import scrapy
import hashlib

class GlamiraImageSpider(scrapy.Spider):
    name = "glamira"
    start_urls = ["https://www.glamira.com/sitemap.xml"]
    # Set the namespace for the sitemap to extract relevant tags
    namespaces = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    # Path to the file containing the crawled image information
    log_file = 'images_info.csv'

    def __init__(self, *args, **kwargs):
        super(GlamiraImageSpider, self).__init__(*args, **kwargs)
        
        # Initialize the CSV file if it doesn't exist, and create the column headers
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Image Title', 'Image URL', 'Last Modified', 'Hash Name'])

    # Function to process data from the initial sitemap
    def parse(self, response):
        self.logger.info(f"HTTP status: {response.status}")
        sitemap_urls = response.xpath('//sitemap:sitemap/sitemap:loc/text()', namespaces=self.namespaces).getall()
        self.logger.info(f"Found {len(sitemap_urls)} sitemap URLs")

        for url in sitemap_urls:
            yield scrapy.Request(url, callback=self.parse_sitemap)

    # Function to process each sitemap to get page URLs
    def parse_sitemap(self, response):
        page_urls = response.xpath('//sitemap:url/sitemap:loc/text()', namespaces=self.namespaces).getall()
        self.logger.info(f"Found {len(page_urls)} page URLs in {response.url}")

        for url in page_urls:
            yield scrapy.Request(url, callback=self.parse_page)

    # Function to process pages and extract image URLs
    def parse_page(self, response):
        # Extract image URLs from <img> tags
        image_urls = response.css('img::attr(src)').getall()
        # Use join to convert relative paths into absolute URLs
        image_urls = [response.urljoin(url) for url in image_urls]

        self.logger.info(f"Found {len(image_urls)} images on {response.url}")
        # Send requests to the image URLs to download the images
        for url in image_urls:
            yield scrapy.Request(url, callback=self.download_image)

    # Function to handle the image download
    def download_image(self, response):
        # Create a file name by hashing the image URL to ensure it's unique
        image_title = response.url.split("/")[-1]
        image_hash = hashlib.md5(response.url.encode()).hexdigest()
        image_extension = response.url.split('.')[-1]
        image_name = f"{image_hash}.{image_extension}"

        # Path to the directory where images will be stored
        image_dir = 'downloaded_images'
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)

        image_path = os.path.join(image_dir, image_name)
        if os.path.exists(image_path):
            self.logger.info(f"Image {image_name} already exists -> Skip download.")
            return

        # Save the image to the directory
        with open(image_path, 'wb') as f:
            f.write(response.body)
        self.logger.info(f"Downloaded image: {image_name}")

        # Log the image information into the CSV file (for future querying)
        last_modified = response.headers.get('Last-Modified', b'N/A').decode('utf-8')
        self.log_image_info(image_title, response.url, last_modified, image_hash)

    # Function to log image information into the CSV file
    def log_image_info(self, image_title, image_url, last_modified, image_hash):
        # Open the CSV file and append the downloaded image information
        with open(self.log_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([image_title, image_url, last_modified, image_hash])
