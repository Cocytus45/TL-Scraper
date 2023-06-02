# TL Scraper

### Overview:
Python script to pull stats from your torrentleech account.<br>
View the usage variables to see stats it can pull.<br>
Only spent a couple minutes on this so not optimized PRs welcome.

**Use at your own discretion don't spam the site, I'm not responsible if you get banned or otherwise.**

### Usage Example:
```python
import tl_scraper

username = 'REPLACE_WITH_YOUR_USERNAME'
password = 'REPLACE_WITH_YOUR_PASSWORD'

scraper = tl_scraper.Scraper()
data = scraper.login(username=username, password=password)

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
