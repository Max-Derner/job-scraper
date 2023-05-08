## job-scraper
A tiny job scraping project for automating job hunting.  
The scraper opens up websites, searches for the word Manchester (case insensitive),  
and emails the target if any hits are found.  
Specific lines of returned content may be ignored, for example if it is common to see the first line as  
"No hits relating to Manchester"  
If a website cannot be accessed it will email the admin which pages don't work.  
If a runtime exception occurs, the stack trace is emailed to the admin also.  

This is a tiny quickly spun up home-brew project.  
While I normally quite like to use TDD where I can, this is something I designed over a couple of weekends in a hurry.  


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


### Automation
This project includes a small bash script called auto_update_and_run.sh.  
This allows me to set the project on a spare machine with a cronjob pointed directly at the shell script.  
This script in turn:  
* Pulls the most recent changes (e.g. adding new websites to scrape)  
* Activates the Python venv  
* Runs the program  
* Deactivates the Python venv  


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
