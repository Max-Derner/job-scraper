## job-scraper
A tiny job scraping job for auto-mating job hunting.  
The scraper opens up websites, searches for the word Manchester case insensitive,  
and emails the target if any hits are found.  
If a website cannot be accessed it will email the admin which pages don't work.  
If a runtime exception occurs, the stack trace is emailed to the admin also.  

This is a tiny quickly spun up home-brew project.  
While I normally quite like to use TDD where I can, this is something I designed over a weekend in a hurry.


### Requirements
Before getting into this, you will need to install FireFox and GeckoDriver.  
If you use Linux or WSL, you should be able to run something like:  
`sudo apt install firefox`  
`sudo apt install firefox-geckodriver`  

Ideally you should set up a venv for this project to run inside.  
execute the following commands:  
`python3 -m venv jobsworth`  
`source jobsworth/bin/activate`  
`pip install -r requirements.txt`  

Now when you want to run the project, activate the venv first:  
`source jobsworth/bin/activate`  
then run
`python3 main.py`


### Caveats
Running this in Windows will break because it doesn't follow the Filesystem Hierarchy Standard of using '/' in it's directory structure.
I have only used this on Ubuntu 20.04.6 LTS, your mileage may vary.


### Required files
You must create two json files which are excluded from this repository for privacy purposes.
* `email_addresses.json`
* `passwords.json`

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
