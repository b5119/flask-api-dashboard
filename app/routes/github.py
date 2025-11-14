"""
GitHub Routes
"""
from flask import Blueprint, render_template, jsonify, request
from app.api.github_api import GitHubAPI

github_bp = Blueprint('github', __name__)
github_api = GitHubAPI()

@github_bp.route('/')
def index():
    """GitHub home page"""
    return render_template('github.html',
                         title='GitHub Explorer',
                         active_page='github')

@github_bp.route('/home')
def github_home():
    """Alias for github home (required by templates)"""
    return index()

@github_bp.route('/api/trending')
def api_trending():
    """API endpoint for trending repos"""
    language = request.args.get('language')
    since = request.args.get('since', 'daily')
    limit = request.args.get('limit', 30, type=int)
    
    try:
        repos = github_api.get_trending_repos(language, since, limit)
        return jsonify({'success': True, 'repositories': repos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@github_bp.route('/api/search/repositories')
def api_search():
    """API endpoint for searching repos"""
    query = request.args.get('q')
    if not query:
        return jsonify({'success': False, 'error': 'Query required'}), 400
    
    try:
        repos = github_api.search_repositories(query)
        return jsonify({'success': True, 'results': repos})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@github_bp.route('/api/repo/<owner>/<repo>')
def api_repo(owner, repo):
    """API endpoint for repo details"""
    try:
        result = github_api.get_repository(owner, repo)
        if result:
            return jsonify({'success': True, 'repository': result})
        else:
            return jsonify({'success': False, 'error': 'Repository not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500