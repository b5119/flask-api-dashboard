#!/usr/bin/env python3
"""
Flask API - GitHub Repository Analytics
"""

from flask import jsonify, request
from app.api.github_analytics_core import GitHubAnalytics
from datetime import datetime, timedelta
import requests
import os

class GitHubAPI:
    """GitHub API handler class"""
    
    def __init__(self):
        self.analytics = GitHubAnalytics()
    
    def check_status(self):
        """Check if GitHub API is available"""
        try:
            limit = self.analytics.check_rate_limit()
            return limit is not None and limit > 0
        except:
            return False
    
    def get_repository(self, owner, repo):
        """Get repository information"""
        return self.analytics.get_repository(owner, repo)
    
    def get_contributors(self, owner, repo, limit=100):
        """Get repository contributors"""
        return self.analytics.get_contributors(owner, repo, limit)
    
    def get_languages(self, owner, repo):
        """Get repository languages"""
        return self.analytics.get_languages(owner, repo)
    
    def get_commits(self, owner, repo, since=None, until=None, limit=100):
        """Get repository commits"""
        return self.analytics.get_commits(owner, repo, since, until, limit)
    
    def get_issues(self, owner, repo, state='all', limit=100):
        """Get repository issues"""
        return self.analytics.get_issues(owner, repo, state, limit)
    
    def get_pull_requests(self, owner, repo, limit=50):
        """Get repository pull requests"""
        return self.analytics.get_pull_requests(owner, repo, 'all', limit)
    
    def get_releases(self, owner, repo):
        """Get repository releases"""
        return self.analytics.get_releases(owner, repo)
    
    def get_trending_repos(self, language=None, since='daily', limit=30):
        """Get trending repositories"""
        try:
            # Build query based on time period
            if since == 'daily':
                date_filter = f"created:>={(datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')}"
            elif since == 'weekly':
                date_filter = f"created:>={(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')}"
            else:
                date_filter = 'stars:>1000'
            
            query = date_filter
            if language:
                query += f' language:{language}'
            
            return self.search_repositories(query, limit=limit)
        except Exception as e:
            print(f"GitHub Trending Error: {e}")
            return []
    
    def search_repositories(self, query, sort='stars', order='desc', page=1, per_page=30, limit=None):
        """Search GitHub repositories"""
        try:
            url = "https://api.github.com/search/repositories"
            params = {
                'q': query,
                'sort': sort,
                'order': order,
                'page': page,
                'per_page': per_page if not limit else min(limit, per_page)
            }
            
            headers = {'Accept': 'application/vnd.github.v3+json'}
            token = os.getenv('GITHUB_TOKEN')
            if token:
                headers['Authorization'] = f'token {token}'
            
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            repos = []
            items = data.get('items', [])
            if limit:
                items = items[:limit]
            
            for item in items:
                repos.append({
                    'name': item['name'],
                    'full_name': item['full_name'],
                    'description': item['description'],
                    'stars': item['stargazers_count'],
                    'stargazers_count': item['stargazers_count'],
                    'forks': item['forks_count'],
                    'forks_count': item['forks_count'],
                    'language': item['language'],
                    'url': item['html_url'],
                    'html_url': item['html_url'],
                    'owner': {
                        'login': item['owner']['login']
                    }
                })
            
            return repos
        except Exception as e:
            print(f"GitHub Search Error: {e}")
            return []
    
    # Flask route wrapper methods
    def rate_limit(self):
        """Check GitHub API rate limit"""
        limit = self.analytics.check_rate_limit()
        return jsonify({"rate_limit_remaining": limit})
    
    def repo_info(self, owner, repo):
        """Fetch repository metadata"""
        data = self.analytics.get_repository(owner, repo)
        if not data:
            return jsonify({"error": "Repository not found"}), 404
        return jsonify(data)
    
    def repo_contributors(self, owner, repo):
        """Fetch top contributors"""
        limit = request.args.get('limit', default=30, type=int)
        contributors = self.analytics.get_contributors(owner, repo, limit)
        return jsonify(contributors)
    
    def repo_languages(self, owner, repo):
        """Fetch programming language usage"""
        data = self.analytics.get_languages(owner, repo)
        return jsonify(data)
    
    def repo_commits(self, owner, repo):
        """Fetch commits data"""
        since = request.args.get('since')
        until = request.args.get('until')
        limit = request.args.get('limit', 100, type=int)
        commits = self.analytics.get_commits(owner, repo, since, until, limit)
        return jsonify(commits)
    
    def repo_issues(self, owner, repo):
        """Fetch repository issues"""
        state = request.args.get('state', 'all')
        limit = request.args.get('limit', 100, type=int)
        issues = self.analytics.get_issues(owner, repo, state, limit)
        return jsonify(issues)
    
    def repo_releases(self, owner, repo):
        """Fetch repository releases"""
        releases = self.analytics.get_releases(owner, repo)
        return jsonify(releases)
    
    def full_report(self, owner, repo):
        """Generate comprehensive analytics report"""
        report = {
            "repository": self.analytics.get_repository(owner, repo),
            "contributors": self.analytics.get_contributors(owner, repo),
            "languages": self.analytics.get_languages(owner, repo),
            "commits": self.analytics.get_commits(owner, repo, limit=100),
            "issues": self.analytics.get_issues(owner, repo, limit=100),
            "pull_requests": self.analytics.get_pull_requests(owner, repo, limit=50),
            "releases": self.analytics.get_releases(owner, repo),
        }
        return jsonify(report)