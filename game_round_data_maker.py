# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis

# x

# last revision 11-14-2024


import os
import requests
from bs4 import BeautifulSoup
from random import sample


def link_list_trimmer(filename):
    """
    Gathers 20 random links from the craigslist search results, and stores to
    a list
    """
    all_links = []

    parent_folder = os.path.dirname(os.path.abspath(__file__))
    file_to_open = os.path.join(parent_folder, filename)

    with open(file_to_open) as file:
        for line in file:
            all_links.append(line.rstrip())

    all_links = all_links[2:]

    trimmed_list = sample(all_links, 20)

    return trimmed_list


def extract_craigslist_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract the title
        title = soup.find('span', id='titletextonly')
        title = title.text.strip() if title else None

        # Extract the price
        price = soup.find('span', class_='price')
        if price:
            # Clean and convert price to int
            price = int(
                price.text.replace(',', '')
                .replace(' ', '')
                .replace('$', '')
                .strip()
            )
            # Discard price if it is 1 or 1234 (filler price)
            if price in {1, 1234}:
                price = None
        else:
            price = None

        # Extract the main photo link
        main_photo = soup.find('img')
        main_photo = (
            main_photo['src'].strip()
            if main_photo and 'src' in main_photo.attrs
            else None)

        # Extract the description
        posting_body = soup.find('section', id='postingbody')
        description = posting_body.text.strip() if posting_body else None

        # Creating the tuple
        data_tuple = (url, title, description, main_photo, price)

        # Discard tuple if any field is None
        if None in data_tuple:
            return None
        return data_tuple

    except Exception as e:
        print(f"ERROR: {e}")
        return None


# Make game round data
def make_round_data():
    url_list = (link_list_trimmer('cl_listings_file.txt'))
    results = []

    for url in url_list:
        result = extract_craigslist_data(url)
        if result:
            results.append(result)

    return results


# Test Code
if __name__  == '__main__':
    # Trim file to 20 links and put in a list
    print(link_list_trimmer('cl_listings_file.txt'))

    # Display pretty results, made a base function formatted with
    # ChatGPT as i could not be arsed to format it
    def print_pretty_results(results):
        if not results:
            print("No valid listings found.")
            return

        for idx, result in enumerate(results, start=1):
            url, title, description, photo, price = result
            print(f"{'='*40}\nListing\n #{idx}")
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Description:\n{description}")
            print(f"Photo URL: {photo}")
            print(f"Original Listing: {url}")
            print(f"{'='*40}\n")

    print_pretty_results(results)
