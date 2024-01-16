# 2024 AI Hackathon Risk Word Cloud 
This is a proof of concept for the data fetching side of generating a wordcloud from 
accessment response comments. 


# Installation
Ensure you have python3 and pip3 installed.

To install all the python dependencies, run:
`pip3 install -r ./requirements.txt`

Create a .env file in the project root and populate the following:
```
OAI_ENDPOINT="https://testonlygpt4.openai.azure.com/"
OAI_API_KEY="<api key>"
OAI_DEPLOYMENT="gpt-4-model-test"

OAI_SEARCH_ENDPOINT="https://hack24search.search.windows.net"
OAI_SEARCH_KEY="<search key>"
OAI_SEARCH_IDX="wordcloud-idx5"
```
Ask Blaine for environment vars if needed. 


# Populating Data
We need to convert the assessment response data into a narrative format that openAI can understand. To do so, we connect to the ADA database to fetch the denormalized response data, lightly process, and dump into `sample_data.txt`. This then needs to be uploaded to the Azure Open AI index for indexing and consumption. 

```Protip: To avoid caching of the index, create a new index for each upload. ```

To generate a new set of data, run:
`python3 read_db.py`

Uploading to index
- Then navigate to: https://oai.azure.com/portal/d45b0d2dff6045c58e955797eef72859/chat?tenantid=bdac6543-2671-43d9-9ffe-8b61e08ab18a
- Click on the [Add your own data] tab. If there is an existing datasource, remove it.
- Then upload the newly generated sample_data.txt file and follow the screen prompts. Give the index a new name like `wordcloud-idx6` and update the `OAI_SEARCH_IDX` environment variable as needed.


# Populating Data
Generating the wordclouds. At the moment, word clouds are generated for each unique question/variable within the various risk assessment surveys. The current test data has 4. For each of these, you will need to uncomment the cooresponding lines in `prompt_histogram.py` and run: `python3 prompt_histogram.py`. The histogram json should output to the screen.
