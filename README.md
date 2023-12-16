# WarDataInsights



## Overview

In October 7th, 2023, during the unfortunate events in Israel, I found myself in Berlin as part of a student exchange program. As my heart was broken and my mind was lost, I realized that contributing in some way or keeping myself busy might be a way to cope. This led me to pursue something I had wanted to do for a while – extracting insights from real data.



Every day, with automationI I ***scraped data*** (alrams) from the Home Front Command site, ran ***ETL*** procedures, and ***visualized*** the results.



# Table of Contents

1. [ Data Scraping](#desc)  
2. [ ETL ](#usage)  
3. [Visualstation](#vis)

<a name="desc"></a>  

## 1. Data Scraping

So, in order to scrape data from the site, I used Python packages called **Selenium** and **BeautifulSoup**

In a nutshell Selenium helps control web browsers, while BeautifulSoup is a sidekick for digging out the good stuff from web pages:

<details><summary>code sample</summary>

```python
from selenium import webdriver
    from bs4 import BeautifulSoup
    ...
    # Launch a browser using Selenium
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    html_content = driver.page_source
    ...
    # Parse HTML content with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    notifications_parent = soup.find('div', class_='ah-notifications')
```
</details>


Having said that, I was able to itrate the html page (ptyhon) and collect the data i would like to 

<details><summary>code sample </summary> 

```python
   alert_tables = notifications_parent.select('[class*="alert_table"]')
   ...
   for alert_table in alert_tables:
   ....
   alert_type_element = alert_table.find('h4', class_='alertTableCategory'``` 

```


</details>


The data, saved into a local data base in my computer using sqllite and sql 

```python
   alert_tables = notifications_parent.select('[class*="alert_table"]')
   ...
   for alert_table in alert_tables:
   ....
   alert_type_element = alert_table.find('h4', class_='alertTableCategory')
```

Too see the full script click [here](https://github.com/ofirtopchy/WarDatainsight/blob/main/Extract.py) 



<a name="usage"></a>  

## 2. ETL

T.B.D



<a name="vis"></a>  

## 3. Visualstation

T.B.D
