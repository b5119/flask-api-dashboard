"""
GitHub Analytics Core
Core functionality for GitHub repository analysis
"""

import requests
import os
from datetime import datetime

class GitHubAnalytics:
    """GitHub API analytics handler"""
    
    def __init__(self):
        self.token = os.getenv('GITHUB_TOKEN')
        self.base_url = 'https://api.github.com'
        self.headers = {
            'Accept': 'application/vnd.github.v3+json'
        }
        if self.token:
            self.headers['Authorization'] = f'token {self.token}'
    
    def _make_request(self, endpoint, params=None):
        """Make API request with error handling"""
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"GitHub API Error: {e}")
            return None
    
    def check_rate_limit(self):
        """Check remaining API rate limit"""
        data = self._make_request('rate_limit')
        if data:
            return data['rate']['remaining']
        return None
    
    def get_repository(self, owner, repo):
        """Get repository information"""
        data = self._make_request(f'repos/{owner}/{repo}')
        if not data:
            return None
        
        return {
            'name': data['name'],
            'full_name': data['full_name'],
            'description': data['description'],
            'html_url': data['html_url'],
            'stargazers_count': data['stargazers_count'],
            'watchers_count': data['watchers_count'],
            'forks_count': data['forks_count'],
            'open_issues_count': data['open_issues_count'],
            'language': data['language'],
            'created_at': data['created_at'],
            'updated_at': data['updated_at'],
            'default_branch': data['default_branch'],
            'size': data['size'],
            'license': data.get('license'),
            'topics': data.get('topics', [])
        }
    
    def get_contributors(self, owner, repo, limit=100):
        """Get repository contributors"""
        data = self._make_request(f'repos/{owner}/{repo}/contributors', 
                                  params={'per_page': limit})
        if not data:
            return []
        
        contributors = []
        for contributor in data:
            contributors.append({
                'login': contributor['login'],
                'contributions': contributor['contributions'],
                'avatar_url': contributor['avatar_url'],
                'html_url': contributor['html_url']
            })
        
        return contributors
    
    def get_languages(self, owner, repo):
        """Get programming languages used in repository"""
        data = self._make_request(f'repos/{owner}/{repo}/languages')
        if not data:
            return {}
        
        # Calculate percentages
        total = sum(data.values())
        percentages = {}
        for lang, bytes_count in data.items():
            percentages[lang] = {
                'bytes': bytes_count,
                'percentage': round((bytes_count / total) * 100, 2)
            }
        
        return percentages
    
    def get_commits(self, owner, repo, since=None, until=None, limit=100):
        """Get commit history"""
        params = {'per_page': limit}
        if since:
            params['since'] = since
        if until:
            params['until'] = until
        
        data = self._make_request(f'repos/{owner}/{repo}/commits', params=params)
        if not data:
            return []
        
        commits = []
        for commit in data:
            commits.append({
                'sha': commit['sha'],
                'message': commit['commit']['message'],
                'author': commit['commit']['author']['name'],
                'date': commit['commit']['author']['date'],
                'html_url': commit['html_url']
            })
        
        return commits
    
    def get_issues(self, owner, repo, state='all', limit=100):
        """Get repository issues"""
        params = {
            'state': state,
            'per_page': limit
        }
        
        data = self._make_request(f'repos/{owner}/{repo}/issues', params=params)
        if not data:
            return []
        
        issues = []
        for issue in data:
            # Skip pull requests (they also show up in issues endpoint)
            if 'pull_request' in issue:
                continue
            
            issues.append({
                'number': issue['number'],
                'title': issue['title'],
                'state': issue['state'],
                'created_at': issue['created_at'],
                'updated_at': issue['updated_at'],
                'html_url': issue['html_url'],
                'user': issue['user']['login']
            })
        
        return issues
    
    def get_pull_requests(self, owner, repo, state='all', limit=50):
        """Get repository pull requests"""
        params = {
            'state': state,
            'per_page': limit
        }
        
        data = self._make_request(f'repos/{owner}/{repo}/pulls', params=params)
        if not data:
            return []
        
        prs = []
        for pr in data:
            prs.append({
                'number': pr['number'],
                'title': pr['title'],
                'state': pr['state'],
                'created_at': pr['created_at'],
                'updated_at': pr['updated_at'],
                'html_url': pr['html_url'],
                'user': pr['user']['login']
            })
        
        return prs
    
    def get_releases(self, owner, repo):
        """Get repository releases"""
        data = self._make_request(f'repos/{owner}/{repo}/releases')
        if not data:
            return []
        
        releases = []
        for release in data:
            releases.append({
                'name': release['name'] or release['tag_name'],
                'tag_name': release['tag_name'],
                'published_at': release['published_at'],
                'html_url': release['html_url'],
                'author': release['author']['login']
            })
        
        return releases