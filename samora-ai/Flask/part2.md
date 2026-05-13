# Flask Interview Questions and Answers - Part 2

## Q1: How does Flask's internal request dispatching work?
**A:** Flask uses Werkzeug's routing system. When a request arrives, Flask's `wsgi_app` method is called. It creates a `Request` object, matches the URL against the URL map (`url_map`), and calls the matched view function. The routing uses `Rule` objects compiled to regular expressions. Matching considers: URL pattern, HTTP method constraints, subdomain, and `strict_slashes`. The matched endpoint name is used to look up the view function. Before calling the view, Flask processes `before_request` hooks. After the view returns, `after_request` hooks modify the response. The response goes through WSGI processing. Custom URL converters can be registered for complex parameter parsing.

## Q2: What is the difference between `Flask.g` and `flask.session`?
**A:** `g` (global context) is a request-scoped object for storing data during a single request. It's cleared after each request. Common uses: caching database connections, storing current user, sharing data between `before_request` and view functions. `session` is a cookie-based object that persists across requests (within a client's browser session). Session data is cryptographically signed (stored in a cookie). `g` is per-request, cleared automatically. `session` is per-user-session, persists across requests. `g` is not shared between requests; `session` is not shared between users. Both are thread-local proxies.

## Q3: How do you implement WebSocket support in Flask?
**A:** Flask doesn't natively support WebSockets (it's WSGI-based). Options: (1) **Flask-SocketIO** — integrates Socket.IO with Flask, supports WebSocket fallback, (2) **gevent-websocket** — monkey-patches WSGI for WebSocket support, (3) Use ASGI — migrate to Quart (Flask-like ASGI framework) or FastAPI. Flask-SocketIO example:

```python
from flask import Flask
from flask_socketio import SocketIO, emit
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
@socketio.on('message')
def handle_message(data):
    emit('response', {'data': data}, broadcast=True)
if __name__ == '__main__':
    socketio.run(app)
```

SocketIO supports: rooms, namespaces, event-based messaging, automatic reconnection, and binary data. For production, use eventlet or gevent as the async mode.

## Q4: Explain Flask's `teardown_request` and `teardown_appcontext`.
**A:** `teardown_request` is called at the end of each request regardless of whether an exception occurred. It's used for cleanup that must happen after every request (closing database connections, releasing locks). `teardown_appcontext` is called when the application context is torn down (typically at the end of a request or CLI command). Difference: `teardown_request` fires per-request; `teardown_appcontext` fires per-application-context (which may span multiple requests). `teardown_request` receives the exception (or None). For cleanup that must happen even on errors, use `try/finally` in the request handler or `teardown_request`.

## Q5: How do you implement database migrations in Flask?
**A:** Flask-Migrate (based on Alembic) handles database migrations: `flask db init`, `flask db migrate -m "message"`, `flask db upgrade`, `flask db downgrade`. Configuration:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
app = Flask(__name__)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
```

Best practices: (1) always review auto-generated migrations before committing, (2) test both upgrade and downgrade, (3) use `flask db history` to track migration order, (4) run migrations as a separate deployment step, (5) use `merge` for parallel migration branches.

## Q6: What is Flask's `url_for` and how does it handle dynamic URLs?
**A:** `url_for(endpoint, **values)` generates URLs for named routes. It supports: (1) path parameters, (2) query string (extra kwargs become `?key=value`), (3) `_external=True` for absolute URLs, (4) `_anchor` for hash fragments, (5) `_method` for HTTP method. `url_for` uses the URL map to generate URLs — it raises `BuildError` for non-existent endpoints. Using `url_for` instead of hardcoded URLs enables easy URL structure changes. For static files: `url_for('static', filename='style.css')`.

## Q7: How do you implement role-based access control (RBAC) in Flask?
**A:** RBAC with custom decorators:

```python
from functools import wraps
from flask import abort, g

