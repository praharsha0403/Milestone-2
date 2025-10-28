#used BeautifulSoup and SoupReplacer to replace specific HTML tags in a file
from bs4 import BeautifulSoup
from bs4.soupreplacer import SoupReplacer
import sys

#did this function to open an HTML file and replace one tag with another
def run_replacer(file_path, og_tag, alt_tag):
    try:
        #opened the given HTML file for reading
        with open(file_path, 'r', encoding='utf-8') as f:
            #created a SoupReplacer object to swap the old tag with the new tag
            replacer = SoupReplacer(og_tag, alt_tag)
            #parsed the HTML file using BeautifulSoup and applied the replacer
            soup = BeautifulSoup(f, 'html.parser', replacer=replacer)
            #printed the modified HTML in a readable (indented) format
            print(soup.prettify())

    #handled file not found error if the file path is invalid
    except FileNotFoundError:
        print(f"File not found: {file_path}")
    #caught and printed any other unexpected error
    except Exception as e:
        print(f"An error occurred: {e}")

#main entry point of the program
if __name__ == "__main__":
    #checked that user passed exactly three command-line arguments (file, old tag, new tag)
    if len(sys.argv) != 4:
        #if not, showed the correct usage format
        print("Usage: python task6.py <html_file> <og_tag> <alt_tag>")
    else:
        #if correct arguments were passed, ran the tag replacer function
        run_replacer(sys.argv[1], sys.argv[2], sys.argv[3])

