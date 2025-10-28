#used BeautifulSoup to parse HTML and extract the <title> tag contents
import sys
from bs4 import BeautifulSoup, SoupStrainer

#did this function to read an HTML file and print all the titles found in it
def extract_titles(path):
    try:
        #opened the HTML file in read mode with UTF-8 encoding
        with open(path, 'r', encoding='utf-8') as f:
            #used SoupStrainer to only parse <title> tags for efficiency
            strainer = SoupStrainer('title')
            #parsed the HTML file with lxml parser and limited scope to title tags
            soup = BeautifulSoup(f, 'lxml', parse_only=strainer)
            #found all title tags in the parsed HTML
            titles = soup.find_all('title')
            #looped through each title tag and printed its text content without spaces
            for t in titles:
                print(t.text.strip())
    #caught any exception (like file not found or parse errors) and printed it
    except Exception as e:
        print("error:", e)

#main entry point of the script
if __name__ == '__main__':
    #checked if user provided the HTML file path as a command-line argument
    if len(sys.argv) < 2:
        #if no file path was given, asked the user to provide one
        print("give html file path")
    else:
        #if a path was given, called the function to extract and print all HTML titles
        extract_titles(sys.argv[1])

