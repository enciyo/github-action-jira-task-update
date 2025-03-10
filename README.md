# Jira Task Is Updated?

This GitHub Action searches for tasks in Jira using a JQL query, compares the results with GitHub branches, checks if the results are merged with release branches, and opens a Jira issue if not.

## Introduction

This GitHub Action is used to synchronize the status of tasks in Jira with GitHub branches. It searches in Jira based on a specific JQL query, checks whether the found tasks are merged with release branches, and automatically opens an issue in Jira if necessary.

## Workflow

This action follows these steps:

1.  **Connect to Jira:** Connects to Jira with the provided Jira server URL and API token.
2.  **Execute JQL Query:** Executes the specified JQL query in Jira and retrieves the results.
3.  **Compare Branches:** Compares the GitHub branches associated with the found Jira tasks.
4.  **Merge Check:** Checks whether the branches are merged with release branches.
5.  **Open Jira Issue:** If a task is not merged with release branches, it automatically opens an issue in Jira.

## Description

This action connects to the Jira server, runs the specified JQL query, and allows you to use the results in your GitHub Actions workflow.

## Usage

### Prerequisites

*   You need to have a Jira account.
*   You need to have a Jira API token.
*   You need to have a GitHub Actions workflow.

### Setup

1.  Add this action to your GitHub Actions workflow.
2.  Configure the following input parameters:

    *   `jira_server`: Jira server URL. Example: `https://jira.example.com` (required).
    *   `jira_api_token`: Jira API token. You can create one from your Jira account (required).
    *   `jql_query`: JQL query to use to search in Jira. Example: `'project = MYPROJECT AND status = "In Progress"'` (required).
    *   `release_branch`: Regex that defines release branches. Example: `'release/.*'` (required).

### Jira Issue Creation

This action can automatically open a Jira issue if a Jira task is not merged with release branches. This feature is useful for tracking release processes and quickly reporting errors. The opened issue indicates that the relevant task has not been merged with release branches and aims to draw the attention of developers. In this way, potential delays or errors in release processes can be detected in advance.

### Example

```yaml
name: Jira Integration Workflow

on:
  push:
    branches: [ "main" ]
  pull_request:
    branches: [ "main" ]

jobs:
  jira-integration:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Jira Search Action
        uses: ./.github/actions
        with:
          jira_server: ${{ secrets.JIRA_SERVER }}
          jira_api_token: ${{ secrets.JIRA_API_TOKEN }}
          jql_query: 'project = MYPROJECT AND status = "In Progress"'
          release_branch: 'release/.*'
```

## License

This project is licensed under the MIT License.

## Contributing

Your contributions are welcome. Please create an issue before submitting a pull request.
