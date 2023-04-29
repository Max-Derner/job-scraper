## job-scraper
A tiny job scraping job for auto-mating job hunting.  
The scraper opens up websites, searches for the word Manchester case insensitive,  
and emails the target if any hits are found.  
If a website cannot be accessed it will email the admin which pages don't work.  
If a runtime exception occurs, the stack trace is emailed to the admin also.  

This is a tiny quickly spun up home-brew project.  
While I normally quite like to use TDD where I can, this is something I designed over a weekend in a hurry.


### Requirements
You must install selenium.
This project uses Firefox and the Geckodriver.
As such, you must install these too.
You must also set up a gmail account to send emails from and get an app password for it.

### Required files
You must create two json files which are excluded from this repository for privacy purposes.
* `email_addresses.json`
* `passwords.json`

email_addresses.json is filled as such:  
```
{  
    "APP_PASSWORD": "fill this in with a proper password"  
}  
```

passwords.json is filled as such:  
```
{  
    "ADMIN": "your email address",  
    "TARGET": "person who gets emailed about jobs",  
    "ROBOT": "email address you have app password for"  
}  
```