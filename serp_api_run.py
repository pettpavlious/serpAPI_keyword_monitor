import pandas as pd
from dotenv import load_dotenv
import os
from serpapi import GoogleSearch
#import serpapi
import pendulum
import pandas as pd
import json
from datetime import date

load_dotenv()
api_key = os.getenv('API_PASSWORD')

def write_file(file_name, file_contents):

    header_value = False

    if os.path.isfile(file_name):

        header_value = False

    else:

        header_value = True

    file_contents.to_csv(file_name, mode="a", encoding="utf-8", index=False, header=header_value)


def log_status(level,job_status, row_count, create_file=0):

    log_columns = [

        "log_timestamp",
        "log_date",
        "level",
        "job_status",
        "row_count"
    ]

    if create_file == 0:

        log_data = [
            pendulum.now().to_datetime_string(),
            pendulum.now().to_date_string(),
            level,
            job_status,
            row_count

        ]

        log_result = pd.DataFrame([log_data], columns=log_columns)

    elif create_file == 1:

        log_result = pd.DataFrame(columns=log_columns)

    write_file("serpapi_log.csv", log_result)



class CSVToJson:
    def __init__(self, csv_file, api_key):
        self.csv_file = csv_file
        self.api_key= api_key

    def csv_to_json(self):
        level = "CSV_JSON"
        # Read the CSV data
        df = pd.read_csv(self.csv_file)
        row_count = len(df)

        # Prepare the data for the JSON format
        self.data = {}
        for i, row in df.iterrows():
            self.data[f'searchApiCall{i+1}'] = {
                'url': 'https://api.example.com/search',
                'method': 'GET',
                'headers': {
                    'Content-Type': 'application/json'
                },
                'params': {
                    'api_key': self.api_key,
                    'q': row['Keyword'],
                    'hl': row['Language'],
                    'gl': row['Country'],
                    'google_domain': row['Google Domain'],
                    'location': row['Location'],
                    'filter': row['Filter'],
                    'device': row['Device'],
                    'num': '10'
                },
                'search_link': row['Domain'],
                'brand': row['Brand'],
            }
        log_status(level, "Success", row_count)
        return self.data 
    

class SearchAPI:
    def __init__(self, json_input):
        self.data=json_input
        self.results_list = []

    def make_api_calls_and_get_results(self):
        level = "API_CALL"
        success = True
        self.results_list = []
        common_columns = ['position', 'title', 'link', 'redirect_link', 'displayed_link', 'favicon', 'snippet', 'source', 'Search Query', 'Date', 'Market', 'Brand']
        for api_call in self.data.values():
            try:
                search = GoogleSearch(api_call['params'])
                results = search.get_dict()
                if 'organic_results' in results:
                    organic_results = results['organic_results']
                    filtered_results = [result for result in organic_results if api_call['search_link'] in result.get('link', '')]
                    if not filtered_results:
                        api_call['params']['num'] = '100'
                        search = GoogleSearch(api_call['params'])
                        results = search.get_dict()
                        if 'organic_results' in results:
                            organic_results = results['organic_results']
                            filtered_results = [result for result in organic_results if api_call['search_link'] in result.get('link', '')]
                        if not filtered_results:
                            empty_result = {
                                'position': 0, 'title': '0', 'link': '0', 'redirect_link': '0', 
                                'displayed_link': '0', 'favicon': '0', 'snippet': '0', 'source': '0',
                                'Search Query': api_call['params']['q'], 'Date': pd.to_datetime('today').date(),
                                'Market': api_call['params']['location'], 'Brand': api_call['brand']
                            }
                            self.results_list.append(pd.DataFrame([empty_result]))
                    if filtered_results:
                        result_df = pd.DataFrame([filtered_results[0]])
                        result_df['Search Query'] = api_call['params']['q']  # Add the 'q' column
                        result_df['Date'] = pd.to_datetime('today').date()
                        result_df['Market'] = api_call['params']['location']
                        result_df['Brand'] = api_call['brand']
                        result_df = result_df[[col for col in common_columns if col in result_df.columns]]
                        self.results_list.append(result_df)
            except Exception as e:
                success = False

        if self.results_list:
            df=pd.concat(self.results_list,ignore_index=True)
            row_count=len(df)
        else:
            df=pd.DataFrame()
            row_count=0
        
        # Log the final status of the process
        status = "Success" if success else "Failure"
        log_status(level, status, row_count)
        return df
    
def call_api():
    # Use the class
    converter = CSVToJson('json_config.csv', api_key)
    json_data=converter.csv_to_json()

    api_call = SearchAPI(json_data)
    df = api_call.make_api_calls_and_get_results()
    write_file("output.csv", df)

call_api()