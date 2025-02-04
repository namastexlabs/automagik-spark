Workflow Source Management
A workflow source represents a connection to a LangFlow instance
Sources are uniquely identified by their URL
When adding a source with an existing URL, we update the existing source rather than creating a new one
Each source stores:
URL (unique identifier)
API Key (encrypted)
Version info (from /api/v1/version endpoint)
Status
Creation/Update timestamps
API Key Encryption
We need proper encryption since this is a public repo
Use an encryption key from settings to encrypt/decrypt API keys
The encryption should be reversible but secure
ID Management
Two types of IDs to handle:
Internal workflow ID (our database primary key)
Source ID (used to build URLs for API calls)
Need to consider whether to use the source's target ID as the table ID
Version Management
Need to add functionality to fetch version info from /api/v1/version
Store this information with the source
Should be updated when source is created/updated
Workflow-Source Relationship
Each workflow has exactly one source
The source provides:
Base URL for API calls
API key for authentication
Version information
Additional workflow info is used to construct specific API calls
Let me validate the API endpoints with the provided credentials:

Ran terminal command
\root\automagik

> curl -H "Authorization: Bearer sk-i1we1SGAEnEggEFryIYF0WcvO3Sd9yvW05z9ls39Rx4" http://lf-cezar.namastex.io/api/v1/version

Output
CopyInsert
{"version":"1.1.1.dev22","main_version":"1.1.1","package":"Langflow Nightly"}
Exit Code 0