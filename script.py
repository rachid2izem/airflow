import requests
import git

github_username = "izemRachid"
github_token = "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"
repository_name = "airflow"

new_branch = input("Enter the new branch name: ")

session = requests.Session()
session.auth = (github_username, github_token)

repo_url = f"https://api.github.com/repos/{github_username}/{repository_name}"
response = session.get(repo_url)
repo_data = response.json()
print(repo_data)


if "message" in repo_data and repo_data["message"] == "Not Found":
    print(f"Repository '{repository_name}' not found.")
    exit()

contents_url = repo_data["contents_url"].replace("{+path}", "")
response = session.get(contents_url)
contents_data = response.json()


etl_folder = None
dags_folder = None

for item in contents_data:
    if item["type"] == "dir":
        if item["name"] == "ETL":
            etl_folder = item
        elif item["name"] == "dags":
            dags_folder = item


if etl_folder is None and dags_folder is None:
    print("Both 'ETL' and 'dags' folders do not exist.")
else:
    repo = git.Repo.clone_from(repo_data["clone_url"], repository_name)
    repo.git.checkout(new_branch)
    
    if etl_folder:
        etl_folder_path = f"{repository_name}/ETL"
        etl_branch_path = f"{repository_name}/{new_branch}/ETL"
        repo.git.mv(etl_folder_path, etl_branch_path)
    
    if dags_folder:
        dags_folder_path = f"{repository_name}/dags"
        dags_branch_path = f"{repository_name}/{new_branch}/dags"
        repo.git.mv(dags_folder_path, dags_branch_path)

    print(f"Branch '{new_branch}' created/updated with the relevant folders.")
