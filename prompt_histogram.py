##############################################################################
# Interface to get a histogram of comment words by question.
# Note: A question is specific to a assessment template and not universal.
# However, for brevity, I'm utilizing the questions as-is in the test data.
# 
# To run this, uncomment out the question you would like the histogram for
# and run python3 prompt_histogram.py
# Histogram data will be logged to the console.
##############################################################################
import os
import openai
import json
from dotenv import load_dotenv

# Bootstrap environement vars
load_dotenv()

endpoint = os.environ['OAI_ENDPOINT']
api_key = os.environ['OAI_API_KEY']
deployment = os.environ['OAI_DEPLOYMENT']


# Azure AI Search setup
search_endpoint = os.environ['OAI_SEARCH_ENDPOINT']
search_key = os.environ['OAI_SEARCH_KEY']
search_index_name = os.environ['OAI_SEARCH_IDX']

# Construct the client
client = openai.AzureOpenAI(
    base_url=f"{endpoint}/openai/deployments/{deployment}/extensions",
    api_key=api_key,
    api_version="2023-08-01-preview",
)

# Generic prompt helper
def ask(prompt):
    completion = client.chat.completions.create(
        model=deployment,
        response_format={ "type": "json" },
        messages=[
            # {
            #     "role": "assistant",
            #     "content": "Risk assessments contain responses. There are several different categories of responses including \"Residual Risk\", \"Inherent Risk Rating\", \"Average Impact Score\".",
            # },

            {
                "role": "user",
                "content": prompt,
            },
        ],
        extra_body={
            "dataSources": [
                {
                    "type": "AzureCognitiveSearch",
                    "parameters": {
                        "endpoint": search_endpoint,
                        "key": search_key,
                        "indexName": search_index_name
                    }
                }
            ]
        }
    )

    # print(completion.model_dump_json(indent=2))
    return completion.choices[0].message.content.replace('```json\n', '').replace('[doc1]', '').replace('```', '')


# Helper to ask questions and get scores
def ask_with_comment_score(prompt):
    return ask("%s. Please give result in json array in the format like \{comment: [the comment], value: value\}. Don't say other things." % (prompt))


# Generate a histogram of common words used in comments for a specific template variable ("question")
def ask_histogram(type):
    #return ask("Please generate a histogram of words and how frequently they are used in comments for responses for the question \"%s\". Return the result in a json object in the format \{word: frequency\}. Please exclude common english language words. Please only return the json object." % (type)) # works
    return ask("What are some words that are used in response comments for responses to the question \"%s\". Return the result in a json object in the format \{word: frequency\}. Please exclude common english language words. Please only return the json object." % (type)) # works
    #return ask("Please generate a histogram of words and how frequently they are used in comments for responses for the question titled \"%s\". Return the result in a json object in the format \{word: frequency\}. Please exclude common english language words. Please only return the json object." % (type)) # works
    #return ask("Please generate a histogram of words frequently used in comments to the survey question \"%s\". Return the result in a json object in the format \{word: frequency\}. Please exclude common english language words. Please only return the json object." % (type)) # kinda works...
    #return ask("Please generate a histogram of words frequently used in comments to the survey question \"%s\". Return the result in a json object in the format \{word: frequency\}. Please exclude common english language words. Please only return the json object." % (type))

################################################
# Uncomment these to run them - they all should work
################################################
#resp = ask_histogram("Inherent Risk Rating")
#resp = ask_histogram("Average Impact Score")
#resp = ask_histogram("Residual Risk") #bad...
resp = ask_histogram("Overall Materiality")


################################################
# These don't rally work
################################################
#resp = ask("Create an json array of unique survey questions. Please only return the json.")
# resp = ask("For each of the unique survey questions, classify the overall sentiment from the comments on a scale of \"negative\", \"mixed\", \"positive\". Please return the results in a json object grouped by the question.")
# resp = ask("For each of the unique survey questions, classify the overall sentiment for that question from the comments. Use a scale of \"negative\", \"mixed\", \"positive\" to classify the sentiment. Please return the results in a json object in the format of \{question: classification\}")
# resp = ask("For each of the unique survey questions, classify the overall sentiment from the comments on a scale of \"negative\", \"mixed\", \"positive\". Please return the results in a json object grouped by the question and the classified sentiment along with a score of how confident you are in the classification.")


print('---------')
print(resp)
print('---------')
data = json.loads(resp)
print(json.dumps(data, indent=4))
