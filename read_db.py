# File to read the data
# Note this uses the ADA sync database not the application database. This is so data is denormaized and easier to work with.
import psycopg2
from psycopg2.extras import RealDictCursor
import random

DATA_FILE = './sample_data.txt'

# Connect to DB
ADA_DB_NAME = 'pbi' # I named this "pbi" locally, switch to whatever you are using...
conn = psycopg2.connect(database = ADA_DB_NAME, user = "", host= 'localhost', password = "", port = 5432)
cur  = conn.cursor()
cur = conn.cursor(cursor_factory=RealDictCursor) #DictCursor

# Fetch Assessment Responses
# cur.execute("""SELECT row_to_json(row) FROM (SELECT * FROM assessment_responses) row LIMIT 2""")
cur.execute("""SELECT * FROM assessment_responses 
                WHERE 
                    assignee_user IS NOT NULL AND 
                    is_calculated IS NOT NULL AND
                    rating_label IS NOT NULL
                ORDER BY created_at DESC 
                LIMIT 1000
            """)
rows = cur.fetchall()

# Make the changes to the database persistent
conn.commit()
# Close cursor and communication with the database
cur.close()
conn.close()

output = ''
grouped_responses = {}

for row in rows:
    responses_id = row["assessment_response_id"]
    if not grouped_responses.get(responses_id, False):
        grouped_responses[responses_id] = [row]
    else:
        grouped_responses[responses_id].append(row)


random_comments = [
    "We're doing great. This risk is a non issue",
    "This risk is critical",
    "We're doing ok. We shoud look at this.",
    "This flew under the radar",
    "This needs to be addressed right away",
    "This is critical",
    "This could have major impact on our next quarter goals.",
    "This could ruin our business",
    "This risk is totally mitigated.",
    "Nothing to see here",
    "Accounting will need to look at this more later",
    "These numbers do not make sense",
    "We are aware of fraud",
    "We are not aware of fraud",
    "Everything is great"
]

negative_comments = [
    "We are aware of fraud",
    "This could ruin our business",
    "We're doing this wrong.",
    "This is critical",
]

def get_random_comment(type):
    if (type == 'Overall Materiality'):
        return random.choice(negative_comments)
    return random.choice(random_comments)


with open(DATA_FILE, "w") as f:
    for response_id in grouped_responses.keys():
        print(response_id)
        a_story = '' # for this specific assessment
        r1 = grouped_responses[response_id][0]

        print(r1['assignee_user'])
        # Figure out the user
        userstr = 'An unknown user'
        if r1['assignee_user']:
            userstr = 'User %s' % (r1['assignee_user'])


        a_story = '\n\n%s %s their %s assement survey for the "%s" assessment on %s. The source of this assessment was an %s.' % (userstr, r1['user_assessment_status'], r1['assessable_type'], r1['assessment'], r1['finalized_date'], r1['source'])

        for r in grouped_responses[response_id]:
            #a_story += '\nThey gave a score of %s ("%s") for "%s" with the comment "%s".' % (r['value'], r['rating_label'], r['criteria_label'], random.choice(random_comments))
            a_story += '\nThey responsed to the survey question "%s" with a score of %s ("%s") with the comment "%s".' % (r['criteria_label'], r['value'], r['rating_label'], get_random_comment(r['criteria_label']))

        f.write("%s\n\n" % (a_story))

print('%s assessments written to %s. Have an awesome day.' % (len(grouped_responses.keys()), DATA_FILE))