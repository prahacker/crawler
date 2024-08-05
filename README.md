# Web Crawler: Search Directories

This Python script crawls a given website to search for directories and optionally uploads the results to an AWS S3 bucket.

## Features

- Recursively crawl a website up to a specified depth.
- Search for directories and validate them by checking for a 200 status code.
- Optionally upload the list of valid directories to an AWS S3 bucket.
- Option to provide a file containing potential directory names.

## Prerequisites

- Python 3.x
- `requests` library
- `beautifulsoup4` library
- `lxml` parser
- `boto3` library

## Installation

1. Install the required libraries using `pip`:

    ```sh
    pip install requests beautifulsoup4 lxml boto3
    ```

2. Ensure you have AWS credentials configured on your system or provide them when prompted.

## Usage

```sh
python web_crawler.py [-h] [-d DEPTH] [-v] [-f FILE] [-b BUCKET] [-s S3FILE] website
'''

**Output:** The script will display a list of existing directories found during the crawl.

## Example
python web_crawler.py -d 5 -v -b my-s3-bucket -s directories.txt https://example.com
This command will initiate the web crawler, searching for directories on `https://example.com` up to a depth of 5 and displaying verbose output and save the output to s3 bucket.

## Important Notes
- If you choose to upload the results to an S3 bucket, you will be prompted to enter your AWS Access Key and Secret Key. Ensure that the provided credentials have the necessary permissions to upload files to the specified S3 bucket.
- Ensure that you have proper authorization and comply with the website's terms of service before running the crawler.
- Web crawling can put a load on servers, so be mindful of not overwhelming the website's resources.
- Always use the verbose mode with caution, as it may print sensitive information or sensitive URLs.

Happy Crawling! 🕷️





