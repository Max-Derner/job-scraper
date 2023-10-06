# **job-scraper**
A tiny job scraping project for automating job hunting.  
The scraper opens up websites, searches for the word Manchester (case insensitive),  
and emails the target if any hits are found.  
Specific lines of returned content may be ignored, for example if it is common to see the first line as  
"No hits relating to Manchester"  
If a website cannot be accessed it will email the admin which pages don't work.  
If a runtime exception occurs, the stack trace is emailed to the admin also.  

This is a tiny quickly spun up home-brew project.  
While I normally quite like to use TDD where I can, this is something I designed over a couple of weekends in a hurry and then added to as time went by. I am now looking to add some tests for it.  


### **Requirements**
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

To leave the venv, simply enter the command:  
`deactivate`  

The security scanning requires a different set of tools not typically distributed in linux distros by default.
You will need both Syft and Grype, produced by Anchore:  
* Syft: https://github.com/anchore/syft#readme  
* Grype: https://github.com/anchore/grype#readme  

Both of those pages contain instructions on how to install.  
For some of the formatting which my bash scripts run, you will also need to install jq, this should be as simple as:  
`sudo apt install jq`

### **Caveats**
Running this in Windows will break because it doesn't follow the Filesystem Hierarchy Standard of using '/' in it's directory structure.  
I have only used this on Ubuntu 20.04.6 LTS, so your mileage may vary.  

### **Required files**
You must create two json files which are excluded from this repository for privacy purposes.  
* `json_files/email_addresses.json`  
* `json_files/passwords.json`  

passwords.json is structured as such:  
```
{  
    "APP_PASSWORD": "fill this in with a proper app password"  
}  
```

email_addresses.json is structured as such:  
```
{  
    "ADMIN": "your email address",  
    "TARGET": "person who gets emailed about jobs",  
    "ROBOT": "email address you have app password for"  
}  
```

### **Security Scanning**
In order to perform the vulnerability scanning you simply need to be in the root directory, then you run the following command:  
`./vulnerability_scanning/vulnerability_scanner.sh`  
Should you have any issues, try running it in a bash sub-shell.  
This will run Syft to produce an SBOM, then run Grype to scan the SBOM, and finally it will parse the output and formulate a tabular output for you.
There is indeed a table output option for Grype but I wanted to recreate it in Bash just to show off.


## **Testing**
Test exist for the following modules:
* futils (file-utils)
* fileio (file input output)
* context_handlers
* web_scraper


## **Automation**
Should you wish to automate the webscraper, you can target the file `run_target.sh` with a cron job.