def require_role(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not g.current_user or role not in g.current_user.roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator
```

Flask-Principal alternative:

```python
from flask_principal import Principal, RoleNeed, Permission
admin_permission = Permission(RoleNeed('admin'))
```

For complex RBAC: store roles in database with many-to-many relationships, support role hierarchy, cache permissions per session, implement permission checking in templates. For fine-grained permissions, use resources and actions: `Permission('users', 'edit')`.

## Q8: Explain Flask's `abort()` function and custom error pages.
**A:** `abort(status_code, description=None)` raises an HTTP exception:

```python
@app.route('/item/<int:item_id>')
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        abort(404, description="Item not found")
    return render_template('item.html', item=item)

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html', error=error), 404
```

`abort` works with standard HTTP codes and custom codes. `errorhandler` registers handlers per code or exception class. Common handlers: 400, 403, 404, 405, 429, 500. Custom exceptions extend `HTTPException`. Generic handler: `@app.errorhandler(Exception)` — use cautiously.

## Q9: How do you implement Flask background tasks without Celery?
**A:** Lightweight options:

```python
import threading
@app.route('/send-email')
def send_email_route():
    thread = threading.Thread(target=send_email, args=(request.form,))
    thread.daemon = True
    thread.start()
    return "Email queued"

def send_email(data):
    with app.app_context():
        user = User.query.get(data['user_id'])
        mail.send(user.email, data['message'])
```

Other approaches: (1) Queue with Python's `queue.Queue` — background worker thread, (2) Redis queue (RQ), (3) APScheduler, (4) thread pool (`concurrent.futures.ThreadPoolExecutor`), (5) subprocess. Caveats: threads need app context (`app.app_context().push()`), daemon threads die on shutdown.

## Q10: What is the Flask `before_request` and `after_request` lifecycle?
**A:** Request lifecycle order: (1) `before_first_request` (runs once, deprecated in 2.3+), (2) `before_request` — runs before each view (return a Response to short-circuit), (3) view function, (4) `after_request` — runs after each view (must return a Response), (5) `teardown_request` — runs even on exceptions. When `before_request` returns a Response, the view isn't called — the response goes directly to `after_request` handlers. Use `before_request` for: auth, DB connection, rate limiting. Use `after_request` for: headers, logging, response modification.

## Q11: How do you implement caching in Flask?
**A:** Flask-Caching provides multiple backends:

```python
from flask_caching import Cache
app.config['CACHE_TYPE'] = 'RedisCache'  # SimpleCache, FileSystemCache, RedisCache, MemcachedCache
cache = Cache(app)

@app.route('/expensive')
@cache.cached(timeout=300)
def expensive_view():
    data = expensive_database_query()
    return render_template('data.html', data=data)
```

Cache types: `SimpleCache` (in-memory, per-process), `FileSystemCache` (shared directory), `RedisCache` (distributed, production), `MemcachedCache`. Cache invalidation: `cache.delete('key')`, `cache.clear()`. `cached` caches entire response; `memoize` caches function return values per arguments. For template fragment caching: `{% cache 300, 'user', user.id %}...{% endcache %}`.

## Q12: Explain Flask's `request` object properties and methods.
**A:** The `request` object provides: `request.url` (full URL), `request.path` (path only), `request.args` (query params), `request.form` (form data), `request.json` (parsed JSON), `request.data` (raw bytes), `request.files` (uploaded files), `request.method` (HTTP method), `request.headers` (headers), `request.cookies`, `request.content_type`, `request.remote_addr` (client IP), `request.user_agent`, `request.referrer`, `request.host`, `request.scheme` (http/https), `request.is_secure`, `request.is_json`, `request.accept_mimetypes`, `request.access_route` (proxy-aware IP chain). `request` is a thread-local proxy accessible only within an active request context.

## Q13: How do you implement API rate limiting in Flask?
**A:** Flask-Limiter provides flexible rate limiting:

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(app=app, key_func=get_remote_address, default_limits=["200 per day", "50 per hour"])

@app.route("/slow")
@limiter.limit("1 per second")
def slow():
    return "Limited"
```

Rate limit strategies: fixed window, sliding window, token bucket. Key functions: `get_remote_address`, custom by user ID or API key. Storage backends: Redis (production), memory (development). Include rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`.

## Q14: What is the difference between `Flask.jsonify` and `json.dumps`?
**A:** `jsonify(data)` creates a `Response` object with `application/json` content type. It serializes data to JSON and wraps it in a Flask response. `json.dumps(data)` returns a JSON string (no response object). `jsonify` handles: setting MIME type, JSONP support, serializer defaults (datetimes, Decimal), response creation. Flask 2.3+ deprecated `jsonify` in favor of returning dicts directly (Flask auto-converts). For custom serialization, use `app.json` provider pattern.

## Q15: How do you implement Flask forms with CSRF protection?
**A:** Flask-WTF provides CSRF-protected forms:

```python
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign In')
```

CSRF protection: Flask-WTF generates a unique CSRF token per session, included as hidden field in forms, validated on POST requests. For AJAX: include `X-CSRFToken` header. For API-only apps, disable CSRF: `WTF_CSRF_CHECK_DEFAULT=False`.

## Q16: Explain Flask's `stream_template` and template streaming.
**A:** Flask supports streaming template rendering for lower Time-To-First-Byte:

```python
@app.route('/stream')
def streamed_page():
    def generate():
        yield render_template('header.html')
        for i in range(100):
            yield render_template('item.html', item=i)
        yield render_template('footer.html')
    return Response(generate(), content_type='text/html')
```

Flask 2.3+ provides `stream_template('template.html', items=items)`. Streaming benefits: lower TTFB, progressive rendering. Limitations: no ETag generation, headers can't change after first byte, template errors appear mid-stream. For SSE: `content_type='text/event-stream'`.

## Q17: How do you implement Flask testing with pytest?
**A:** Flask application testing with pytest:

```python
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
```

Tools: `client.get/post/put/delete`, `response.get_json()`, `response.status_code`. Use `app.test_request_context()` for URL generation without HTTP. Mock external services with `pytest-mock`. Test database with in-memory SQLite.

## Q18: What is Flask's `stream_with_context` and when is it needed?
**A:** `stream_with_context` pushes the application context for streaming responses:

```python
from flask import stream_with_context, Response

@app.route('/stream-logs')
def stream_logs():
    def generate():
        user_id = request.args.get('user_id')
        with app.app_context():
            for log in get_logs_for_user(user_id):
                yield f"data: {log}\n\n"
    return Response(stream_with_context(generate()), mimetype='text/event-stream')
```

Without it, the generator runs outside the request context — `request`, `g`, `session` would raise `RuntimeError`. Needed when accessing Flask globals inside the generator.

## Q19: How do you implement Flask CLI commands?
**A:** Custom CLI commands with Click:

```python
import click
from flask.cli import with_appcontext

@app.cli.command('init-db')
@with_appcontext
def init_db_command():
    db.create_all()
    click.echo('Database initialized.')

@app.cli.command('create-user')
@click.argument('username')
@click.option('--admin', is_flag=True)
@click.password_option()
@with_appcontext
def create_user_command(username, password, admin):
    user = User(username=username, role='admin' if admin else 'user')
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
```

Run: `flask init-db`, `flask create-user --admin alice`.

## Q20: Explain Flask's `register_error_handler` vs `errorhandler` decorator.
**A:** Both register error handlers but differ in usage:

```python
# Decorator approach
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

# Method approach (app factory)
def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, not_found)
    return app
```

Blueprint error handlers only handle errors within that blueprint's context. App-level handlers catch all errors. `register_error_handler` is useful in factory patterns where the decorator isn't available at import time.

## Q21: How do you implement database encryption with Flask-SQLAlchemy?
**A:** Column-level encryption using custom types:

```python
from sqlalchemy import LargeBinary, TypeDecorator
from cryptography.fernet import Fernet

class EncryptedString(TypeDecorator):
    impl = LargeBinary
    def __init__(self, key, *args, **kwargs):
        self.fernet = Fernet(key)
        super().__init__(*args, **kwargs)
    def process_bind_param(self, value, dialect):
        if value is not None:
            return self.fernet.encrypt(value.encode())
    def process_result_value(self, value, dialect):
        if value is not None:
            return self.fernet.decrypt(value).decode()
```

Best practices: store keys in environment variables, use separate keys per environment, implement key rotation, use authenticated encryption (Fernet = AES-CBC + HMAC), hash sensitive fields used for lookups.

## Q22: What is Flask's `_app_ctx_stack` and how does it work?
**A:** `_app_ctx_stack` is a `LocalStack` that manages application contexts. When an application context is pushed (`app.app_context().push()`), it's stored on this stack. The `current_app` proxy looks up the stack to find the active application context. Similarly, `_request_ctx_stack` manages request contexts. These stacks are thread-local (each thread has its own). Key behavior: pushing creates a new `AppContext` with the app's `url_adapter`, `g` is stored on the application context, multiple apps can be pushed.

## Q23: How do you implement Flask HTTPS and TLS configuration?
**A:** Flask HTTPS configuration:

```python
# Development (self-signed)
app.run(ssl_context='adhoc')

