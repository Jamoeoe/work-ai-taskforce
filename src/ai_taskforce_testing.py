import pandas as pd
import matplotlib.pyplot as plt
import openai
import sys
import os
import io
from dotenv import load_dotenv

data_files = os.listdir("data")
data = pd.read_excel(f"data/{data_files[0]}")
capture_info = io.StringIO()
data.info(buf=capture_info)

if os.path.exists(".env"):
    load_dotenv()

client = openai.OpenAI(
    base_url="https://api.genai.mil/v1",
    api_key=os.getenv("GENAI_KEY")
)

message = f"""
I have this Python {sys.version[:6]} code:

**Code start**
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data/sample_data.xlsx')

#INSERT YOUR CODE HERE

**Code end**

Here is what data.to_string() looks like:
{data.to_string()}

Here is what data.info() looks like:
{capture_info.getvalue()}

Show me the code I need to insert at the comment to do the following: 
1. Print the 3 most critical take aways from the data.
2. Create and show visualizations of the 3 most critical take aways using plt. 
I like when the titles of my graphs are spaced out from the graph itself so it doesn't overlap. 

When relevant, consider multi factor interactions in the data.

Make sure your response can be executed as python code, without removing any characters or cleaning. Do not include any markdown formatting or backticks such as ```python ```.
"""

n = 5 # the number of responses per prompt, increasing this reduces the chance of a failed run 1-%f^n
response = client.chat.completions.create(
    model="gemini-3.5-flash", # in testing this model performs best of all available
    messages=[
        {"role": "user", "content": message}
    ],
    n=n,
    temperature=2, # determines how creative the model is with the response, turn up to make it more creative, but increases failure rate
    prompt_cache_key=None # makes it so the api won't remember previous runs
)

valid = -1
for choice in range (n):
    try:
        exec(response.choices[choice].message.content) # ai generated variables can leak into this namespace
        valid = choice
        break
    except:
        continue

if valid == -1:
    print("\n\n\n\nNo response from AI valid\n\n\n\n")
    exit(0)

with open("src/ai_output.py", "w") as f:
    f.write(
f"""
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data/sample_data.xlsx')

{response.choices[valid].message.content}
""")
