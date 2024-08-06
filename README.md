<h1 style="text-align: center;"><strong>Usenet Google Group Archive Scraping Project</strong></h1>

Two simple python codes that scrape the google groups Usenet archive for thread and comment metadata.

**Thread_scraper:** scrapes all the thread metadata in a newsgroup (including title, url, and date) and create a unique thread ID to track which posting behavior chronologically. Output a csv of all the threads in a newsgroup.

**Comment_scraper:** scrapes all the comment metadata (including author, date, text, comment number, and unique url string (which can be used to reconstruct its url)) for every comment in every thread URL in a csv from the thread_scraper. Outputs to a csv of all the comments in all the threads of a newsgroup. 

*You'll need to make sure pandas, bs4, selenium, and webdriver-manager are all installed.*
