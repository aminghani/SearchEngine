import os
from together import Together
from SearchEngine.utils.utils import extract_numbers
client = Together(api_key=os.environ.get("TOGETHER_API_KEY"))

def portion(query, limit):
    response = client.chat.completions.create(
            model="mistralai/Mistral-7B-Instruct-v0.3",
            messages=[{"role": "user", "content": "I am going to give you some user search query, you should determine "+
               "how many of the result should be retrieved from semantic database and how many of them should be "+
               "retrieved from keyword database, and sum of the two should be equal to some number which is also given."+
               "also not that your first output should indicate semantic database output and the second number is "+
               "output for keyword database. please keep your anwer to just numbers and do not say more that two numbers. "+
               "avoid any further explanation. your output should contain one (), one number in start, one comma "+
               "and one number after that, like this: (2, 6). "
               "example 1: query: I need a dress for a summer wedding that is elegant and lightweight. "+
               "limit: 10, output:(8, 2) "+
               "example 2: blue denim jacket. "+
               "limit: 8, output:(3, 5) "+
               f"now, answer this query: {query} "+
               f"limit: {limit}, output:"}],)
    output = response.choices[0].message.content
    output = output.replace(" ", "")
    return extract_numbers(output)
