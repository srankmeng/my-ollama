import json
import os
import requests
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from requests.auth import HTTPBasicAuth

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
EMAIL = os.getenv("EMAIL")
WORKSPACE_DOMAIN = os.getenv("WORKSPACE_DOMAIN")
SPACE_ID = os.getenv("SPACE_ID")

LLM = OllamaLLM(model="llama3.2")

def create_confluence_page(title, description, body):
  url = f"https://{WORKSPACE_DOMAIN}/wiki/api/v2/pages"
  auth = HTTPBasicAuth(EMAIL, API_TOKEN)
  headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
  }

  confluence_body = f"<h2>{description}</h2><div>{body}</div>"
    
  payload = json.dumps({
    "spaceId": SPACE_ID, 
    "status": "current",
    "title": title,
    "parentId": "",
    "body": {
        "representation": "storage",
        "value": confluence_body
    }
  })

  response = requests.post(url, data=payload, headers=headers, auth=auth)
  print(json.dumps(response.json(), sort_keys=True, indent=4, separators=(",", ": ")))

def parse_response(response):
  lines = response.splitlines()
  title = lines[0].strip()
  description = lines[1].strip()
  body = "\n".join(lines[2:]).strip()
  return title, description, body

def generate_content(user_prompt):
  template = (
    "You are a senior software architect at a technology company. You have just received a feature request for {user_prompt}. "
    "Your task is to perform a detailed analysis on this request, considering its technical feasibility, architectural impact, and potential risks. "
    "You will evaluate the following aspects:\n\n" 
    "High-Level Overview: Provide a summary of the feature and its business value.\n"
    "Architectural Impact: Analyze the impact of the feature on the architecture of the system.\n"
    "API Design (if needed): show me api design, api specification, what is the input (include data type, mandatory) and output, error code, validation rule, And example data in section name \"example data\".\n"
    "Database Design(if needed): please show me entity column name, data type, primary key, foreign key in table view, And example data in section name \"example data\".\n"
    "Finally, conclusions all the above, write it in the format of a Confluence page, using appropriate headers and sections to structure the information clearly. include code block, header text, bold text, table, etcs. As markdown format."
  )

  formatted_prompt = ChatPromptTemplate.from_template(template).format(user_prompt=user_prompt)
  response = LLM.invoke(formatted_prompt)
  return response

# Input from user
user_prompt = input("Enter your request feature : ")
response = generate_content(user_prompt)
# print(response)

# Parse the generated content
title, description, body = parse_response(response)

# Create the Confluence page
create_confluence_page(title, description, body)