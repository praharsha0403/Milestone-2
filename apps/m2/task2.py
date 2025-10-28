#used BeautifulSoup to parse HTML files and extract image sources
from bs4 import BeautifulSoup, SoupStrainer
import sys

#did this function to extract all image URLs (src attributes) from an HTML file
def extract_images(file_path):
    try:
        #opened the given HTML file in read mode
        with open(file_path, 'r', encoding='utf-8') as f:
            #used SoupStrainer to filter and parse only <img> tags for efficiency
            only_img_tags = SoupStrainer("img")
            #parsed the HTML file using lxml parser (faster and cleaner)
            soup = BeautifulSoup(f, "lxml", parse_only=only_img_tags)

            #looped through all <img> tags that have a 'src' attribute
            for img in soup.find_all("img", src=True):
                #printed the source URL/path of each image
                print(img["src"])

    #handled the case where the provided file path doesn’t exist
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    #caught any other unexpected errors
    except Exception as e:
        print(f"An error occurred: {e}")

#main program starts here
if __name__ == "__main__":
    #checked if a file path argument is passed through the command line
    if len(sys.argv) < 2:
        #if not provided, showed correct usage format
        print("Usage: python task2.py <html_file>")
    else:
        #if provided, called the function to extract images from that file
        extract_images(sys.argv[1])
