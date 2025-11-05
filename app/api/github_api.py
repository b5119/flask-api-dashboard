#!/usr/bin/env python3
"""
Flask API - GitHub Repository Analytics
Converts CLI-based GitHub Analytics into RESTful API endpoints.
"""

from flask import Flask, jsonify, request
from github_analytics_core import GitHubAnalytics  # We'll isolate logic in core file for clarity
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
analytics = GitHubAnalytics()


@app.route('/')
def home():
    """API Root Endpoint"""
    return jsonify({
        "message": "Welcome to GitHub Analytics API",
        "endpoints": {
            "/api/repo/<owner>/<repo>": "Get general repository info",
            "/api/repo/<owner>/<repo>/contributors": "Get contributors list",
            "/api/repo/<owner>/<repo>/languages": "Get programming language stats",
            "/api/repo/<owner>/<repo>/commits": "Get commit statistics",
            "/api/repo/<owner>/<repo>/issues": "Get issues data",
            "/api/repo/<owner>/<repo>/releases": "Get release data",
            "/api/repo/<owner>/<repo>/full-report": "Generate complete repo analytics report",
            "/api/rate-limit": "Check GitHub API rate limit"
        }
    })


@app.route('/api/rate-limit')
def rate_limit():
    """Check GitHub API rate limit"""
    limit = analytics.check_rate_limit()
    return jsonify({"rate_limit_remaining": limit})


@app.route('/api/repo/<owner>/<repo>')
def repo_info(owner, repo):
    """Fetch repository metadata"""
    data = analytics.get_repository(owner, repo)
    if not data:
        return jsonify({"error": "Repository not found"}), 404
    return jsonify(data)


@app.route('/api/repo/<owner>/<repo>/contributors')
def repo_contributors(owner, repo):
    """Fetch top contributors"""
    limit = request.args.get('limit', default=30, type=int)
    contributors = analytics.get_contributors(owner, repo, limit)
    return jsonify(contributors)


@app.route('/api/repo/<owner>/<repo>/languages')
def repo_languages(owner, repo):
    """Fetch programming language usage"""
    data = analytics.get_languages(owner, repo)
    return jsonify(data)


@app.route('/api/repo/<owner>/<repo>/commits')
def repo_commits(owner, repo):
    """Fetch commits data"""
    since = request.args.get('since')
    until = request.args.get('until')
    limit = request.args.get('limit', 100, type=int)
    commits = analytics.get_commits(owner, repo, since, until, limit)
    return jsonify(commits)


@app.route('/api/repo/<owner>/<repo>/issues')
def repo_issues(owner, repo):
    """Fetch repository issues"""
    state = request.args.get('state', 'all')
    limit = request.args.get('limit', 100, type=int)
    issues = analytics.get_issues(owner, repo, state, limit)
    return jsonify(issues)


@app.route('/api/repo/<owner>/<repo>/releases')
def repo_releases(owner, repo):
    """Fetch repository releases"""
    releases = analytics.get_releases(owner, repo)
    return jsonify(releases)


@app.route('/api/repo/<owner>/<repo>/full-report')
def full_report(owner, repo):
    """Generate comprehensive analytics report"""
    report = {
        "repository": analytics.get_repository(owner, repo),
        "contributors": analytics.get_contributors(owner, repo),
        "languages": analytics.get_languages(owner, repo),
        "commits": analytics.get_commits(owner, repo, limit=100),
        "issues": analytics.get_issues(owner, repo, limit=100),
        "pull_requests": analytics.get_pull_requests(owner, repo, limit=50),
        "releases": analytics.get_releases(owner, repo),
    }
    return jsonify(report)


if __name__ == '__main__':
    port = int(os.getenv("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