# With cert files
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain('/path/to/cert.pem', '/path/to/key.pem')
app.run(ssl_context=context)

# Redirect HTTP to HTTPS
@app.before_request
def redirect_to_https():
    if not request.is_secure and request.host != 'localhost:5000':
        return redirect(request.url.replace('http://', 'https://'))
```

Production: terminate TLS at reverse proxy (Nginx, Cloudflare, ALB). Configure Flask for proxy: `app.config['PREFERRED_URL_SCHEME'] = 'https'`. Use WSGI middleware `ProxyFix` to get correct scheme.

## Q24: Explain Flask's `json.provider` and custom JSON handling.
**A:** Flask 2.3+ uses a JSON provider pattern:

```python
from flask.json.provider import JSONProvider
import orjson

class ORJSONProvider(JSONProvider):
    def dumps(self, obj, **kwargs):
        return orjson.dumps(obj).decode()
    def loads(self, s, **kwargs):
        return orjson.loads(s)

app = Flask(__name__)
app.json = ORJSONProvider(app)
```

Built-in provider: `DefaultJSONProvider`. Custom providers control `dumps()` and `loads()`. Benefits: consistent serialization across views, session, and `jsonify`. For large JSON, `orjson` provides 3-5x speedup over standard `json`.

## Q25: How do you implement Flask request validation with Marshmallow?
**A:** Flask-Marshmallow + Marshmallow:

```python
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields, validate, ValidationError

class UserSchema(ma.Schema):
    name = fields.String(required=True, validate=validate.Length(min=1, max=100))
    email = fields.Email(required=True)
    age = fields.Integer(validate=validate.Range(min=0, max=150))

user_schema = UserSchema()

@app.route('/users', methods=['POST'])
def create_user():
    try:
        data = user_schema.load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 422
    user = User(**data)
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201
```

Marshmallow features: nested schemas, pre/post processing hooks (`@pre_load`), custom validators, partial loading. Compared to WTForms: Marshmallow is schema-focused (serialization), WTForms is form-focused.

## Q26: What is Flask's `app.config` and best practices for configuration management?
**A:** Configuration management:

```python
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

app.config.from_object(DevelopmentConfig)
```

Best practices: environment variables for secrets, configuration classes per environment, `.env` for development (never committed), validate required config at startup, don't hardcode config in code, use `app.config.get('KEY', default)` for safe access.

## Q27: How do you implement WebSocket with Flask-SocketIO?
**A:** Flask-SocketIO for real-time bidirectional communication:

```python
from flask_socketio import SocketIO, emit, join_room, leave_room
socketio = SocketIO(app, cors_allowed_origins="*")

@socketio.on('connect')
def handle_connect():
    emit('server_message', {'data': 'Connected!'})

@socketio.on('join')
def handle_join(data):
    join_room(data['room'])
    emit('message', f"{data['username']} joined", to=data['room'])
```

Events: `connect`, `disconnect`, custom events. Features: rooms, namespaces, broadcasting, acknowledgments, binary data. Async modes: eventlet (recommended), gevent, threading. For production: use Redis as message queue for multi-process scaling.

## Q28: Explain Flask's `send_file` and `send_from_directory`.
**A:** Flask file serving:

```python
from flask import send_file, send_from_directory

@app.route('/download/<filename>')
def download_file(filename):
    return send_file(f'reports/{filename}', as_attachment=True, download_name='report.pdf')

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
```

Features: conditional response (ETag, `If-Modified-Since`), range requests, MIME type detection, `Cache-Control` headers. `send_from_directory` is safer than `send_file` (path traversal protection). For static files, mount with `StaticMiddleware`.

## Q29: How do you implement Flask-SQLAlchemy lazy loading and eager loading?
**A:** Relationship loading strategies:

```python
from sqlalchemy.orm import joinedload, selectinload

# Lazy loading (N+1 problem)
users = User.query.all()  # Each user.posts access triggers a query

# Eager loading
users = User.query.options(joinedload(User.posts)).all()  # Single JOIN query
users = User.query.options(selectinload(User.posts)).all()  # Two queries, often faster
```

Strategies: `lazy='select'` (default), `lazy='joined'` (LEFT JOIN), `lazy='subquery'` (subquery), `lazy='dynamic'` (returns query). Eager loading prevents N+1 queries. `joinedload` for single relation; `selectinload` for multiple relations or large collections.

## Q30: What is Flask's `request.get_json()` and when to use it?
**A:** `request.get_json(silent=False, force=False, cache=True)` parses incoming JSON:

```python
data = request.get_json()
data = request.get_json(force=True)    # Parse even with wrong Content-Type
data = request.get_json(silent=True)   # Return None on parse error instead of 400
```

Parameters: `silent=False` — raises 400 on parse error; `force=False` — only parses if Content-Type is JSON; `cache=True` — caches result. For empty bodies: returns `None` (silent) or 400 error. Use `force=True` cautiously.

## Q31: How do you implement Flask blueprint modularization for large applications?
**A:** Blueprint-based application structure:

```python
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('auth/login.html')

def create_app():
    app = Flask(__name__)
    app.register_blueprint(auth_bp)
    return app
```

Blueprint features: `url_prefix`, `template_folder`, `static_folder`, `subdomain`, `url_defaults`. Blueprint resources are scoped. For large apps: organize by feature (auth, admin, blog, API). For API versioning: blueprints per version.

## Q32: Explain Flask's `context processors` and when to use them.
**A:** Context processors inject variables into all templates:

```python
@app.context_processor
def inject_globals():
    return {
        'app_name': 'MyApp',
        'current_year': datetime.utcnow().year,
    }
```

Use cases: site-wide constants, current user in all templates, navigation menus, feature flags. Context processors run for every template render — avoid expensive operations. Blueprint processors only apply to that blueprint's templates. Multiple processors merge their dictionaries.

## Q33: How do you implement Flask-JWT authentication?
**A:** Flask-JWT-Extended:

```python
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

app.config['JWT_SECRET_KEY'] = 'super-secret'
jwt = JWTManager(app)

@app.route('/login', methods=['POST'])
def login():
    user = User.authenticate(request.json['username'], request.json['password'])
    access_token = create_access_token(identity=user.id)
    return jsonify(access_token=access_token)

@app.route('/protected')
@jwt_required()
def protected():
    current_user_id = get_jwt_identity()
    return jsonify(logged_in_as=current_user_id)
