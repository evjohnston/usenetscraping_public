Usenet Scraping Project

Two simple python codes that scrape the google groups Usenet archive for thread and comment metadata.

Thread_scraper: scrapes all the thread metadata in a newsgroup (including title, url, and date) and create a unique thread ID to track which posting behavior chronologically. Output a csv of all the threads in a newsgroup.

Comment_scraper: scrapes all the comment metadata (including author, date, text, and comment number) for every comment in every thread URL in a csv from the thread_scraper. Outputs to a csv of all the comments in all the threads of a newsgroup. 