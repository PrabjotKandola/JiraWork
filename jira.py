import requests
import base64

# Jira Configuration
jira_base_url = "https://www.jlpit.com/jira/rest/api/2"
jira_username = "j84568798" # You're username
jira_api_token = ""  # Your API token

# Set up headers
auth_str = base64.b64encode(bytes(f"{jira_username}:{jira_api_token}", "utf-8")).decode("ascii")


headers = {
    "Authorization": f"Basic {auth_str}",
    "Content-Type": "application/json",
}

def check_for_name(issue_key, name):
    issue_url = f"{jira_base_url}/issue/{issue_key}?expand=changelog"
    response = requests.get(issue_url, headers=headers)
    response.raise_for_status()

    changelog = response.json()["changelog"]["histories"]
    for history in changelog:
        if history["author"]["displayName"] == name:
            return True
    return False

jql_query = "project = JMST"
search_url = f"{jira_base_url}/search?jql={jql_query}"

try:
    response = requests.get(search_url, headers=headers)
    response.raise_for_status()

    joseph_tickets = []
    uppendra_tickets = []

    issues = response.json()["issues"]
    for issue in issues:
        if check_for_name(issue["key"], "Joseph"):
            joseph_tickets.append(issue["key"])
        if check_for_name(issue["key"], "Uppendra"):
            uppendra_tickets.append(issue["key"])

    # Print results
    print("Tickets associated with Joseph:")
    for ticket in joseph_tickets:
        print(ticket)

    print("\nTickets associated with Uppendra:")
    for ticket in uppendra_tickets:
        print(ticket)

except requests.RequestException as e:
    print(f"Failed to retrieve issues. Error: {e}")
