#used BeautifulSoup to parse HTML and extract all hyperlink URLs
from bs4 import BeautifulSoup, SoupStrainer
import sys

#did this function to extract all link URLs (href attributes) from an HTML file
def extract_links(file_path):
    try:
        #opened the given HTML file in read mode with UTF-8 encoding
        with open(file_path, 'r', encoding='utf-8') as f:
            #used SoupStrainer to filter and parse only <a> (anchor) tags for better performance
            only_a_tags = SoupStrainer("a")
            #parsed only the anchor tags using lxml parser
            soup = BeautifulSoup(f, "lxml", parse_only=only_a_tags)

            #looped through all <a> tags that contain an 'href' attribute
            for tag in soup.find_all("a", href=True):
                #printed the value of each href (the actual link URL)
                print(tag["href"])

    #handled case when the provided file is not found
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    #caught any other unexpected errors and printed them
    except Exception as e:
        print(f"An error occurred: {e}")

#main program entry point
if __name__ == "__main__":
    #checked if the user provided a file path argument
    if len(sys.argv) < 2:
        #if no file was given, displayed correct usage format
        print("Usage: python task3.py <html_file>")
    else:
        #if a file was given, called the function to extract all links from it
        extract_links(sys.argv[1])
