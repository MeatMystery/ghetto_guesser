# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis
# ChatGPT used to help resolve syntax issues & make docstring format prettier,
# linted w/ FLAKE8, spellchecked w/ StreetSideSoftware's Spell Checker

# round_data_maker module; Takes the cl_listings_file generated previously, and
# selects a random predetermined padded number of listings to scrape. Scrapes
# the listings for title, text, description, photourl, etc, and creates a list
# of dictionaries that contain that info to be used as round data

# last revision 11-14-2024


import os
import requests
from bs4 import BeautifulSoup
from random import sample
import re


def make_round_data(filename):
    """
    Generates round data by extracting valid Craigslist listings from the
    link file, storing the data as a list of dictionaries. Includes a nested
    function to trim the list to 5 elements for the final round.
    """

    def link_list_trimmer():
        """
        Trims the list of Craigslist listings to be more easily parsable by
        gathering x random links from the Craigslist search result file and
        storing them in a list.
        """
        all_links = []

        parent_folder = os.path.dirname(os.path.abspath(__file__))
        file_to_open = os.path.join(parent_folder, filename)

        with open(file_to_open) as file:
            for line in file:
                all_links.append(line.rstrip())

        all_links = all_links[2:]  # Skip first two lines bc they're garbage
        return sample(all_links, 15)  # Return x random links

    def redact_price(text, price):
        """
        Redacts the price from the given title/description if it
        appears in most formats, replaces it with [REDACTED PRICE].
        """
        if text is None or price is None:
            return text  # No price or text to redact

        # Convert price to string for pattern matching
        price_str = str(price)

        # Define patterns for potential price formats
        # Had ChatGPT help with getting the search string formatting and syntax
        # correct to catch most cases.
        price_patterns = [
            rf'\b{price_str}\b',             # Exact match of price
            rf'\b{price_str}\.\d{{2}}\b',    # Price with decimal
            rf'\$\s*{price_str}\b',          # Price prefixed by $
            rf'\$\s*{price_str}\.\d{{2}}\b'  # Price prefixed by $ with decimal
        ]
        header_text_to_remove = [
            # There is still one leading newline for formatting purposes
            'QR Code Link to This Post\n\n\n'
        ]

        # Replace all price patterns with [REDACTED PRICE]
        for pattern in price_patterns:
            text = re.sub(
                pattern,
                '[REDACTED PRICE]',
                text,
                flags=re.IGNORECASE
            )

        # Remove unnecessary header text
        for ttr in header_text_to_remove:
            text = re.sub(
                ttr,
                '',
                text,
                flags=re.IGNORECASE
            )

        return text

    def extract_craigslist_data(url):
        """
        Extracts data from a Craigslist URL, including the title, price, photo
        link, and description. Returns a dictionary if all fields are valid,
        or None otherwise.
        """
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

            # Redact price from the title
            if title:
                title = redact_price(title, price)

            # Extract the main photo link
            main_photo = soup.find('img')
            main_photo = (
                main_photo['src'].strip()
                if main_photo and 'src' in main_photo.attrs
                else None
                )

            # Extract the description
            posting_body = soup.find('section', id='postingbody')
            description = posting_body.text.strip() if posting_body else None
            # Shorten to 800 characters for formatting
            description = description[:600]

            # Redact price from the description
            if description:
                description = redact_price(description, price)

            # Create the dictionary
            data_dict = {
                "url": url,
                "title": title,
                "description": description,
                "photo": main_photo,
                "price": price,
                }

            # Discard dictionary if any field is None
            if None in data_dict.values():
                return None
            return data_dict

        except Exception as e:
            print(f"ERROR: {e}")
            return None

    def final_round_data(data):
        """
        Trims the listing data list to the final output of 5 elements.
        """
        return sample(data, 5) if len(data) >= 5 else data

    # Generate URLs and extract data
    url_list = link_list_trimmer()
    results = []

    for url in url_list:
        result = extract_craigslist_data(url)
        if result:
            results.append(result)

    # Trim the results for the final round
    round_data = final_round_data(results)
    return round_data


# Test Code
# Made the base function, had ChatGPT do the formatting because
# I could not be arsed for code that was just diagnostic
if __name__ == '__main__':
    # Print pretty results
    def print_pretty_results(results):
        if not results:
            print("No valid listings found.")
            return

        for idx, result in enumerate(results, start=1):
            print(f"{'='*40}\nListing #{idx}\n")
            print(f"Title: {result['title']}")
            print(f"Price: {result['price']}")
            print(f"Description:\n{result['description']}")
            print(f"Photo URL: {result['photo']}")
            print(f"Original Listing: {result['url']}")
            print(f"{'='*40}\n")

    # Generate Round Data
    results = make_round_data('cl_listings_file.txt')
    print(results)
    print_pretty_results(results)
