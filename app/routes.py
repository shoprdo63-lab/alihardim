from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from app.models.database import Product, Category, db
from app.api.aliexpress import aliexpress_api
from config import Config
from sqlalchemy import func, or_

main = Blueprint('main', __name__)


def get_category_key_from_name(name):
    """Convert Hebrew category name to key."""
    for key, val in Config.SAFE_CATEGORIES.items():
        if val == name:
            return key
    return name.lower().replace(' ', '_')


@main.route('/')
def index():
    """Home page with featured products."""
    # Get featured products from different categories
    featured_products = []
    
    # Get one product from each category
    for category_key in list(Config.SAFE_CATEGORIES.keys())[:6]:
        product = Product.query.filter_by(
            category=category_key,
            is_modest=True
        ).order_by(func.random()).first()
        if product:
            featured_products.append(product)
    
    # Get hot/new products
    new_products = Product.query.filter_by(is_modest=True).order_by(
        Product.created_at.desc()
    ).limit(12).all()
    
    # Get popular products
    popular_products = Product.query.filter_by(is_modest=True).order_by(
        Product.orders_count.desc().nullslast()
    ).limit(12).all()
    
    # Categories with counts
    categories = []
    for key, name in Config.SAFE_CATEGORIES.items():
        count = Product.query.filter_by(category=key).count()
        categories.append({
            'key': key,
            'name': name,
            'count': count,
            'icon': get_category_icon(key)
        })
    
    return render_template('index.html',
                          featured_products=featured_products,
                          new_products=new_products,
                          popular_products=popular_products,
                          categories=categories)


@main.route('/category/<category_key>')
def category(category_key):
    """Category page with products."""
    page = request.args.get('page', 1, type=int)
    sort = request.args.get('sort', 'popular')
    
    # Validate category
    if category_key not in Config.SAFE_CATEGORIES:
        return redirect(url_for('main.index'))
    
    # Base query
    query = Product.query.filter_by(category=category_key, is_modest=True)
    
    # Sorting
    if sort == 'price_asc':
        query = query.order_by(Product.price.asc())
    elif sort == 'price_desc':
        query = query.order_by(Product.price.desc())
    elif sort == 'newest':
        query = query.order_by(Product.created_at.desc())
    else:  # popular
        query = query.order_by(Product.orders_count.desc().nullslast())
    
    # Paginate
    products = query.paginate(page=page, per_page=Config.PRODUCTS_PER_PAGE, error_out=False)
    
    category_name = Config.SAFE_CATEGORIES.get(category_key, category_key)
    
    return render_template('category.html',
                          products=products,
                          category_key=category_key,
                          category_name=category_name,
                          sort=sort,
                          total=query.count())


@main.route('/product/<product_id>')
def product_detail(product_id):
    """Product detail page."""
    product = Product.query.filter_by(product_id=product_id).first_or_404()
    
    # Get related products from same category
    related = Product.query.filter(
        Product.category == product.category,
        Product.id != product.id,
        Product.is_modest == True
    ).order_by(func.random()).limit(8).all()
    
    return render_template('product.html',
                          product=product,
                          related_products=related)


@main.route('/search')
def search():
    """Search products."""
    query_text = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', '')
    
    if not query_text:
        return render_template('search.html', 
                            products=None,
                            query='',
                            message='הקלד מילת חיפוש')
    
    # Build search query
    search_query = Product.query.filter(Product.is_modest == True)
    
    # Text search in title and description (Hebrew or English)
    search_filter = or_(
        Product.title.ilike(f'%{query_text}%'),
        Product.title_hebrew.ilike(f'%{query_text}%'),
        Product.description.ilike(f'%{query_text}%'),
        Product.description_hebrew.ilike(f'%{query_text}%')
    )
    search_query = search_query.filter(search_filter)
    
    # Category filter
    if category and category in Config.SAFE_CATEGORIES:
        search_query = search_query.filter_by(category=category)
    
    # Get results
    products = search_query.order_by(Product.orders_count.desc().nullslast()).paginate(
        page=page, per_page=Config.PRODUCTS_PER_PAGE, error_out=False
    )
    
    # Save search query
    if query_text:
        from app.models.database import SearchQuery
        sq = SearchQuery(query=query_text, category=category, results_count=products.total)
        db.session.add(sq)
        db.session.commit()
    
    return render_template('search.html',
                          products=products,
                          query=query_text,
                          category=category,
                          total=products.total)


