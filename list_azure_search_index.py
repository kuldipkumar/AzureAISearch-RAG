import requests

# Your Azure Cognitive Search details
endpoint = "YOUR_COGNITIVE_SEARCH_END_POINT"
api_key = "YOUR_COGNITIVE_SEARCH_API_KEY"

# Construct the URL for listing indexes
url = f"{endpoint}/indexes?api-version=2021-04-30-Preview"

# Set up the headers with the API key
headers = {
    "Content-Type": "application/json",
    "api-key": api_key
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    indexes = response.json()["value"]
    
    # Print the names of all indexes
    print("Available indexes:")
    for index in indexes:
        print(f"- {index['name']}")
else:
    print(f"Failed to retrieve indexes. Status code: {response.status_code}")
    print(f"Response: {response.text}")
