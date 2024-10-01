# Glamira Image Crawler

This project is a Scrapy-based web crawler designed to download all images from the sitemap of [glamira.com](https://www.glamira.com/sitemap.xml) and store the image information, including Image Title, Image URL, Last Modified date, and a unique Hash Name for each image. The crawler uses concurrency settings optimized for performance to handle large-scale crawling efficiently.

## Features

- Crawls images from `https://www.glamira.com/sitemap.xml` and all linked pages.
- Stores image information in a CSV file (`images_info.csv`) for future retrieval.
- Downloads images to a specified directory (`downloaded_images`) with unique names using MD5 hashing.
- Handles concurrency to increase the crawling speed.

## Performance

- **Concurrent Requests**: Set to 32 (increased from the default 16), allowing Scrapy to process 32 requests simultaneously.
- **Concurrent Requests per Domain**: Set to 16, enabling more parallel requests to the same domain to speed up image downloading.
- **Crawling Performance**: In a test run of 1 hour and 20 minutes, the spider successfully crawled 25,612 images, averaging 5.34 images per second.

## Usage

### Prerequisites

- Python 3.9.19
- Scrapy
- csvkit (if you plan to analyze or manipulate the CSV output)

### Setup

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/glamira-image-crawler.git
   cd glamira-image-crawler
   ```

2. **Install dependencies:**

   You can use pip to install Scrapy and other necessary packages:

   ```bash
   pip install scrapy
   ```

3. **Run the spider:**

   To start crawling the images, use the following command:

   ```bash
   scrapy crawl glamira
   ```

4. **Check the results:**

   - Downloaded images will be stored in the `downloaded_images` directory.
   - Image information will be saved in the `images_info.csv` file with the following fields:
     - Image Title
     - Image URL
     - Last Modified
     - Hash Name

### Improving Performance

Feel free to explore ways to further optimize the crawler. Some ideas for improvement include:

- Implementing better error handling or retries for failed requests.
- Modifying the crawling process to selectively crawl specific image categories or pages.
- Find a way to retrieve more information, such as product attributes, and store them in a CSV file.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request if you have any improvements or suggestions.

---

**Note:** During development, ensure that your changes in `settings.py` (e.g., concurrency settings) are thoroughly tested, as they may significantly impact performance.
