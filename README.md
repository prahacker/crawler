# Crawler
website crawler to find directories
# Web Crawler: Search Directories

This Python script is a web crawler designed to search for existing directories on a specified website. It starts from a given base URL and recursively navigates through links to find directories containing the specified search term.

## How to Use

1. **Installation:** Ensure you have Python installed on your system.

2. **Clone the Repository:** Clone this repository to your local machine using `git clone` or download the ZIP file and extract it.

3. **Install Dependencies:** Navigate to the project directory and install the required dependencies using pip:  pip install requests beautifulsoup4

4. **Run the Crawler:** To use the web crawler, execute the `crawler.py` script from the terminal or command prompt, providing the required arguments: python crawler.py <website_url> -d <depth> -v

- `<website_url>`: Replace this with the URL of the website you want to crawl.
- `-d <depth>`: Specify the maximum depth for crawling (default: 3). This controls how many levels deep the crawler will search.
- `-v`: Optional flag to enable verbose output. This will print URLs being searched and any errors encountered.

5. **Output:** The script will display a list of existing directories found during the crawl.

## Example
python crawler.py https://example.com -d 3 -v
This command will initiate the web crawler, searching for directories on `https://example.com` up to a depth of 5 and displaying verbose output.

## Important Notes

- Ensure that you have proper authorization and comply with the website's terms of service before running the crawler.
- Web crawling can put a load on servers, so be mindful of not overwhelming the website's resources.
- Always use the verbose mode with caution, as it may print sensitive information or sensitive URLs.

Happy Crawling! 🕷️





