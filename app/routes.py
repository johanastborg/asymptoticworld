from flask import Blueprint, jsonify, request
from app import db
from app.models import Post, VisitorStats
from app.services import content_generator, image_generator, trends

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return jsonify({'message': 'Welcome to Asymptotic World API'})

@bp.route('/posts', methods=['GET'])
def get_posts():
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return jsonify([post.to_dict() for post in posts])

@bp.route('/posts/generate', methods=['POST'])
def generate_post():
    """
    Triggers the generation of a new post based on trends.
    """
    # 1. Get trending topics
    trending_topic = trends.get_current_trend()

    # 2. Generate content using Gemini
    title, content = content_generator.generate_blog_post(trending_topic)

    # 3. Generate image using Nano Banana
    image_url = image_generator.generate_header_image(title)

    # 4. Save to DB
    new_post = Post(title=title, content=content, header_image_url=image_url)
    db.session.add(new_post)
    db.session.commit()

    return jsonify(new_post.to_dict()), 201

@bp.route('/stats/visit', methods=['POST'])
def record_visit():
    data = request.json
    page = data.get('page', '/')
    ip = request.remote_addr # simplified
    visit = VisitorStats(page_viewed=page, visitor_ip=ip)
    db.session.add(visit)
    db.session.commit()
    return jsonify({'status': 'recorded'}), 200
