# GhettoGusser - Remake of 'Ghetto Price is Right' from 2022 CCOMP-11p class
# Originally by Story on the Programming Discord, re-made Chase Varvayanis

# link_file_maker; Scrapes all valid links from the given Craigslist
# URL. Saves the collected links to a file named 'cl_listings_file.txt' in the
# script's parent directory.

# last revision 11-14-2024


import os
import requests
from bs4 import BeautifulSoup


def generate_listings_file(url):
    """
    Collect all links from a Craigslist search page and save them to a text
    file.

    Performs the following steps:
    1. Scrapes all valid links from the given Craigslist URL.
    2. Saves the collected links to a file named 'cl_listings_file.txt' in the
       script's parent directory.

    Args:
        url (str): The URL of the Craigslist search page to scrape.

    Returns:
        str: The path to the generated text file containing the links.
    """
    # Get the path to the script's parent folder
    parent_folder = os.path.dirname(os.path.abspath(__file__))
    output_file_path = os.path.join(parent_folder, "cl_listings_file.txt")

    # Collect links
    def collect_links(url):
        """
        Scrape and collect all links from a Craigslist search page.

        This function extracts all anchor (`<a>`) tags containing valid `href`
        attributes from the given URL.

        Args:
            url (str): The URL of the Craigslist search page to scrape.

        Returns:
            list: A list of all valid links found on the page.
        """
        # Obtained my User-Agent from here: https://myhttpheader.com/
        # Honestly exists more out of paranoia about getting my IP blocked
        # by CL, probably don't actually need it.
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
            )
        }
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all links (to listings) on the page and store them in a list
        links = []
        for link in soup.find_all("a", href=True):
            # Ensure the href attribute exists and is populated, if so adds
            # to the links list
            if link['href']:
                full_url = link['href']
                links.append(full_url)
        return links

    all_links = collect_links(url)

    # Save links to a file in the script's folder
    def save_links_to_file(links, filename):
        """
        Save a list of links to a text file.

        Each link is written on a new line, making the file easily parsable
        for later use (e.g., randomly selecting a line for further processing).

        Args:
            links (list): A list of links to save.
            filename (str): The name of the file to save the links to.
        """
        with open(filename, 'w') as file:
            for link in links:
                file.write(link + "\n")

    save_links_to_file(all_links, output_file_path)

    return output_file_path


# Test Code
if __name__ == "__main__":
    # URL of the Craigslist search page
    url = "https://sacramento.craigslist.org/search/sss"

    # Process the links and get the output file path
    generated_output_file_path = generate_listings_file(url)

    # Print results
    print(
        "listing link file generated and saved to: "
        f"{generated_output_file_path}."
        )
