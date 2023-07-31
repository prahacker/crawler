import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def search_all_directories(base_url, max_depth=3, verbose=False):
    # Create a set to store the found directories to avoid duplicates
    directories = set()

    # Create a set to store the already visited URLs
    visited_urls = set()

    def recursive_crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
            visited_urls.add(url)

            if verbose:
                print(f"Searching: {url}")

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'lxml')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    if not href.startswith('javascript:void(0)'):
                        absolute_link = urljoin(url, href)
                        if absolute_link.startswith(base_url) and not absolute_link.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf')):
                            directories.add(absolute_link)
                            # Recursively crawl nested directories
                            recursive_crawl(absolute_link, depth + 1)
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Error while accessing {url}: {e}")
        except requests.exceptions.HTTPError as e:
            if verbose:
                print(f"HTTP error occurred while accessing {url}: {e}")

    recursive_crawl(base_url, 0)
    return directories

if __name__ == "__main__":
    # Create the argument parser
    parser = argparse.ArgumentParser(description="Web Crawler: Search Directories")

    # Add arguments
    parser.add_argument("website", help="The URL of the website to crawl.")
    parser.add_argument("-d", "--depth", type=int, default=3, help="Maximum depth for crawling (default: 3)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")

    # Parse the arguments
    args = parser.parse_args()

    # Extract the arguments
    website_url = args.website
    max_crawl_depth = args.depth
    verbose_mode = args.verbose

    # Call the web crawler function
    result = search_all_directories(website_url, max_depth=max_crawl_depth, verbose=verbose_mode)

    # Print the result
    print("Existing Directories:")
    for directory in result:
        print(directory)