```

Features: access + refresh tokens, token freshness, token blocklist (revocation), custom claims, CSRF protection for cookie-based tokens.

## Q34: What is Flask's `message flashing` and how does it work?
**A:** Flask's flash messaging for one-time notifications:

```python
flash('Invalid credentials', 'error')
return redirect(url_for('login'))
```

Template:
```html
{% with messages = get_flashed_messages(with_categories=true) %}
  {% for category, message in messages %}
    <div class="alert alert-{{ category }}">{{ message }}</div>
  {% endfor %}
{% endwith %}
```

`flash(message, category='message')` stores messages in the session. Categories: 'message', 'success', 'error', 'warning', 'info'. For AJAX: return flash messages via JSON.

## Q35: How do you implement Flask database connection pooling with SQLAlchemy?
**A:** SQLAlchemy connection pool configuration:

```python
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_size': 10,
    'max_overflow': 20,
    'pool_timeout': 30,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

Pool sizing: `pool_size = max_workers * (query_time / total_time)`. Monitor database connections. `pool_pre_ping=True` detects stale connections. For multi-worker Gunicorn: each worker has its own pool (total = `workers * pool_size`).

## Q36: Explain Flask's `app.logger` and logging configuration.
**A:** Flask logging configuration:

```python
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler('app.log', maxBytes=1024*1024*10, backupCount=10)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)

app.logger.info('Request received')
app.logger.error(f'Failed to process: {error}')
```

Flask uses Python's standard logging. `app.logger` is `'flask.app'`. For production: use structured format (JSON) for log aggregation, add request context, use correlation IDs, set appropriate log levels.

## Q37: How do you implement Flask-Security for authentication?
**A:** Flask-Security provides comprehensive auth:

```python
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin, login_required

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')
```

Features: registration, login/logout, password reset, email confirmation, role management, remember-me, session-based + token-based auth, JSON API endpoints.

## Q38: What is Flask's `make_response` and when to use it?
**A:** `make_response` creates a Response object from various return types:

```python
response = make_response(render_template('page.html'))
response.headers['X-Custom-Header'] = 'value'
response.set_cookie('key', 'value', max_age=3600, httponly=True)
response.cache_control.max_age = 300
return response
```

`make_response` accepts: a string, a tuple `(body, status, headers)`, or a Response object. After creation, set cookies, headers, status code, cache control, content type, ETag.

## Q39: How do you implement Flask template inheritance and blocks?
**A:** Jinja2 template inheritance:

```html
{# base.html #}
{% block title %}Default Title{% endblock %}
{% block content %}{% endblock %}

{# child.html #}
{% extends "base.html" %}
{% block title %}User Profile{% endblock %}
{% block content %}
    <h1>{{ user.name }}</h1>
{% endblock %}
```

Features: `{{ super() }}` includes parent content, nested blocks, multiple inheritance levels, `{% include %}`, `{% macro %}`, `{% set %}`, `{% import %}`.

## Q40: Explain Flask's `abort` with custom error descriptions.
**A:** `abort` with custom details:

```python
abort(404, description=f"Item {item_id} not found")
abort(403, description="Permission denied")

@app.errorhandler(HTTPException)
def handle_http_error(error):
    return render_template('errors/http_error.html',
        error_code=error.code, description=error.description), error.code
```

Custom exception classes extend `HTTPException`. Properties: `code`, `name`, `description`. Useful for API error messages, user-friendly pages, localization.

## Q41: How do you implement Flask test factories and fixtures?
**A:** Advanced testing with factory pattern:

```python
@pytest.fixture(scope='module')
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def auth_client(client):
    client.post('/auth/login', json={'email': 'test@test.com', 'password': 'password123'})
    return client
```

Best practices: use `app.test_request_context()` for URL generation, test error paths, use `pytest-cov` for coverage, use `factory_boy` for test data, mock external services.

## Q42: What is Flask's `url_defaults` and `url_value_preprocessor`?
**A:** These hooks allow default URL parameter injection:

```python
@blog_bp.url_defaults
def add_locale(endpoint, values):
    if 'locale' not in values:
        values['locale'] = g.get('locale', 'en')

@blog_bp.url_value_preprocessor
def pull_locale(endpoint, values):
    g.locale = values.pop('locale')
```

`url_value_preprocessor` extracts URL params before the view, typically for setting `g` variables. `url_defaults` provides defaults for `url_for`. Useful for language/locale in URLs, subdomains, version prefixes.

## Q43: How do you implement Flask rate limiting with Redis?
**A:** Custom Redis-based rate limiter:

```python
redis_client = redis.Redis.from_url('redis://localhost:6379')

def rate_limit(key_func, limit, window=60):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            key = f"ratelimit:{key_func()}:{request.endpoint}"
            current = redis_client.get(key)
            if current and int(current) >= limit:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            pipe = redis_client.pipeline()
            pipe.incr(key)
            if not current:
                pipe.expire(key, window)
            pipe.execute()
            return f(*args, **kwargs)
        return decorated
    return decorator
```

Algorithms: fixed window, sliding window (sorted sets), token bucket. For distributed: use Redis pipeline for atomic operations.

## Q44: Explain Flask's `safe_join` and file path safety.
**A:** `safe_join` prevents directory traversal:

```python
from flask import safe_join
try:
    filepath = safe_join(app.config['UPLOAD_FOLDER'], filename)
except ValueError:
    abort(404)
```

Security practices: always use `secure_filename()` to sanitize filenames, never join user input with file paths directly, use `safe_join` instead of `os.path.join`, resolve symlinks with `os.path.realpath`, store files outside web root.

## Q45: How do you implement Flask-Admin for admin interfaces?
**A:** Flask-Admin provides automatic admin interfaces:

```python
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

admin = Admin(app, name='MyAdmin', template_mode='bootstrap4')

class UserAdmin(ModelView):
    column_list = ['id', 'email', 'username', 'active']
    column_searchable_list = ['email', 'username']
    can_create = True
    can_edit = True
    can_delete = True

admin.add_view(UserAdmin(User, db.session))
```

Features: CRUD for SQLAlchemy models, file management, Redis console, role-based access, customizable templates, batch operations, CSV export.

## Q46: What is Flask's `app.before_first_request` and its deprecation?
**A:** `before_first_request` runs once before the first request (deprecated in Flask 2.3+). Deprecated because: doesn't work with WSGI servers that fork workers (Gunicorn), creates race conditions in multi-worker environments. Alternatives: app factory with initialization, CLI command for setup, lazy initialization.

