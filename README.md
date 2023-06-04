# TL Scraper

### Overview:
Python script to pull stats from your torrentleech account.<br>
View the usage variables to see stats it can pull.<br>

**Use at your own discretion don't spam the site, I'm not responsible if you get banned or otherwise.**

### Usage Examples:
With 2FA
```python
import tl_scraper

username = 'REPLACE_WITH_YOUR_USERNAME'
password = 'REPLACE_WITH_YOUR_PASSWORD'
auth_key = 'REPLACE_WITH_YOUR_FULL_AUTH_KEY'

scraper = tl_scraper.Scraper(username=username, password=password, auth_key=auth_key)
data = scraper.login()

username = data[0]
notifications = data[1]
uploaded = data[2]
downloaded = data[3]
achievement = data[4]
points = data[5]
requests = data[6]
invites = data[7]
lottery_tickets = data[8]
buffer = data[9]
ratio = data[10]
hit_and_runs = data[11]
```

Without 2FA
```python
import tl_scraper

username = 'REPLACE_WITH_YOUR_USERNAME'
password = 'REPLACE_WITH_YOUR_PASSWORD'

scraper = tl_scraper.Scraper(username=username, password=password)
data = scraper.login()

username = data[0]
notifications = data[1]
uploaded = data[2]
downloaded = data[3]
achievement = data[4]
points = data[5]
requests = data[6]
invites = data[7]
lottery_tickets = data[8]
buffer = data[9]
ratio = data[10]
hit_and_runs = data[11]
```

With specific website


*Currently I'm unable to get it to pull data from sites other then https://www.torrentleech.me but your're welcome to submit a PR if you're able to figure it out. As of right now it works for my use case and I haven't run into any serious issues. I'll look into it further if it becomes a problem.
```python
import tl_scraper

username = 'REPLACE_WITH_YOUR_USERNAME'
password = 'REPLACE_WITH_YOUR_PASSWORD'
url = 'REPLACE_WITH_URL'

scraper = tl_scraper.Scraper(username=username, password=password, url=url)
data = scraper.login()

username = data[0]
notifications = data[1]
uploaded = data[2]
downloaded = data[3]
achievement = data[4]
points = data[5]
requests = data[6]
invites = data[7]
lottery_tickets = data[8]
buffer = data[9]
ratio = data[10]
hit_and_runs = data[11]
```
