import pandas as pd
import matplotlib.pyplot as plt
import openai
import sys
import os
import io
from dotenv import load_dotenv

load_dotenv()

data = pd.read_excel('data/sample_data.xlsx')

ai_key = os.getenv("GENAI_KEY")

client = openai.OpenAI(
    base_url="https://api.genai.mil/v1",
    api_key=ai_key
)

capture_info = io.StringIO()
data.info(buf=capture_info)

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

Make sure your response can be executed as python code, without removing any characters or cleaning. Do not include any markdown formatting or backticks such as ```python ```.
"""

response = client.chat.completions.create(
    model="gemini-2.5-flash",
    messages=[
        {"role": "user", "content": message}
    ],
    n=5,
    temperature=0.1,
    prompt_cache_key=None
)

valid = -1
for i in range (5):
    try:
        exec(response.choices[i].message.content)
        valid = i
        break
    except:
        continue

if valid == -1:
    print("\n\n\n\nNo response from AI valid\n\n\n\n")
    exit(0)

with open("ai_output.py", "w") as f:
    f.write(
f"""
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_excel('data/sample_data.xlsx')

{response.choices[valid].message.content}
""")