## Q47: How do you implement Flask database performance monitoring?
**A:** SQLAlchemy query profiling:

```python
from sqlalchemy import event

@event.listens_for(engine, 'before_cursor_execute')
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info['query_start_time'] = time.time()

@event.listens_for(engine, 'after_cursor_execute')
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total = time.time() - conn.info['query_start_time']
    app.logger.debug(f'Query: {statement[:100]}... ({total:.3f}s)')
```

For production: APM tools (Datadog, New Relic, Sentry), log slow queries, monitor connection pool metrics.

## Q48: Explain Flask's `request.remote_addr` and proxy configurations.
**A:** Behind proxies, `request.remote_addr` shows the proxy IP. Use `ProxyFix`:

```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)
```

`x_for=1` means one proxy level. `request.access_route` shows all proxy IPs. Without `ProxyFix`, `request.remote_addr` shows the last proxy IP. Security: only enable when behind a trusted proxy.

## Q49: How do you implement Flask-APScheduler for scheduled tasks?
**A:** APScheduler integration:

```python
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

scheduler = BackgroundScheduler()
scheduler.add_job(func=clean_expired_sessions, trigger=CronTrigger(hour=3, minute=0))
scheduler.start()

def clean_expired_sessions():
    with app.app_context():
        Session.query.filter(Session.expires_at < datetime.utcnow()).delete()
        db.session.commit()
```

Triggers: `IntervalTrigger`, `CronTrigger`, `DateTrigger`. For persistence: `SQLAlchemyJobStore`. For distributed systems: use Redis locking, run scheduler as separate process.

## Q50: What is Flask's `json.security` and security considerations?
**A:** Flask JSON security settings:

```python
app.config['JSON_AS_ASCII'] = True      # Escape non-ASCII
app.config['JSON_SORT_KEYS'] = False     # Preserve key order
```

Security issues: JSONP callback injection, JSON hijacking (prefix with `while(1);`), XXE injection, prototype pollution. For public APIs: set `JSON_AS_ASCII=True` to prevent charset-based attacks.

## Q51: How do you implement Flask-Bootstrap integration?
**A:** Flask-Bootstrap:

```python
from flask_bootstrap import Bootstrap
Bootstrap(app)
```

```html
{% extends "bootstrap/base.html" %}
{% import "bootstrap/wtf.html" as wtf %}
{% block content %}
<div class="container">
    {{ wtf.quick_form(form) }}
</div>
{% endblock %}
```

Features: Bootstrap CSS/JS, `wtf.quick_form()` with Bootstrap styling. For Bootstrap 5, use `bootstrap-flask`.

## Q52: Explain Flask's `app.url_map` and routing introspection.
**A:** `app.url_map` provides routing information:

```python
@app.route('/debug/routes')
def list_routes():
    routes = []
    for rule in app.url_map.iter_rules():
        routes.append({
            'endpoint': rule.endpoint,
            'methods': list(rule.methods - {'HEAD', 'OPTIONS'}),
            'path': rule.rule,
        })
    return jsonify(routes)
```

Useful for: sitemaps, route documentation, debugging, permission checking, dynamic navigation.

## Q53: How do you implement Flask-Celery integration?
**A:** Flask-Celery for distributed tasks:

```python
def make_celery(app):
    celery = Celery(app.import_name, backend=app.config['CELERY_RESULT_BACKEND'],
                    broker=app.config['CELERY_BROKER_URL'])
    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)
    celery.Task = ContextTask
    return celery
```

Features: task queues, retry logic, task scheduling (Celery Beat), task grouping/chaining, rate limiting, monitoring (Flower). Start: `celery -A app.celery worker --loglevel=info`.

## Q54: What is Flask's `request.range` and how does it handle byte ranges?
**A:** Flask handles `Range` headers for partial content:

```python
range_header = request.headers.get('Range', None)
if range_header:
    # Parse: bytes=start-end
    # Return 206 Partial Content with Content-Range header
```

`send_file` handles range requests automatically. Essential for: video/audio seeking, resume downloads, parallel downloads.

## Q55: How do you implement Flask database triggers and events?
**A:** SQLAlchemy event listeners:

```python
from sqlalchemy import event

@event.listens_for(User, 'before_insert')
def user_before_insert(mapper, connection, target):
    target.created_at = datetime.utcnow()
```

Events: `before_insert`, `after_insert`, `before_update`, `after_update`, `before_delete`, `after_delete`. Use for timestamps, audit logging, data validation, derived fields, cache invalidation.

## Q56: Explain Flask's `app.extensions` and extension registration.
**A:** `app.extensions` is a dict of registered extensions:

```python
class MyExtension:
    def init_app(self, app):
        if not hasattr(app, 'extensions'):
            app.extensions = {}
        app.extensions['my_extension'] = self
```

Standard pattern: `ext = Extension(); ext.init_app(app)`. Access via `current_app.extensions['my_extension']`. This avoids circular imports and supports lazy initialization.

## Q57: How do you implement Flask two-factor authentication (2FA)?
**A:** TOTP-based 2FA with pyotp:

```python
import pyotp
secret = pyotp.random_base32()
totp = pyotp.TOTP(secret)
uri = totp.provisioning_uri(name=user.email, issuer_name="MyApp")
# Generate QR code from URI for authenticator app
if totp.verify(token):
    # Token is valid
```

Best practices: store secrets encrypted, provide backup codes, support multiple authenticator apps, implement rate limiting on verification, support WebAuthn.

## Q58: What is Flask's `wsgi_app` method and WSGI middleware?
**A:** `app.wsgi_app(environ, start_response)` is Flask's WSGI callable:

```python
class TimingMiddleware:
    def __call__(self, environ, start_response):
        start = time.time()
        def custom_start_response(status, headers, exc_info=None):
            headers.append(('X-Response-Time', str(int((time.time()-start)*1000))))
            return start_response(status, headers, exc_info)
        return self.app(environ, custom_start_response)

app.wsgi_app = TimingMiddleware(app.wsgi_app)
```

Common middleware: `ProxyFix`, `SharedDataMiddleware`, `ProfilerMiddleware`. Middleware order: outer wraps inner.

## Q59: How do you implement Flask MongoDB with MongoEngine?
**A:** Flask-MongoEngine:

