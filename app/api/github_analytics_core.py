#!/usr/bin/env python3
"""
GitHub Analytics Core Module
Contains the main logic for interacting with GitHub API
"""

import os
import requests
from datetime import datetime

class GitHubAnalytics:
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {'Authorization': f'token {self.token}'} if self.token else {}

    def check_rate_limit(self):
        response = requests.get(f'{self.base_url}/rate_limit', headers=self.headers)
        return response.json()['resources']['core']['remaining']

    def get_repository(self, owner, repo):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}', headers=self.headers)
        return response.json() if response.status_code == 200 else None

    def get_contributors(self, owner, repo, limit=30):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/contributors', 
                              params={'per_page': limit}, headers=self.headers)
        return response.json() if response.status_code == 200 else []

    def get_languages(self, owner, repo):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/languages', headers=self.headers)
        return response.json() if response.status_code == 200 else {}

    def get_commits(self, owner, repo, since=None, until=None, limit=100):
        params = {'per_page': limit}
        if since: params['since'] = since
        if until: params['until'] = until
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/commits', 
                              params=params, headers=self.headers)
        return response.json() if response.status_code == 200 else []

    def get_issues(self, owner, repo, state='all', limit=100):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/issues',
                              params={'state': state, 'per_page': limit}, headers=self.headers)
        return response.json() if response.status_code == 200 else []

    def get_releases(self, owner, repo):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/releases', headers=self.headers)
        return response.json() if response.status_code == 200 else []

    def get_pull_requests(self, owner, repo, state='all', limit=50):
        response = requests.get(f'{self.base_url}/repos/{owner}/{repo}/pulls',
                              params={'state': state, 'per_page': limit}, headers=self.headers)
        return response.json() if response.status_code == 200 else []