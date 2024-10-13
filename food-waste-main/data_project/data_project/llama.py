import ollama
from image_processing import extracted_text

model = 'llama3.1'

prompt = '''
I have this image of a receipt in String format 
Please tell me the index where the items of the receipt start to get listed and where they stop being listed in the string that I have given you. I don't want any explanation, just the start and end index seperated by a space inbetween. It  The String for the receipt is as follows
''' + extracted_text

stream = ollama.chat(
    model=model,
    messages=[{'role':'user', 'content':prompt}], 
    stream = True
)

reply = ""

for chunk in stream:
    reply += chunk['message']['content']
    

prompt = """
The start and end indices are given. Please tell me what the item names are as listed between these indices, and DO NOT include any other text, headers or introductions whatsover. Remove the item code and the items numbers. The start and end indices are as follows
""" + reply + "This is the list" + extracted_text

stream = ollama.chat(
    model=model,
    messages=[{'role':'user', 'content':prompt}], 
    stream = True
)

items_array = []
var = ""

for chunk in stream:
    if len(chunk['message']['content']) == 0 or chunk['message']['content'] == "\nGV":
        items_array.append(var)
        var = ""
    else:
        var += chunk['message']['content']

cleaned_array = items_array[0].split('\n')

allItemsString = ""

for i in cleaned_array:
    allItemsString = allItemsString+str(i)

itemVar = "Great Value Peanut Butter"

prompt = """
This is a list of the items given below, check if
""" + itemVar + "exists in the array given. Interpret the abbreviations given for the items and ignore the other text. If there is a match, return true and if not, return false. DO NOT type anything else. This is the array" + allItemsString

stream = ollama.chat(
    model=model,
    messages=[{'role':'user', 'content':prompt}], 
    stream = True
)
boolean = "0"
for chunk in stream:
    boolean = str(chunk['message']['content'])
