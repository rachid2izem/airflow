import requests
import git

# GitHub repository details
github_username = "your_username"
github_token = "your_token"
repository_name = "your_repository"

# Get the new branch name from user
new_branch = input("Enter the new branch name: ")

# Connect to GitHub and authenticate
session = requests.Session()
session.auth = (github_username, github_token)

# Get repository information
repo_url = f"https://api.github.com/repos/{github_username}/{repository_name}"
response = session.get(repo_url)
repo_data = response.json()

# Check if the repository exists
if "message" in repo_data and repo_data["message"] == "Not Found":
    print(f"Repository '{repository_name}' not found.")
    exit()

# Get the list of contents in the repository
contents_url = repo_data["contents_url"].replace("{+path}", "")
response = session.get(contents_url)
contents_data = response.json()

# Check if 'ETL' and 'query' folders exist
etl_folder = None
query_folder = None

for item in contents_data:
    if item["type"] == "dir":
        if item["name"] == "ETL":
            etl_folder = item
        elif item["name"] == "query":
            query_folder = item

# Create or update the branch folder
if etl_folder is None and query_folder is None:
    print("Both 'ETL' and 'query' folders do not exist.")
else:
    repo = git.Repo.clone_from(repo_data["clone_url"], repository_name)
    repo.git.checkout(new_branch)
    
    if etl_folder:
        etl_folder_path = f"{repository_name}/ETL"
        etl_branch_path = f"{repository_name}/{new_branch}/ETL"
        git.Repo.rename(etl_folder_path, etl_branch_path)
    
    if query_folder:
        query_folder_path = f"{repository_name}/query"
        query_branch_path = f"{repository_name}/{new_branch}/query"
        git.Repo.rename(query_folder_path, query_branch_path)

    print(f"Branch '{new_branch}' created/updated with the relevant folders.")
