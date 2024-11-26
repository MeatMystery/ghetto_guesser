import os
import requests
from bs4 import BeautifulSoup
from random import sample


def make_round_data(filename):
    """
    Generates round data by extracting valid Craigslist listings from the given file.
    """

    def link_list_trimmer():
        """
        Gathers 20 random links from the Craigslist search results and stores them in a list.
        """
        all_links = []

        parent_folder = os.path.dirname(os.path.abspath(__file__))
        file_to_open = os.path.join(parent_folder, filename)

        with open(file_to_open) as file:
            for line in file:
                all_links.append(line.rstrip())

        all_links = all_links[2:]  # Skip the first two lines
        return sample(all_links, 20)  # Return 20 random links

    def extract_craigslist_data(url):
        """
        Extracts data from a Craigslist URL, including the title, price, photo link, and description.
        Returns a tuple if all fields are valid, or None otherwise.
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
    # Display pretty results, made a base function formatted with
    # ChatGPT as I could not be arsed to format it
    def print_pretty_results(results):
        if not results:
            print("No valid listings found.")
            return

        for idx, result in enumerate(results, start=1):
            url, title, description, photo, price = result
            print(f"{'='*40}\nListing #{idx}")
            print(f"Title: {title}")
            print(f"Price: {price}")
            print(f"Description:\n{description}")
            print(f"Photo URL: {photo}")
            print(f"Original Listing: {url}")
            print(f"{'='*40}\n")

    # Generate results
    results = make_round_data('cl_listings_file.txt')
    print_pretty_results(results)
