# got_issues

## Overview

This is a simple alternative frontend for GitHub issues. It is built with FastAPI, Jinja2, and Tailwinds.

## Installation

1. Clone this repository.
2. Install required packages.

    ```bash
    pip install -r requirements.txt
    ```

3. Set the `GITHUB_ACCESS_TOKEN` environment variable to your GitHub Personal Access Token.

    ```bash
    export GITHUB_ACCESS_TOKEN=your_personal_access_token
    ```

4. Run the FastAPI server.

    ```bash
    uvicorn main:app --reload
    ```

5. Navigate to `http://localhost:8000/{repo_owner}/{repo_name}` in your web browser to view issues.

## Project Structure

- `main.py`: Contains the FastAPI application and all route definitions.
- `templates/`: Contains Jinja2 templates for the frontend.

## Endpoints

- `GET /{repo_owner}/{repo_name}/`: List all issues for a specific repository
- `GET /{repo_owner}/{repo_name}/issue/{issue_id}`: View a single issue

## Environment Variables

- `GITHUB_ACCESS_TOKEN`: GitHub Personal Access Token for API access

## Dependencies

Refer to `requirements.txt` for a full list of dependencies.
