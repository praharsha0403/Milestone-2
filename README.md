# BeautifulSoup
Beautiful Soup is a library that makes it easy to scrape information
from web pages. It sits atop an HTML or XML parser, providing Pythonic
idioms for iterating, searching, and modifying the parse tree.

## Environment Setup and Installation

```bash
~/> cd beautifulsoup
```
#### Create ```Conda``` environment and activate it inside ```~/beautifulsoup``` directory
```bash
# python=3.10 is required
:~/ cd beautifulsoup
beautifulsoup:~/ conda create -n bs4 python=3.10
beautifulsoup:~/ conda activate bs4
```

### OR

#### Create ```Venv``` environment and activate it inside ```~/beautifulsoup``` directory
```bash
# python=3.10 is required
:~/ cd beautifulsoup
beautifulsoup:~/ python3 -m venv venv
beautifulsoup:~/ source venv/bin/activate  # On macOS/Linux
```

#### Install all dependencies with pytest
```bash
beautifulsoup:~/ pip install -e .
beautifulsoup:~/ pip install pytest
```


#### Run Test
```bash
#  If you are using conda env
cd beautifulsoup
beautifulsoup:~/ pytest
```
```bash
# if you are using venv env
cd beautifulsoup/bs4/tests
beautifulsoup/bs4/tests:~/ pytest
```





# Quick start

```
>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup("<p>Some<b>bad<i>HTML")
>>> print(soup.prettify())

```
```
<html>
 <body>
  <p>
   Some
   <b>
    bad
    <i>
     HTML
    </i>
   </b>
  </p>
 </body>
</html>
>>> soup.find(string="bad")
'bad'
>>> soup.i
<i>HTML</i>
#
>>> soup = BeautifulSoup("<tag1>Some<tag2/>bad<tag3>XML", "xml")
#
>>> print(soup.prettify())
<?xml version="1.0" encoding="utf-8"?>
<tag1>
 Some
 <tag2/>
 bad
 <tag3>
  XML
 </tag3>
</tag1>
```



# Links

* [Homepage](https://www.crummy.com/software/BeautifulSoup/bs4/)
* [Documentation](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
* [Discussion group](https://groups.google.com/group/beautifulsoup/)
* [Development](https://code.launchpad.net/beautifulsoup/)
* [Bug tracker](https://bugs.launchpad.net/beautifulsoup/)
* [Complete changelog](https://bazaar.launchpad.net/~leonardr/beautifulsoup/bs4/view/head:/CHANGELOG)






