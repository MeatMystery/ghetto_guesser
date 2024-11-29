import os
import requests
from bs4 import BeautifulSoup
from random import sample
import re


def make_round_data(filename):
    """
    Generates round data by extracting valid Craigslist listings from the
    link file.
    """

    def link_list_trimmer():
        """
        Trims the list of craigslist listing s to be more easily paresable by
        gathering 20 random links from the Craigslist search results and stores
        them in a list.
        """
        all_links = []

        parent_folder = os.path.dirname(os.path.abspath(__file__))
        file_to_open = os.path.join(parent_folder, filename)

        with open(file_to_open) as file:
            for line in file:
                all_links.append(line.rstrip())

        all_links = all_links[2:]  # Skip first two lines bc they're garbage
        return sample(all_links, 20)  # Return 20 random links

    def trim_description(description, price):
        """
        Redacts the price from the description if it appears in any format.
        Replaces it with [REDACTED PRICE].
        Used ChatGPT to help find the possible variations price could take
        and how to pass them to the regular expression module
        """
        if price is None:
            return description  # No price to redact

        # Convert price to string for pattern matching
        price_str = str(price)

        # Define patterns for potential price formats done w/ ChatGPT
        price_patterns = [
            rf'\b{price_str}\b',             # Exact match of price
            rf'\b{price_str}\.\d{{2}}\b',    # Price with decimal
            rf'\$\s*{price_str}\b',          # Price prefixed by $
            rf'\$\s*{price_str}\.\d{{2}}\b'  # Price prefixed by $ with decimal
            ]
        text_to_remove = [
            'QR Code Link to This Post\n\n\n'
            ]
        # Replace all matches with [REDACTED PRICE]
        for pattern in price_patterns:
            description = re.sub(
                pattern,
                '[REDACTED PRICE]',
                description,
                flags=re.IGNORECASE
                )

        for ttr in text_to_remove:
            description = re.sub(
                ttr,
                '',
                description,
                flags=re.IGNORECASE
                )

        return description

    def extract_craigslist_data(url):
        """
        Extracts data from a Craigslist URL, including the title, price, photo
        link, and description. Returns a tuple if all fields are valid, or None
        otherwise.
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

            # Redact price from description
            if description:
                description = trim_description(description, price)

            # Create the tuple
            data_tuple = (url, title, description, main_photo, price)

            # Discard tuple if any field is None
            if None in data_tuple:
                return None
            return data_tuple

        except Exception as e:
            print(f"ERROR: {e}")
            return None

    # Generate URLs and extract data
    url_list = link_list_trimmer()
    results = []

    for url in url_list:
        result = extract_craigslist_data(url)
        if result:
            results.append(result)

    return results


# Test Code
if __name__ == '__main__':
    # Display pretty results, made a base function and formatted with
    # ChatGPT for testing readability as I could not be arsed to format
    # it
    def print_pretty_results(results):
        if not results:
            print("No valid listings found.")
            return

        for idx, result in enumerate(results, start=1):
            url, title, description, photo, price = result
            print(f"{'='*40}\nListing #{idx}\n")
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Description:\n{description}")
            print(f"Photo URL: {photo}")
            print(f"Original Listing: {url}")
            print(f"{'='*40}\n")

    # Generate results
    results = make_round_data('cl_listings_file.txt')
    print_pretty_results(results)
