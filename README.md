## job-scraper
A tiny job scraping job for auto-mating job hunting.  
The scraper opens up websites, searches for the word Manchester case insensitive,  
and emails the target if any hits are found.  
If a website cannot be accessed it will email the admin which pages don't work.  
If a runtime exception occurs, the stack trace is emailed to the admin also.  

This is a tiny quickly spun up home-brew project.  
While I normally quite like to use TDD where I can, this is something I designed over a weekend in a hurry.


### Requirements
Ideally you should set up a venv for this project to run inside.  
execute the following commands:  
`python3 -m venv jobsworth`  
`source jobsworth/bin/activate`  
`pip install -r requirements.txt`  

Now when you want to run the project, activate the venv first:  
`source jobsworth/bin/activate`  
then run
`python3 main.py`


### Required files
You must create two json files which are excluded from this repository for privacy purposes.
* `email_addresses.json`
* `passwords.json`
* `sites.json`

email_addresses.json is structured as such:  
```
{  
    "APP_PASSWORD": "fill this in with a proper password"  
}  
```

passwords.json is structured as such:  
```
{  
    "ADMIN": "your email address",  
    "TARGET": "person who gets emailed about jobs",  
    "ROBOT": "email address you have app password for"  
}  
```

sites.json is structured as such:
```
{
    "page-alias": {
        "page": "https://www.page.co.uk/careers/#vacanciesmain",
        "main-content": "//*[@id=\"main-content\"]"  <--- this is an x-path for the pages main content
    },
    .......
}
```
the x-path should point to something that can provide a view of all the available jobs

regex.json is structured as such:
```

```