"""
GitHub Routes
"""

from flask import Blueprint, render_template, request, jsonify
from app.api.github_api import GitHubAPI

github_bp = Blueprint('github', __name__)
github_api = GitHubAPI()


@github_bp.route('/')
def index():
    """GitHub explorer home"""
    return render_template('github.html',
                         title='GitHub Explorer',
                         active_page='github')


@github_bp.route('/api/repo/<owner>/<repo>')
def get_repository(owner, repo):
    """Get repository information"""
    try:
        repo_data = github_api.get_repository(owner, repo)
        
        if repo_data:
            return jsonify({
                'success': True,
                'repository': repo_data
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


@github_bp.route('/api/repo/<owner>/<repo>/contributors')
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


@github_bp.route('/api/repo/<owner>/<repo>/languages')
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


@github_bp.route('/api/trending')
def get_trending():
    """Get trending repositories"""
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    
    try:
        trending = github_api.get_trending_repos(language, since)
        
        return jsonify({
            'success': True,
            'repositories': trending
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@github_bp.route('/api/search/repositories')
def search_repositories():
    """Search repositories"""
    query = request.args.get('q', '')
    sort = request.args.get('sort', 'stars')
    order = request.args.get('order', 'desc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 30, type=int)
    
    if not query:
        return jsonify({
            'success': False,
            'error': 'Search query required'
        }), 400
    
    try:
        results = github_api.search_repositories(
            query=query,
            sort=sort,
            order=order,
            page=page,
            per_page=per_page
        )
        
        return jsonify({
            'success': True,
            'results': results
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500