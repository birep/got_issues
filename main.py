from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from github import Github
from dataclasses import dataclass, field
from datetime import datetime
from typing import List
import markdown
import os

@dataclass
class Comment:
    username: str
    body: str
    created_at: datetime
    updated_at: datetime
    show_updated_at: bool = field(init=False)

    def __post_init__(self):
        self.show_updated_at = self.created_at != self.updated_at

@dataclass
class Issue:
    title: str
    body: str
    created_at: datetime
    updated_at: datetime
    labels: List[str]
    comments: List[Comment]
    show_updated_at: bool = field(init=False)

    def __post_init__(self):
        self.show_updated_at = self.created_at != self.updated_at

app = FastAPI()

templates = Jinja2Templates(directory="templates")

GITHUB_ACCESS_TOKEN = os.environ.get("GITHUB_ACCESS_TOKEN")

def get_issues(repo_owner: str, repo_name: str, state='open', sort='created', direction='desc'):
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    issues = repo.get_issues(state=state, sort=sort, direction=direction)
    return issues

@app.get("/{repo_owner}/{repo_name}/", response_class=HTMLResponse)
async def read_root(request: Request, repo_owner: str, repo_name: str, state: str = 'open', sort: str = 'created', direction: str = 'desc'):
    issues = get_issues(repo_owner, repo_name, state, sort, direction)
    return templates.TemplateResponse("index.html", {"request": request, "issues": issues, "repo_owner": repo_owner, "repo_name": repo_name})

@app.get("/{repo_owner}/{repo_name}/issue/{issue_id}", response_class=HTMLResponse)
async def read_issue(request: Request, repo_owner: str, repo_name: str, issue_id: int):
    g = Github(GITHUB_ACCESS_TOKEN)
    repo = g.get_repo(f"{repo_owner}/{repo_name}")
    gh_issue = repo.get_issue(number=issue_id)

    issue_body_html = markdown.markdown(gh_issue.body, extensions=["mdx_linkify"])
    comments = [Comment(
                    comment.user.login,
                    markdown.markdown(comment.body),
                    comment.created_at,
                    comment.updated_at
                ) for comment in gh_issue.get_comments()]

    labels = [label.name for label in gh_issue.labels]

    issue = Issue(
        gh_issue.title,
        issue_body_html,
        gh_issue.created_at,
        gh_issue.updated_at,
        labels,
        comments
    )

    return templates.TemplateResponse(
        "issue.html",
        {
            "request": request,
            "issue": issue
        }
    )
