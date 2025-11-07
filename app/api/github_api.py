#!/usr/bin/env python3
"""
Flask API - GitHub Repository Analytics
Converts CLI-based GitHub Analytics into RESTful API endpoints.
"""

from flask import jsonify, request
from app.api.github_analytics_core import GitHubAnalytics

class GitHubAPI:
    """GitHub API handler class"""
    
    def __init__(self):
        self.analytics = GitHubAnalytics()
    
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