```python
from flask_mongoengine import MongoEngine
app.config['MONGODB_SETTINGS'] = {'db': 'myapp', 'host': 'localhost'}
db = MongoEngine(app)

class Post(db.Document):
    title = db.StringField(required=True, max_length=200)
    content = db.StringField()
    tags = db.ListField(db.StringField())
    meta = {'indexes': ['title']}

posts = Post.objects(published=True).order_by('-created_at').limit(20)
```

Features: schema validation, references, embedded documents, indexing, aggregation pipeline, signals (pre_save, post_save).

## Q60: Explain Flask's `_compat` module and compatibility layer.
**A:** Flask's internal `_compat` module (largely removed in Flask 2.3+) handled Python version differences. Modern Flask targets Python 3.8+. Extension authors should: target Python 3.8+ only, use `from __future__ import annotations`, prefer `asyncio.run`. Older compat helpers included `string_types`, `text_type`, `iteritems`, `reraise`.

## Q61: How do you implement Flask-Excel/CSV import/export?
**A:** CSV export:

```python
def generate():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['ID', 'Name', 'Email'])
    yield output.getvalue()
    for user in users:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([user.id, user.name, user.email])
        yield output.getvalue()

return Response(generate(), mimetype='text/csv',
    headers={'Content-Disposition': 'attachment; filename=users.csv'})
```

CSV import: `csv.DictReader(file.stream)` with validation. Excel: use `openpyxl` with `BytesIO` output.

## Q62: What is Flask's `app.context_processor` vs `template_global`?
**A:** `context_processor` returns a dict merged into template context. `template_global()` registers a global Jinja2 function:

```python
@app.context_processor
def utility_processor():
    return dict(site_name='MyApp', format_price=lambda amt: f"${amt:.2f}")

@app.template_global()
def is_admin(user):
    return user and user.role == 'admin'

@app.template_filter()
def capitalize_words(text):
    return ' '.join(w.capitalize() for w in text.split())
```

`template_filter()` creates a Jinja2 filter. `template_test()` creates a Jinja2 test.

## Q63: How do you implement Flask full-text search with SQLAlchemy?
**A:** PostgreSQL full-text search:

```python
from sqlalchemy import func, TSVECTOR

class Article(db.Model):
    search_vector = Column(TSVECTOR)
    __table_args__ = (db.Index('ix_article_search', search_vector, postgresql_using='gin'),)

query = Article.query.filter(
    Article.search_vector.op('@@')(func.plainto_tsquery('english', q))
).order_by(func.ts_rank(Article.search_vector, func.plainto_tsquery('english', q)).desc())
```

For Elasticsearch: use `elasticsearch-dsl`. For SQLite: use FTS5.

## Q64: Explain Flask's `request.environ` and WSGI environment.
**A:** `request.environ` exposes the full WSGI environment dict with: CGI variables (`REQUEST_METHOD`, `PATH_INFO`), HTTP headers (`HTTP_*`), WSGI-specific (`wsgi.*`), custom middleware-added keys. Access directly for: lower-level debugging, middleware communication, reading non-standard headers.

## Q65: How do you implement Flask-SSE (Server-Sent Events)?
**A:** SSE for real-time updates:

```python
@app.route('/events')
def event_stream():
    def generate():
        while True:
            yield f"data: {json.dumps({'time': time.time()})}\n\n"
            time.sleep(2)
    return Response(stream_with_context(generate()),
        mimetype='text/event-stream',
        headers={'Cache-Control': 'no-cache', 'X-Accel-Buffering': 'no'})
```

SSE considerations: one-way server→client, works with `EventSource` in browser, limited to ~6 connections per browser (HTTP/1.1).

## Q66: What is Flask's `_find_handler` and error handling internals?
**A:** When an exception occurs: Flask checks blueprint error handlers, then application error handlers, then defaults. For `HTTPException`, checks `error.code` first, then exception class. The handler registry is in `app.error_handler_spec` dict.

## Q67: How do you implement Flask-HTMX integration?
**A:** HTMX for dynamic pages:

```python
@app.route('/users')
def list_users():
    if request.headers.get('HX-Request'):
        return render_template('partials/user_list.html', users=users)
    return render_template('users.html', users=users)
```

HTMX features: `hx-get/post`, `hx-target`, `hx-swap`, `hx-trigger`, `HX-Trigger` response header. CSRF: include token in `hx-headers`.

## Q68: Explain Flask's `make_null_session` and session implementations.
**A:** Flask supports multiple session backends:

```python
class RedisSessionInterface(SessionInterface):
    def open_session(self, app, request):
        sid = request.cookies.get('session')
        if sid:
            data = self.redis.get(f'session:{sid}')
            if data:
                return RedisSession(sid, pickle.loads(data))
        return RedisSession(generate_sid())
```

Backends: `SecureCookieSession` (default, cookie-based), Redis (server-side, shared across workers), Database (SQLAlchemy), Filesystem. Flask-Session provides multiple backends.

## Q69: How do you implement Flask file upload with progress bar?
**A:** Chunked upload:

```python
@app.route('/upload/init', methods=['POST'])
def init_upload():
    upload_id = str(uuid.uuid4())
    os.makedirs(os.path.join(UPLOAD_FOLDER, upload_id))
    return jsonify({'upload_id': upload_id, 'chunk_size': 1024*1024})

@app.route('/upload/<upload_id>/<int:chunk_index>', methods=['POST'])
def upload_chunk(upload_id, chunk_index):
    chunk = request.files['chunk']
    chunk.save(os.path.join(UPLOAD_FOLDER, upload_id, str(chunk_index)))
    return jsonify({'status': 'ok'})
```

Client tracks: `chunks_completed / total_chunks = progress`. Or use `XMLHttpRequest.upload.onprogress`.

## Q70: What is Flask's `session.permanent` and session lifetime?
**A:** `session.permanent` controls session expiration:

```python
session.permanent = True  # Uses PERMANENT_SESSION_LIFETIME
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=31)
app.config['SESSION_REFRESH_EACH_REQUEST'] = True  # Refresh on activity
```

Non-permanent sessions expire when browser closes. For cookie-based sessions, expiration is in the signed cookie.

## Q71: How do you implement Flask testing with SQLite in-memory database?
**A:** Isolated database testing:

```python
@pytest.fixture(scope='function')
def app():
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()
```

Best practices: `scope='function'` for isolation, seed minimal test data, test all CRUD, test errors, use factories.

