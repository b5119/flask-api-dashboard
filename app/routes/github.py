"""
GitHub Routes
Handles GitHub-related endpoints
"""

from flask import Blueprint, jsonify, request
from app.api.github_api import GitHubAPI

github_bp = Blueprint('github', __name__)
github_api = GitHubAPI()

@github_bp.route('/repo/<owner>/<repo>')
def get_repository(owner, repo):
    """Get GitHub repository information"""
    try:
        result = github_api.get_repository(owner, repo)
        
        if result:
            return jsonify({
                'success': True,
                'repository': result
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Repository not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/contributors')
def get_contributors(owner, repo):
    """Get repository contributors"""
    limit = request.args.get('limit', 100, type=int)
    
    try:
        contributors = github_api.get_contributors(owner, repo, limit)
        
        return jsonify({
            'success': True,
            'contributors': contributors
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/languages')
def get_languages(owner, repo):
    """Get repository languages"""
    try:
        languages = github_api.get_languages(owner, repo)
        
        return jsonify({
            'success': True,
            'languages': languages
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/commits')
def get_commits(owner, repo):
    """Get repository commits"""
    since = request.args.get('since')
    until = request.args.get('until')
    limit = request.args.get('limit', 100, type=int)
    
    try:
        commits = github_api.get_commits(owner, repo, since, until, limit)
        
        return jsonify({
            'success': True,
            'commits': commits
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/issues')
def get_issues(owner, repo):
    """Get repository issues"""
    state = request.args.get('state', 'all')
    limit = request.args.get('limit', 100, type=int)
    
    try:
        issues = github_api.get_issues(owner, repo, state, limit)
        
        return jsonify({
            'success': True,
            'issues': issues
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/pulls')
def get_pull_requests(owner, repo):
    """Get repository pull requests"""
    limit = request.args.get('limit', 50, type=int)
    
    try:
        pulls = github_api.get_pull_requests(owner, repo, limit)
        
        return jsonify({
            'success': True,
            'pull_requests': pulls
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/repo/<owner>/<repo>/releases')
def get_releases(owner, repo):
    """Get repository releases"""
    try:
        releases = github_api.get_releases(owner, repo)
        
        return jsonify({
            'success': True,
            'releases': releases
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/trending')
def get_trending():
    """Get trending GitHub repositories"""
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    limit = request.args.get('limit', 30, type=int)
    
    try:
        repos = github_api.get_trending_repos(language, since, limit)
        
        return jsonify({
            'success': True,
            'repositories': repos,
            'count': len(repos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/search')
def search_repositories():
    """Search GitHub repositories"""
    query = request.args.get('q')
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Query parameter "q" is required'
        }), 400
    
    sort = request.args.get('sort', 'stars')
    order = request.args.get('order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    
    try:
        repos = github_api.search_repositories(query, sort, order, page, per_page)
        
        return jsonify({
            'success': True,
            'repositories': repos,
            'count': len(repos)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@github_bp.route('/status')
def check_status():
    """Check if GitHub API is available"""
    is_available = github_api.check_status()
    
    return jsonify({
        'available': is_available,
        'message': 'GitHub API is available' if is_available else 'GitHub API unavailable'
    })