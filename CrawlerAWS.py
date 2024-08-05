import argparse
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

def search_all_directories(base_url, max_depth=3, verbose=False, directories_file=None):
  
    directories = set()

   
    visited_urls = set()


    potential_directories = set()


    if directories_file:
        if os.path.exists(directories_file):
            with open(directories_file, 'r') as file:
                for line in file:
                    potential_directories.add(line.strip())
        else:
            if verbose:
                print(f"File {directories_file} not found.")
    
    def recursive_crawl(url, depth):
        if depth > max_depth or url in visited_urls:
            return

        try:
            response = requests.get(url)
            response.raise_for_status() 
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
                            # Check if the link is a potential directory
                            for potential_dir in potential_directories:
                                if potential_dir in absolute_link:
                                    directories.add(absolute_link)
                            # Recursively crawl nested directories
                            recursive_crawl(absolute_link, depth + 1)
        except requests.exceptions.RequestException as e:
            if verbose:
                print(f"Error while accessing {url}: {e}")
        except requests.exceptions.HTTPError as e:
            if verbose:
                print(f"HTTP error occurred while accessing {url}: {e}")

    def verify_directories(directories):
        valid_directories = set()
        for directory in directories:
            try:
                response = requests.get(directory)
                if response.status_code == 200:
                    valid_directories.add(directory)
                elif verbose:
                    print(f"Invalid directory (status code {response.status_code}): {directory}")
            except requests.exceptions.RequestException as e:
                if verbose:
                    print(f"Error while verifying {directory}: {e}")
        return valid_directories

    recursive_crawl(base_url, 0)
    verified_directories = verify_directories(directories)
    return verified_directories

def upload_to_s3(directories, bucket_name, s3_file_name, aws_access_key, aws_secret_key, verbose=False):
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    try:
   
        with open('/tmp/visited_directories.txt', 'w') as file:
            for directory in directories:
                file.write(directory + '\n')
    
        s3.upload_file('/tmp/visited_directories.txt', bucket_name, s3_file_name)
        if verbose:
            print(f"Uploaded visited directories to s3://{bucket_name}/{s3_file_name}")
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except NoCredentialsError as e:
        print(f"Credentials not available: {e}")
    except PartialCredentialsError as e:
        print(f"Incomplete credentials: {e}")
    except Exception as e:
        print(f"Error uploading to S3: {e}")

if __name__ == "__main__":
 
    parser = argparse.ArgumentParser(description="Web Crawler: Search Directories")


    parser.add_argument("website", help="The URL of the website to crawl.")
    parser.add_argument("-d", "--depth", type=int, default=3, help="Maximum depth for crawling (default: 3)")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print verbose output")
    parser.add_argument("-f", "--file", help="File containing a list of potential directory names")
    parser.add_argument("-b", "--bucket", help="S3 bucket name to upload the results")
    parser.add_argument("-s", "--s3file", help="S3 file name to save the results")

    
    args = parser.parse_args()


    website_url = args.website
    max_crawl_depth = args.depth
    verbose_mode = args.verbose
    directories_file = args.file
    bucket_name = args.bucket
    s3_file_name = args.s3file

    result = search_all_directories(website_url, max_depth=max_crawl_depth, verbose=verbose_mode, directories_file=directories_file)

    if bucket_name and s3_file_name:
        aws_access_key = input("Enter your AWS Access Key: ")
        aws_secret_key = input("Enter your AWS Secret Key: ")
        upload_to_s3(result, bucket_name, s3_file_name, aws_access_key, aws_secret_key, verbose=verbose_mode)

    print("Existing Directories:")
    for directory in result:
        print(directory)
