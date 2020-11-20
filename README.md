# Facebook Regex Scraper

Scrape Facebook Public Group Posts without using Facebook API using [Selenium](https://seleniumhq.github.io/docs/).

## What It can Do

- Scrape text from Public Group Posts

## Install Requirements

Please make sure Firefox is installed and [geckodriver](https://github.com/mozilla/geckodriver) is available.

```sh
pip install -r requirements.txt
```

## Usage

```python
from Scrape import Scrape

scraper = Scrape("webdriver/geckodriver")
 
# pattern to find Instagram profiles. Source: regex101.com/r/uNc8HG/1
my_pattern = "@\w(?:(?:\w|(?:\.(?!\.))){0,28}(?:\w))?"

scraper.set_pattern(pattern=my_pattern)

for r in scraper.get_posts(group="123456789012345"):
    print("https://www.instagram.com/{}/".format(r.replace("@","")))

```

### Note:

- Please use this code for Educational purposes only
