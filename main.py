import os
import re
import subprocess
from jira import JIRA
import requests

JIRA_SERVER = os.environ.get("JIRA_SERVER")
JIRA_API_TOKEN = os.environ.get("JIRA_API_TOKEN")
JQL_QUERY = os.environ.get("JQL_QUERY")
RELEASE_BRANCH = os.environ.get("RELEASE_BRANCH", "develop")
GITHUB_REPOSITORY = os.environ.get("GITHUB_REPOSITORY")
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_API_ACCEPT_HEADER = "application/vnd.github+json"
jira = JIRA(server=JIRA_SERVER, token_auth=JIRA_API_TOKEN)

def _filter_branches_by_jira_task_key(branches, jira_tasks):
    """
    Filters a list of branches to include only those that contain a Jira task key.

    Args:
        branches (list): A list of branch names.
        jira_tasks (list): A list of Jira task dictionaries, each containing a 'key' field.

    Returns:
        list: A list of branch names that contain at least one Jira task key.
    """
    filtered_branches = []
    for branch in branches:
        for task in jira_tasks:
            if task["key"] in branch:
                filtered_branches.append(branch)
    return filtered_branches

def run_command(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {command}")
        print(f"Return code: {result.returncode}")
        print(f"Stdout: {result.stdout}")
        print(f"Stderr: {result.stderr}")
    return result

def search_jira(jql_query):
    try:
        issues = jira.search_issues(jql_query)
        return issues
    except requests.exceptions.RequestException as e:
        print(f"Network error occurred during Jira search: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred during Jira search: {e}")
        return []

def find_last_release_branch():
    command = "git branch -r --sort=-committerdate"
    result = run_command(command)
    branches = [
        branch.strip().replace("origin/", "")
        for branch in result.stdout.splitlines()
        if "->" not in branch
    ]
    for branch in branches:
        if re.match(RELEASE_BRANCH, branch):
            return branch
    return None

def _get_last_release_branch():
    last_release_brach = find_last_release_branch()
    if not last_release_brach:
        print("No release branch found.")
        exit(1)
    return last_release_brach

def _get_unmerged_branches(last_release_brach):
    command = f"git branch -r --no-merged {last_release_brach}"
    result = run_command(command)
    branches = [
        branch.strip().replace("remotes/origin/", "")
        for branch in result.stdout.splitlines()
        if "->" not in branch
    ]
    return branches

def get_no_merged_branches():
    last_release_brach = _get_last_release_branch()
    branches = _get_unmerged_branches(last_release_brach)
    return branches

if __name__ == "__main__":
    no_merged_branches = get_no_merged_branches()
    jira_tasks = search_jira(JQL_QUERY)
    normalized_branches = _filter_branches_by_jira_task_key(no_merged_branches, jira_tasks)

    if not GITHUB_REPOSITORY:
        print("GITHUB_REPOSITORY environment variable not found.")
        exit(1)

    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN environment variable not found.")
        exit(1)

    owner, repo = GITHUB_REPOSITORY.split("/")

    for branch in normalized_branches:
        issue_title = "Merge request for {}".format(branch)
        issue_body = "Please merge branch {} into the release branch.".format(branch)
        github_api_url = "https://api.github.com/repos/{}/{}/issues".format(owner, repo)
        headers = {
            "Authorization": "Bearer {}".format(GITHUB_TOKEN),
            "Accept": GITHUB_API_ACCEPT_HEADER,
        }
        data = {"title": issue_title, "body": issue_body, "labels": ["merge-request"]}
        response = requests.post(github_api_url, headers=headers, json=data)

        if response.status_code == 201:
            print(f"Issue created for {branch}: {response.json()['html_url']}")
        else:
            print(f"Failed to create issue for {branch}: {response.content}")
