import json
import os
import re
import requests
from dotenv import load_dotenv
from langchain_ollama import OllamaLLM
from langchain_core.prompts import ChatPromptTemplate
from requests.auth import HTTPBasicAuth

load_dotenv()

API_TOKEN = os.getenv("API_TOKEN")
EMAIL = os.getenv("EMAIL")
WORKSPACE_DOMAIN = os.getenv("WORKSPACE_DOMAIN")
PROJECT_ID = os.getenv("PROJECT_ID")

LLM = OllamaLLM(model="llama3.2")

def create_jira_ticket(project_id, summary, description, issue_type_id):
  url = f"https://{WORKSPACE_DOMAIN}/rest/api/3/issue"
  auth = HTTPBasicAuth(EMAIL, API_TOKEN)
  headers = {
      "Accept": "application/json",
      "Content-Type": "application/json"
  }
  payload = json.dumps({
    "fields": {
      "project": {
        "id": f"{project_id}"
      },
      "summary": summary,
      # "description": description,
      "description": {
        "content": [
          {
            "content": [
              {
                "text": description,
                "type": "text"
              }
            ],
            "type": "paragraph"
          }
        ],
        "type": "doc",
        "version": 1
      },
      "issuetype": {
        "id": f"{issue_type_id}"
      }
    }
  })
  response = requests.post(url, data=payload, headers=headers, auth=auth)
  print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def parse_jira_response(content):

  # Extract Summary (without "Summary: ")
  summary_match = re.search(r"Summary:\s*(.+?)(?=\nDescription:|\n\nDescription:|$)", content, re.DOTALL)
  summary = summary_match.group(1).strip() if summary_match else ""

  # Extract Description (handles same-line or multiline cases)
  description_match = re.search(r"Description:\s*\n*(.+?)(?=\n\nIssue Type:|\nIssue Type:|$)", content, re.DOTALL)
  description = description_match.group(1).strip() if description_match else ""

  # Extract Issue Type (if it exists)
  issue_type_match = re.search(r"Issue Type:\s*\n*(\d+)", content, re.DOTALL)
  issue_type = issue_type_match.group(1) if issue_type_match else "10001"

  return summary, description, issue_type

def generate_jira_content(user_prompt):
  template = (
    "Generate a summary and description for a Jira ticket based on the following user prompt:\n\n"
    "User Prompt: \"{user_prompt}\"\n\n"
    "Please provide:\n"
    "1. Summary: A brief summary (1-2 sentences).\n"
    "2. Description: A detailed description (3-5 sentences) including steps to reproduce, expected outcome, and actual outcome. if it's as bullet points, please newline.\n"
    "3. Issue Type: should be return 10001 for task / 10005 for story /10006 for Bug. Note: task - something that takes minutes to complete, story - something that takes hours to complete, bug - something that is broken.\n"
    "== For example output should be like this:\n"
    "Summary: <summary>\n"
    "Description: <description>\n"
    "Issue Type: 10005"
  )

  formatted_prompt = ChatPromptTemplate.from_template(template).format(user_prompt=user_prompt)
  response = LLM.invoke(formatted_prompt)
  return response

# Input from user
user_prompt = input("Enter your requirement details : ")
response = generate_jira_content(user_prompt)
print(response)

# Parse the content
summary, description, issue_type = parse_jira_response(response)
print('======================= start summary =======================')
print(summary)
print('======================= start description =======================')
print(description)
print('======================= start issue_type =======================')
print(issue_type)


# Create the jira ticket
create_jira_ticket(PROJECT_ID, summary, description, issue_type)