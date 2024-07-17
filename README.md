# About serp_api_extractor

This repository provides an end to end API pipeline for SerpAPI that provides a dataframe containing results for each specified keyword that is mentioned.

As this is a solution for modern day businesses with multiple brands, the solution also includes other indicative parameters in the final output which are not derived from the API itself.


## About use

- The repo contains and .env varibale that stores the key of the API.


- The repo contains a json_config.csv file in which the user can add the parameters and keywords that they want to monitor when the API makes a call.


- The solution receives a dictionary containing the result of the search for a specific keyword (along with other parameters). Then it searches for the URL of the website we are trying to monitor for and retains only that.

## Get started

```bash
git clone git@github.com:pettpavlious/serpAPI_keyword_monitor.git
cd serpAPI_keyword_monitor
```

### Step one: Add your key in the .env file

### Step two: Install all necessary packages

```bash
pip install -r requirement.txt
```
### Step three: Configure all parameters in json_config.csv

- The json_config.csv contains extra parameters that are not necessary for the API, but can be useful. Feel free to remove or make any changes if they are unnecessary.

### Step four: Run the serp_api_run.py
```bash
python serp_api_run.py 
```

- In case that the API returns no results for a keyword then the row of said keyword will contain 0 as the position along with the outputs of the API.

## Logs

The script runs in two phases. You can check the logs each time you run the script to identify where the output stopped and what issue might require attention.