@main.route('/api/sync-products', methods=['POST'])
def sync_products():
    """API endpoint to sync products from AliExpress."""
    try:
        # Get search keywords for each category
        from app.services.content_filter import SAFE_SEARCH_KEYWORDS
        
        added_count = 0
        
        # Keywords for each category
        category_keywords = {
            'electronic': ['smartphone', 'laptop', 'headphones', 'charger', 'cable'],
            'toys': ['lego', 'educational toy', 'puzzle', 'remote control car'],
            'home_garden': ['kitchen', 'storage', 'garden tools', 'led lamp'],
            'tools': ['drill', 'tool set', 'screwdriver'],
            'jewish': ['kippah', 'tzitzit', 'menorah', 'mezuzah'],
            'sports': ['camping', 'tent', 'backpack', 'sports equipment'],
            'car': ['car accessories', 'car organizer', 'car tool'],
            'pet': ['dog toy', 'cat toy', 'pet accessories'],
            'office': ['notebook', 'pen', 'desk organizer'],
            'art': ['paint', 'canvas', 'art supplies'],
        }
        
        for category_key, keywords in category_keywords.items():
            for keyword in keywords[:2]:  # Limit to 2 keywords per category
                try:
                    # Fetch products
                    api_products = aliexpress_api.search_products(
                        keywords=keyword,
                        page_size=20
                    )
                    
                    # Save to database
                    for api_product in api_products:
                        # Check if product already exists
                        existing = Product.query.filter_by(
                            product_id=api_product['product_id']
                        ).first()
                        
                        if not existing:
                            product = Product(
                                product_id=api_product['product_id'],
                                title=api_product['title'],
                                title_hebrew=api_product.get('title_hebrew', api_product['title']),
                                description_hebrew=api_product.get('description_hebrew', ''),
                                price=api_product['price'],
                                original_price=api_product.get('original_price'),
                                currency='USD',
                                category=category_key,
                                image_url=api_product['image_url'],
                                product_url=api_product['product_url'],
                                affiliate_url=api_product.get('affiliate_url', ''),
                                rating=float(api_product['rating']) if api_product.get('rating') else None,
                                store_name=api_product.get('store_name', ''),
                                is_modest=True
                            )
                            db.session.add(product)
                            added_count += 1
                    
                    db.session.commit()
                except Exception as e:
                    print(f"Error syncing {keyword}: {e}")
                    db.session.rollback()
                    continue
        
        return jsonify({
            'success': True,
            'added': added_count,
            'message': f'נוספו {added_count} מוצרים בהצלחה!'
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@main.route('/api/products/count')
def products_count():
    """Get total products count."""
    total = Product.query.filter_by(is_modest=True).count()
    by_category = {}
    
    for key in Config.SAFE_CATEGORIES.keys():
        by_category[key] = Product.query.filter_by(category=key).count()
    
    return jsonify({
        'total': total,
        'by_category': by_category
    })


@main.route('/cart')
def cart():
    """Shopping cart page."""
    # Get cart from session (stored in localStorage on frontend)
    # For now, show empty cart template
    return render_template('cart.html')


@main.route('/wishlist')
def wishlist():
    """Wishlist/Favorites page."""
    # Get wishlist from session
    # For now, show empty wishlist template
    return render_template('wishlist.html')


@main.route('/login')
def login():
    """Login page."""
    return render_template('login.html')


def get_category_icon(key):
    """Get icon name for category."""
    icons = {
        'electronic': 'laptop',
        'toys': 'toy-brick',
        'home_garden': 'home',
        'tools': 'tools',
        'jewish': 'star-of-david',
        'sports': 'basketball',
        'car': 'car',
        'pet': 'paw',
        'office': 'pencil',
        'art': 'palette',
    }
    return icons.get(key, 'tag')