## Q72: Explain Flask's `process_response` and `finalize_request`.
**A:** `process_response` runs `after_request` handlers. `finalize_request` handles the full lifecycle: (1) view returns, (2) `make_response` converts to Response, (3) `process_response` runs `after_request` handlers, (4) `finalize_request` runs `teardown_request`, (5) WSGI response is sent.

## Q73: How do you implement Flask-Alembic for database migrations?
**A:** Alembic with Flask-Migrate:

```bash
flask db init
flask db migrate -m "create users"
flask db upgrade
flask db downgrade
flask db history
flask db current
```

Best practices: review auto-generated migrations, write downgrade methods, test against production-like data, deploy migrations as separate step.

## Q74: What is Flask's `request.trusted_hosts` and host header validation?
**A:** Host header validation prevents host injection:

```python
app.config['TRUSTED_HOSTS'] = ['myapp.com', 'www.myapp.com']

@app.before_request
def validate_host():
    if request.host not in app.config['TRUSTED_HOSTS']:
        abort(400, 'Untrusted host')
```

Host header attacks: password reset poisoning, cache poisoning, SSRF. Always validate host headers in production.

## Q75: How do you implement Flask API documentation with Flasgger?
**A:** Flasgger generates Swagger docs:

```python
from flasgger import Swagger, swag_from
Swagger(app)

@app.route('/users/<int:user_id>')
@swag_from({
    'parameters': [{'name': 'user_id', 'in': 'path', 'type': 'integer'}],
    'responses': {200: {'description': 'A single user'}}
})
def get_user(user_id):
    return jsonify(user.to_dict())
```

Features: auto-generate Swagger UI at `/apidocs/`, parse OpenAPI from docstrings, validate requests against schema, support YAML/JSON spec files.

## Q76: Explain Flask's `app.url_build_error_handlers` and URL generation errors.
**A:** Custom handling for URL generation failures:

```python
@app.url_build_error_handlers.append
def handle_build_error(error, endpoint, values):
    app.logger.warning(f'Failed to build URL for {endpoint}: {error}')
    return url_for('index')
```

Errors occur when: endpoint doesn't exist, required URL parameters missing, blueprint not registered.

## Q77: How do you implement Flask background task tracking?
**A:** Task tracking system:

```python
tasks = {}  # Use Redis in production

def create_task(name):
    task_id = str(uuid4())
    tasks[task_id] = {'id': task_id, 'status': 'pending', 'progress': 0}
    return task_id

@app.route('/tasks/<task_id>')
def get_task_status(task_id):
    task = tasks.get(task_id)
    if not task:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(task)
```

For distributed tasks: use Celery with result backend. Task cleanup: periodic job to remove old tasks.

## Q78: What is Flask's `request.access_route` and trusted proxies?
**A:** `access_route` provides the IP chain from `X-Forwarded-For`:

```python
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=3)

# request.remote_addr — real client IP (after ProxyFix)
# request.access_route — list of all proxy IPs
```

Without `ProxyFix`, `remote_addr` is the direct connection IP (proxy). Security: only trust proxies you control.

## Q79: How do you implement Flask-GraphQL integration?
**A:** GraphQL with Graphene:

```python
from graphene import ObjectType, String, Int, Field, Schema
from flask_graphql import GraphQLView

class Query(ObjectType):
    user = Field(UserType, id=Int())
    def resolve_user(self, info, id):
        return get_user(id)

schema = Schema(query=Query)
app.add_url_rule('/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))
```

For production: add authentication, query depth limiting, rate limit by complexity, use dataloader, disable GraphiQL.

## Q80: Explain Flask's `app.logger` hierarchy and propagation.
**A:** Logger hierarchy: `app.logger` is `'flask.app'`, propagates to `'flask'` → root logger. `logging.getLogger('werkzeug')` for dev server logs. Module-level: `log = logging.getLogger(__name__)`. Log propagation can be disabled: `app.logger.propagate = False`.

## Q81: How do you implement Flask-JSON-RPC APIs?
**A:** JSON-RPC protocol:

```python
class JSONRPC:
    def handle(self):
        data = request.get_json()
        method = self.methods.get(data['method'])
        result = method(*data.get('params', []))
        return jsonify({'jsonrpc': '2.0', 'result': result, 'id': data['id']})
```

Features: batch requests, named and positional params, notifications (no response).

## Q82: What is Flask's `app.secret_key` and how session signing works?
**A:** `secret_key` is used for cryptographic session signing. Flow: session data → serialized (JSON) → compressed (zlib) → signed (HMAC-SHA1) → base64 → cookie. Verification: server reads cookie, verifies signature, decompresses, deserializes. Invalid signature → empty session. Never hardcode secrets.

## Q83: How do you implement Flask-OpenAPI/Swagger with APISpec?
**A:** APISpec for OpenAPI:

```python
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

spec = APISpec(title='My API', version='1.0.0', plugins=[MarshmallowPlugin()])
spec.path(view=get_user)  # Register from docstring
```

Alternative to Flasgger. Generate OpenAPI schema programmatically from Marshmallow schemas and view functions.

## Q84: What is Flask's `app.create_jinja_environment`?
**A:** Custom Jinja2 environment:

```python
from jinja2 import Environment

def create_jinja_environment():
    env = super().create_jinja_environment()
    env.globals['my_global'] = lambda: 'value'
    env.policies['url.new_style'] = True
    return env

app.create_jinja_environment = create_jinja_environment
```

Customize: globals, filters, tests, policies, extensions, autoescape, undefined behavior.

## Q85: How do you implement Flask RESTful API with Flask-RESTful?
**A:** Flask-RESTful for resource-based APIs:

```python
from flask_restful import Api, Resource

api = Api(app)

class UserResource(Resource):
    def get(self, user_id):
        user = User.query.get_or_404(user_id)
        return user.to_dict()
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        user.name = request.json['name']
        db.session.commit()
        return user.to_dict()
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return '', 204

api.add_resource(UserResource, '/users/<int:user_id>')
```

Features: automatic routing, request parsing (`reqparse`), output marshalling, endpoint naming.

## Q86: What is Flask's `app.preprocess_request` and `app.process_response`?
**A:** `preprocess_request` runs all `before_request` handlers. Returns None if all pass, or a Response if one short-circuits. `process_response` runs all `after_request` handlers, then saves session, then runs `teardown_request`. These are internal methods but can be overridden for custom request processing.

## Q87: How do you implement Flask-Compress for response compression?
**A:** Flask-Compress:

