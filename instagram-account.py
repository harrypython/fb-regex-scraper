from Scrape import Scrape

s = Scrape("webdriver/geckodriver")

s.set_pattern(pattern="@\w(?:(?:\w|(?:\.(?!\.))){0,28}(?:\w))?")

a = s.get_posts(group="123456789012345")

for b in a:
    print("https://www.instagram.com/{}/".format(b.replace("@","")))