```python
from flask_compress import Compress
compress = Compress()
compress.init_app(app)

app.config['COMPRESS_MIMETYPES'] = ['text/html', 'application/json']
app.config['COMPRESS_LEVEL'] = 6
app.config['COMPRESS_MIN_SIZE'] = 500
```

Compresses responses with gzip/deflate. More efficient than application-level compression. Consider using at reverse proxy level (Nginx) instead.

## Q88: What is Flask's `app.auto_find_instance_path`?
**A:** `auto_find_instance_path` (default True) automatically finds the instance folder relative to the app's package/module. The instance folder is used for configuration files, databases, downloads. Set `instance_path` explicitly for custom location. Instance folder is outside the package, making it suitable for runtime-modifiable files.

## Q89: How do you implement Flask API versioning with Accept headers?
**A:** Content negotiation versioning:

```python
@app.before_request
def api_versioning():
    accept = request.headers.get('Accept', '')
    if 'application/vnd.myapp.v2+json' in accept:
        g.api_version = 2
    elif 'application/vnd.myapp.v1+json' in accept:
        g.api_version = 1
    else:
        g.api_version = 1

@app.route('/users')
def list_users():
    if g.api_version == 2:
        return jsonify([user.to_v2_dict() for user in User.query.all()])
    return jsonify([user.to_dict() for user in User.query.all()])
```

More RESTful than URL-based versioning but less discoverable.

## Q90: What is Flask's `app.subdomain_matching`?
**A:** Subdomain matching enables routing based on subdomain:

```python
app.config['SERVER_NAME'] = 'myapp.com'
app.url_map.default_subdomain = ''

@ app.route('/', subdomain='<subdomain>')
def subdomain_index(subdomain):
    return f"Welcome to {subdomain}.myapp.com"

api_bp = Blueprint('api', __name__, subdomain='api')
```

Useful for: multi-tenant apps, API subdomain (`api.myapp.com`), admin subdomain (`admin.myapp.com`).

## Q91: How do you implement Flask-Mail for sending emails?
**A:** Flask-Mail:

```python
from flask_mail import Mail, Message

mail = Mail(app)

@app.route('/send-email')
def send_email():
    msg = Message('Hello', recipients=['user@example.com'])
    msg.body = 'This is a test email'
    msg.html = '<h1>Test</h1>'
    mail.send(msg)
    return 'Email sent'
```

Configuration: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`. For async: use threading with `app.app_context()`.

## Q92: What is Flask's `app.open_resource`?
**A:** `app.open_resource(resource, mode='rb')` opens resources relative to the app's root path:

```python
with app.open_resource('static/data/terms.txt') as f:
    content = f.read()
```

Useful for reading packaged resources (files bundled with the application). Works with both development and installed packages.

## Q93: How do you implement Flask error logging to external services?
**A:** Sentry integration:

```python
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

sentry_sdk.init(dsn='https://...', integrations=[FlaskIntegration()])

@app.errorhandler(Exception)
def handle_exception(error):
    sentry_sdk.capture_exception(error)
    return jsonify({'error': 'Internal server error'}), 500
```

Other services: Datadog, New Relic, Logstash. Ensure PII is not logged.

## Q94: What is Flask's `app.root_path` and `app.instance_path`?
**A:** `app.root_path` is the filesystem path of the application package (where Flask looks for templates, static files). `app.instance_path` is the path to the instance folder (for runtime files). Set explicitly: `Flask(__name__, root_path='/path', instance_path='/path')`. These paths are used by `app.open_resource()`, `send_from_directory`, and template/static file lookups.

## Q95: How do you implement Flask background task queues with RQ?
**A:** RQ (Redis Queue) integration:

```python
from rq import Queue
from redis import Redis

redis_conn = Redis()
queue = Queue(connection=redis_conn)

@app.route('/process')
def process():
    job = queue.enqueue(long_task, args=(data,))
    return jsonify({'job_id': job.id})

@app.route('/jobs/<job_id>')
def job_status(job_id):
    job = queue.fetch_job(job_id)
    return jsonify({'status': job.get_status(), 'result': job.result})
```

Run worker: `rq worker`. RQ features: job retry, job scheduling, job dependencies, result TTL. Lighter than Celery.

## Q96: What is Flask's `app.aborter` and custom abort handling?
**A:** `app.aborter` is a `Aborter` instance that maps status codes to exception classes:

```python
from werkzeug.exceptions import Aborter

app.aborter = Aborter(mapping={
    404: CustomNotFound,
    403: CustomForbidden,
})
```

Custom abort classes can have custom behavior (logging, metrics). The aborter is what `abort()` calls internally.

## Q97: How do you implement Flask-Admin custom views?
**A:** Custom admin views:

```python
from flask_admin import BaseView, expose

class AnalyticsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/analytics.html')
    
    @expose('/reports')
    def reports(self):
        return self.render('admin/reports.html')

admin.add_view(AnalyticsView(name='Analytics', endpoint='analytics'))
```

BaseView provides: `@expose()` for routing, `render()` for template rendering, `is_accessible()` for access control.

## Q98: What is Flask's `app.prepare_import` and extension loading?
**A:** `prepare_import()` is an internal method called during `Flask()` initialization. It sets up the import path for the application package. Understanding this helps with: debugging import errors, configuring package discovery, and setting up complex application structures. Modern Flask doesn't require significant import path manipulation.

## Q99: How do you implement Flask-Pydantic integration?
**A:** Flask-Pydantic for request/response validation:

```python
from flask_pydantic import validate

@app.route('/users/<user_id>')
@validate(query=UserQuery, body=UserBody)
def update_user():
    # request.query_params validated as UserQuery
    # request.body_params validated as UserBody
    return UserResponse(user=...).model_dump()
```

Alternative: manual Pydantic validation:

```python
from pydantic import BaseModel

class UserSchema(BaseModel):
    name: str
    email: str

@app.route('/users', methods=['POST'])
def create_user():
    user = UserSchema(**request.json)
    return user.model_dump()
```

## Q100: How do you implement Flask-CORS for specific origins?
**A:** Flask-CORS configuration:

```python
from flask_cors import CORS

CORS(app, origins=['https://myapp.com', 'https://admin.myapp.com'],
     methods=['GET', 'POST', 'PUT', 'DELETE'],
     allow_headers=['Authorization', 'Content-Type'],
     supports_credentials=True,
     max_age=3600)
```

Per-route CORS:

```python
@cross_origin(origin='https://api.myapp.com')
@app.route('/api/data')
def api_data():
    return jsonify(data)
```

Avoid `origins=['*']` with credentials. Use specific origins in production.
