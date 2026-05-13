# Flask Interview Questions and Answers

## Q1: What is Flask?
**A:** Flask is a lightweight WSGI web application framework in Python, created by Armin Ronacher in 2010. It's designed to be simple, extensible, and minimalistic (micro-framework). Flask provides routing, request handling, templating (Jinja2), and integrates with various extensions for databases, authentication, and more.

## Q2: What are the key features of Flask?
**A:** Key features include: lightweight and modular design, built-in development server and debugger, Jinja2 templating, routing with URL parameters, request/response handling, session management, secure cookies, RESTful request dispatching, WSGI compliance, extensive extension ecosystem (Flask-SQLAlchemy, Flask-Login, Flask-Migrate).

## Q3: What is the difference between Flask and Django?
**A:** Flask is a micro-framework with minimal built-in features, giving developers freedom to choose components. Django is a full-stack framework with ORM, admin panel, authentication, and more built-in. Flask is more flexible and lightweight; Django provides more out-of-the-box. Flask suits smaller projects and microservices; Django suits larger applications.

## Q4: How do you create a minimal Flask application?
**A:** `from flask import Flask; app = Flask(__name__); @app.route('/') def hello(): return 'Hello, World!'`. Run with `flask run` or `python app.py` with `app.run()`. Set `FLASK_APP=app.py` and `FLASK_ENV=development` for debug mode.

## Q5: How does Flask handle routing?
**A:** Routes are defined with `@app.route(rule, methods=["GET"])` decorator. The rule is a URL pattern with optional variable parts: `@app.route('/user/<username>')`. Converters specify types: `<int:post_id>`, `<float:value>`, `<path:subpath>`, `<uuid:uuid>`. Multiple methods: `methods=["GET", "POST"]`.

## Q6: How do you handle URL parameters in Flask?
**A:** Variable rules in routes: `@app.route('/post/<int:post_id>')`. The function receives `post_id` as argument. Query parameters via `request.args`: `request.args.get('page', 1)`. URL building: `url_for('function_name', param=value)`. Avoid hardcoding URLs.

## Q7: What is Jinja2 and how is it used in Flask?
**A:** Jinja2 is Flask's default templating engine. Templates are HTML files with placeholders: `{{ variable }}`, control structures: `{% for item in items %}`, filters: `{{ name|upper }}`, inheritance: `{% extends "base.html" %}`. Rendered with `render_template('template.html', variable=value)`.

## Q8: How does Flask handle request data?
**A:** `request.form` for POST form data, `request.args` for GET query params, `request.json` for JSON body, `request.data` for raw data, `request.files` for uploaded files, `request.headers` for HTTP headers, `request.cookies` for cookies, `request.method` for HTTP method.

## Q9: How do you handle JSON requests and responses in Flask?
**A:** JSON request: `data = request.get_json()` (returns parsed JSON dict). JSON response: `return jsonify({"key": "value"})` (sets Content-Type to application/json). `jsonify` handles serialization of dicts, lists, and other types. For custom serialization, use `json.dumps` with `Response`.

## Q10: What are Flask blueprints?
**A:** Blueprints organize Flask applications into modular components. Define: `bp = Blueprint('auth', __name__, url_prefix='/auth')`. Register: `app.register_blueprint(bp)`. Blueprints can have their own templates, static files, and error handlers. Essential for scaling Flask applications with separate domains.

## Q11: How do you handle static files in Flask?
**A:** Static files go in `static/` folder by default. Access: `url_for('static', filename='style.css')` which generates `/static/style.css`. Custom static folder: `app = Flask(__name__, static_folder='assets')`. Use `send_from_directory` for serving files from other directories.

## Q12: How does Flask handle file uploads?
**A:** HTML form with `enctype="multipart/form-data"`. View: `file = request.files['file']; filename = secure_filename(file.filename); file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))`. Use `werkzeug.utils.secure_filename` to sanitize filenames. Validate file size with `MAX_CONTENT_LENGTH` config.

## Q13: What is the Flask application context?
**A:** Application context (`current_app`, `g`) is pushed when a request comes in. `current_app` provides access to the Flask application instance. `g` is a namespace for request-scoped data (like DB connection). Contexts are created and destroyed per request. Manual push: `with app.app_context():`.

## Q14: What is the Flask request context?
**A:** Request context (`request`, `session`) is created per request. `request` contains all HTTP request data. `session` stores per-user data across requests (signed cookies). Contexts are thread/worker-local. Accessible only during request handling unless manually pushed.

## Q15: How does Flask handle sessions?
**A:** Flask sessions store data in signed cookies (client-side). Configure `SECRET_KEY` for signing. Usage: `session['username'] = user.name; username = session.get('username'); session.pop('username', None)`. For server-side sessions, use Flask-Session extension (Redis, filesystem, database).

## Q16: What is `g` in Flask?
**A:** `g` is a thread-local namespace for storing data during a request. Commonly used for database connections: `g.db = get_db()`. Clean up at end of request with `teardown_appcontext` handler. Data in `g` persists only within the same request/application context.

## Q17: How does Flask handle error handling?
**A:** `@app.errorhandler(404) def not_found(error): return render_template('404.html'), 404`. Error handlers for specific HTTP codes. `abort(status_code)` raises errors. Custom exception classes with error handlers. `app.handle_exception` for unhandled exceptions. Returns (response, status_code) tuple.

## Q18: What is `abort()` in Flask?
**A:** `from flask import abort; abort(404)` raises an `HTTPException`. Handled by registered error handlers. Can include description: `abort(404, description="Resource not found")`. Common codes: 400 (bad request), 401 (unauthorized), 403 (forbidden), 404 (not found), 500 (server error).

## Q19: How do you handle redirects in Flask?
**A:** `from flask import redirect; return redirect(url_for('index'))`. `redirect(location, code=302)`. Common codes: 301 (permanent), 302 (found/temporary), 303 (see other), 307 (temporary), 308 (permanent). `url_for` generates URLs from view function names.

## Q20: How does Flask handle cookies?
**A:** Set: `response.set_cookie('key', 'value', max_age=3600)`. Get: `request.cookies.get('key')`. Delete: `response.delete_cookie('key')`. Options: max_age, expires, path, domain, secure, httponly, samesite. For signed cookies, use `session` instead.

## Q21: What is `make_response` in Flask?
**A:** `make_response()` creates a response object from various return types: string, dict (jsonify), tuple `(response, status, headers)`, or Response object. Allows modifying response before returning: `resp = make_response(render_template(...)); resp.headers['X-Custom'] = 'value'`.

## Q22: How do you implement before and after request hooks?
**A:** `@app.before_request` runs before each request (setup DB, auth check). `@app.after_request` runs after each request (modify response, add headers). `@app.teardown_request` runs after response is sent (cleanup). Return response or None in before_request to halt processing.

## Q23: What is `teardown_appcontext` in Flask?
**A:** `@app.teardown_appcontext` registers a function called when the application context is popped (typically at request end). Used for cleanup: closing database connections, releasing resources. Receives the exception (if any) that occurred during the request.

## Q24: How does Flask handle database integration?
**A:** Flask doesn't include an ORM. Common integrations: Flask-SQLAlchemy (SQLAlchemy ORM), Flask-MongoEngine (MongoDB), Flask-Peewee (Peewee ORM). Pattern: configure database URI in `app.config`, initialize extension (`db = SQLAlchemy(app)`), define models, use `db.session` for operations.

## Q25: What is Flask-SQLAlchemy?
**A:** Flask-SQLAlchemy adds SQLAlchemy ORM support to Flask. Provides: `db.Model` (declarative base), `db.Column`, `db.relationship`, `db.session`. Simplifies configuration with `SQLALCHEMY_DATABASE_URI`. Supports migrations via Flask-Migrate. Automatically handles session lifecycle per request.

## Q26: How do you handle database migrations in Flask?
**A:** Using Flask-Migrate (Alembic wrapper). Initialize: `flask db init`. Generate: `flask db migrate -m "message"`. Apply: `flask db upgrade`. Rollback: `flask db downgrade`. Manage: `flask db history`, `flask db stamp`. Migrations are version-controlled Python scripts.

## Q27: How does Flask handle forms?
**A:** HTML forms processed with `request.form`. For validation: Flask-WTF extension (WTForms integration). Define form classes: `class LoginForm(FlaskForm): username = StringField('Username', validators=[DataRequired()])`. Render with `form.username()` and validate with `form.validate_on_submit()`.

## Q28: What is Flask-WTF?
**A:** Flask-WTF integrates WTForms with Flask for form handling and CSRF protection. Features: form classes with field types and validators, CSRF token generation/validation, file upload handling, reCAPTCHA support, and internationalization. CSRF protection is automatic with `SECRET_KEY` configured.

## Q29: How does Flask handle CSRF protection?
**A:** Flask-WTF provides built-in CSRF protection. Include `{{ form.hidden_tag() }}` in forms. CSRF token is generated per session and validated on POST. Without Flask-WTF, manually check tokens: compare token from form with session-stored token. Always use CSRF protection for state-changing requests.

## Q30: What is `url_for` in Flask?
**A:** `url_for('view_function', param=value, _external=True)` generates URLs from view function names. Handles URL changes automatically. Accepts query parameters as keyword args. `_external=True` generates absolute URLs. Example: `url_for('user.profile', username='john')` -> `/user/john`.

## Q31: How do you implement authentication in Flask?
**A:** Common approach: Flask-Login extension. User model with `is_authenticated`, `is_active`, `is_anonymous`, `get_id()`. Login: `login_user(user)`. Logout: `logout_user()`. Protect views: `@login_required` decorator. `current_user` proxy for logged-in user. Session-based by default.

## Q32: What is Flask-Login?
**A:** Flask-Login manages user sessions. Provides: `LoginManager` (setup), `login_user()` (log in), `logout_user()` (log out), `@login_required` (decorator), `current_user` (proxy). Requires user model with methods: `is_authenticated`, `is_active`, `is_anonymous`, `get_id()`. User loader callback loads user from ID.

## Q33: What is Flask-Principal?
**A:** Flask-Principal provides identity management and resource-level permissions. Concepts: Identity (current user), Need (permission requirement), Permission (check). Example: `admin_permission = Permission(RoleNeed('admin'))`. Used for fine-grained access control beyond simple login/logout.

## Q34: How does Flask handle configuration management?
**A:** `app.config` dictionary stores configuration. Sources: hardcoded (`app.config['KEY'] = 'value'`), object-based (`app.config.from_object(ConfigClass)`), file-based (`app.config.from_pyfile('config.cfg')`), environment vars (`app.config.from_prefixed_env()`). Common pattern: class-based config per environment.

## Q35: What is the `flask` command-line interface?
**A:** `flask run` starts dev server. `flask shell` opens Python shell with app context. `flask routes` lists all registered routes. Custom CLI commands with `@app.cli.command()`. Options: `--host`, `--port`, `--debug`, `--cert` (HTTPS). Requires `FLASK_APP` environment variable.

## Q36: How do you create custom CLI commands in Flask?
**A:** `import click; @app.cli.command('create-user') @click.argument('username') def create_user(username): ...`. Run: `flask create-user admin`. Click decorators for arguments, options, and prompts. Commands can use `current_app` and database. Group commands with `@app.cli.group()`.

## Q37: How does Flask handle signals?
**A:** Flask signals (via Blinker) allow decoupled notification. Built-in signals: `request_started`, `request_finished`, `got_request_exception`, `template_rendered`. Subscribe: `from flask import request_finished; request_finished.connect(my_callback)`. Custom signals: `namespace = Namespace(); my_signal = namespace.signal('my-signal')`.

## Q38: What is the difference between signals and hooks?
**A:** Hooks (`before_request`, `after_request`) are synchronous, Flask-specific, and run in request order. Signals (Blinker) are decoupled, allow multiple subscribers, support async, and can be used outside Flask. Signals are more flexible; hooks are simpler for per-request logic.

## Q39: How do you handle caching in Flask?
**A:** Flask-Caching extension supports multiple backends: Redis, Memcached, filesystem, simple (in-memory). Cache view results: `@cache.cached(timeout=300)`. Cache function results: `@cache.memoize(timeout=300)`. Manual: `cache.set(key, value, timeout)`, `cache.get(key)`. Invalidate: `cache.delete(key)`.

## Q40: What is Flask-Caching?
**A:** Flask-Caching adds caching support. Backends: SimpleCache (in-memory), RedisCache, MemcachedCache, FileSystemCache, SASLMemcachedCache. Configuration: `app.config['CACHE_TYPE'] = 'RedisCache'`. Features: cached view decorator, memoization, cache key prefix, default timeout, cache headers.

## Q41: How does Flask handle email sending?
**A:** Flask-Mail extension. Configure SMTP server: `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USERNAME`, `MAIL_PASSWORD`. Send: `msg = Message('Subject', recipients=['to@example.com']); msg.body = 'Body'; mail.send(msg)`. Support for attachments, HTML emails, and bulk sending.

## Q42: What is Flask-Mail?
**A:** Flask-Mail provides SMTP email sending. Configure `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USE_TLS`, `MAIL_USE_SSL`, `MAIL_USERNAME`, `MAIL_PASSWORD`, `MAIL_DEFAULT_SENDER`. Message class: attachments (`msg.attach()`), HTML (`msg.html`), recipients (to, cc, bcc). Connection pooling for bulk emails.

## Q43: How does Flask handle RESTful APIs?
**A:** Flask can build REST APIs directly with `@app.route` and `jsonify`. Flask-RESTful extension provides `Resource` classes with method-based routing. Flask-RESTx adds Swagger documentation. For more features, consider FastAPI or Flask with Flask-RESTful for structured API development.

## Q44: What is Flask-RESTful?
**A:** Flask-RESTful provides `Resource` class for building REST APIs. `class UserAPI(Resource): def get(self, id): ... ; def post(self): ...`. Register: `api.add_resource(UserAPI, '/users/<int:id>')`. Built-in request parsing (`reqparse`), response marshalling (`marshal_with`), and error handling.

## Q45: What is `reqparse` in Flask-RESTful?
**A:** `reqparse` is a request parser (deprecated in newer versions, use `webargs` or marshmallow). Define expected arguments: `parser = reqparse.RequestParser(); parser.add_argument('name', type=str, required=True)`. Parse: `args = parser.parse_args()`. Validates types and provides default values.

## Q46: How does Flask handle WebSockets?
**A:** Flask natively doesn't support WebSockets. Flask-SocketIO integrates Socket.IO (WebSocket with fallbacks). Server: `socketio = SocketIO(app); @socketio.on('message') def handle_message(data): ...`. Run with `socketio.run(app)`. Supports rooms, events, and broadcasting.

## Q47: What is Flask-SocketIO?
**A:** Flask-SocketIO adds WebSocket support via Socket.IO protocol. Features: bidirectional event-based communication, rooms, broadcasting, fallback transports (long-polling), async modes (threading, gevent, eventlet). Client: Socket.IO JavaScript library. Events: `emit`, `on`, `send`. Authentication via events.

## Q48: How do you handle background tasks in Flask?
**A:** Options: thread-based (`threading.Thread`), Flask-Executor (thread pool), Celery (distributed task queue), Redis Queue (RQ). Simple: `@app.route('/start-task') def start(): thread = Thread(target=long_task); thread.start(); return 'Task started'`. For production: Celery or RQ with task status tracking.

## Q49: What is Celery and how is it used with Flask?
**A:** Celery is a distributed task queue. Create: `celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])`. Define tasks: `@celery.task def send_email(data): ...`. Call: `send_email.delay(data)`. Requires broker (Redis/RabbitMQ) and result backend. Monitor with Flower.

## Q50: How does Flask handle testing?
**A:** Flask provides test client: `app.test_client()`. Example: `with app.test_client() as client: resp = client.get('/'); assert resp.status_code == 200`. Use `pytest` with Flask's `app.test_request_context()` for request context without server. Flask testing docs recommend `pytest`.

## Q51: How do you test Flask applications with pytest?
**A:** Create conftest.py with fixtures: `@pytest.fixture def app(): app = create_app(); yield app`. Test: `def test_home(client): resp = client.get('/'); assert b'Hello' in resp.data`. Use `app.test_request_context()` for testing code needing request context.

## Q52: What is `app.test_request_context()`?
**A:** Pushes a request context without sending a real request: `with app.test_request_context('/?page=1'): current_app.name; request.args.get('page')`. Useful for testing code that depends on `request`, `session`, `g`, or `url_for`. Cleanup happens on exit.

## Q53: How does Flask handle application factories?
**A:** Application factory pattern: `def create_app(config_name): app = Flask(__name__); app.config.from_object(config); db.init_app(app); return app`. Benefits: multiple instances (testing, production), configurable, avoids circular imports. Extensions use `init_app()` instead of constructor.

## Q54: Why use an application factory in Flask?
**A:** Application factories provide: multiple app instances (testing config, production config), delayed extension creation (avoid circular imports), per-request configuration, easier testing (create app with test config), and better organization for larger projects. Standard pattern for Flask apps.

## Q55: How does Flask handle circular imports?
**A:** Common issue with models and app creation. Solutions: use application factory (extensions don't import app), lazy initialization (`db.init_app(app)`), import inside functions, separate models into their own module, use `current_app` instead of importing `app`.

## Q56: What is `current_app` proxy?
**A:** `from flask import current_app` provides access to the Flask application instance from anywhere within the application context. Avoids importing the app instance directly (prevents circular imports). `current_app.config['KEY']`, `current_app.logger`, etc. Only available during request processing.

## Q57: How does Flask handle logging?
**A:** `app.logger` is the default logger. Config: `app.logger.setLevel(logging.INFO); handler = logging.FileHandler('app.log'); app.logger.addHandler(handler)`. Usage: `app.logger.info('Request received')`, `app.logger.error('Error occurred')`. Can configure specific loggers with standard `logging` module.

## Q58: What is the Flask debug mode?
**A:** Enabled with `FLASK_ENV=development` or `app.run(debug=True)`. Provides: automatic reloader (restarts on code change), interactive debugger (Werkzeug debugger) on errors, helpful error pages. Never use in production (security risk - debugger allows code execution).

## Q59: What is the difference between `FLASK_ENV` and `FLASK_DEBUG`?
**A:** `FLASK_ENV=development` sets debug mode and enables reloader. `FLASK_DEBUG=1` separately controls debug mode. In Flask 2.3+, `--debug` flag replaces FLASK_ENV. Use `--debug` for development, `--no-debug` for production. Environment variables are deprecated for newer Flask versions.

## Q60: How does Flask handle JSON serialization?
**A:** `jsonify()` serializes dicts/lists to JSON response. Custom serializers: `app.json_encoder = CustomJSONEncoder` (deprecated in Flask 2.3+). Use `json` module or `app.json.dumps()`. Flask 2.3+ uses `orjson` if available for faster JSON serialization.

## Q61: What is `flask.json.provider`?
**A:** Flask 2.3+ uses `JSONProvider` abstraction. Replace with: `app.json = MyJSONProvider(app)`. Or set default provider: `app.json_provider_class = OrJSONProvider`. Customize serialization by subclassing `JSONProvider` and overriding `dumps()` and `loads()`.

## Q62: How do you implement pagination in Flask?
**A:** SQLAlchemy pagination: `Page = Model.query.paginate(page=page, per_page=10, error_out=False)`. Provides: `Page.items`, `Page.total`, `Page.pages`, `Page.has_prev`, `Page.has_next`, `Page.prev_num`, `Page.next_num`. Manual: calculate offset/limit from query params.

## Q63: How does Flask handle rate limiting?
**A:** Flask-Limiter extension. Usage: `@limiter.limit("5 per minute")`. Config: `RATELIMIT_ENABLED`, `RATELIMIT_STORAGE_URL` (Redis/memory). Key functions: `request.remote_addr`, custom callable. Exempt specific endpoints. Default rate limit for all routes. Storage options: memory, Redis, Memcached, MongoDB.

## Q64: What is Flask-Limiter?
**A:** Flask-Limiter adds rate limiting. Decorators: `@limiter.limit("100/day")`, `@limiter.exempt`. Key functions identify clients: IP, user ID header. Storage backends: in-memory (development), Redis (production). Limits defined per endpoint, per blueprint, or globally. Response headers: `X-RateLimit-*`.

## Q65: How does Flask handle file configuration?
**A:** `app.config.from_pyfile('config.cfg')` loads from Python file. `app.config.from_object('module.ConfigClass')` loads from class. `app.config.from_json('config.json')` loads from JSON. `app.config.from_mapping({'KEY': 'value'})` from dict. Environment vars: `app.config.from_prefixed_env('FLASK')`.

## Q66: What is Flask's `instance` folder?
**A:** The instance folder (`instance/`) stores config files that shouldn't be committed (secret keys, DB passwords). `app = Flask(__name__, instance_relative_config=True)`. Load with `app.config.from_pyfile('config.py')` from instance folder. Access via `app.instance_path`.

## Q67: How do you handle environment-specific configuration?
**A:** Class-based config: `class Config: SECRET_KEY = '...' ; class DevelopmentConfig(Config): DEBUG = True ; class ProductionConfig(Config): DEBUG = False`. Load: `app.config.from_object(DevelopmentConfig)`. Use env var: `app.config.from_object(os.environ.get('FLASK_CONFIG', 'config.DevelopmentConfig'))`.

## Q68: What is `SECRET_KEY` and why is it important?
**A:** `SECRET_KEY` is used for signing session cookies, CSRF tokens, and other security tokens. Must be a random, secret string (at least 32 bytes). Generate: `os.urandom(24)` or `secrets.token_hex(16)`. Store in environment variable or instance config. Rotate periodically.

## Q69: How does Flask handle multiple environments?
**A:** Development: debug mode, verbose logging, relaxed CORS. Testing: separate database, test client. Staging: production-like with test data. Production: optimized, error logging, caching enabled. Use environment variables (`FLASK_ENV`, `DATABASE_URL`) to select configuration class.

## Q70: How do you set up Flask with Docker?
**A:** Dockerfile: `FROM python:3.11; WORKDIR /app; COPY requirements.txt .; RUN pip install -r requirements.txt; COPY . .; EXPOSE 5000; CMD ["gunicorn", "-w", "4", "app:app"]`. Docker-compose for multi-service apps (Flask + Redis + DB). Use `.dockerignore` to exclude unnecessary files.

## Q71: How does Flask perform under production?
**A:** Flask's built-in server is single-threaded and unsuitable for production. Deploy with production WSGI servers: Gunicorn (`gunicorn -w 4 app:app`), uWSGI, mod_wsgi (Apache). Use reverse proxy (NGINX) for static files, load balancing, and SSL termination. Add caching, CDN, and connection pooling.

## Q72: What is `gunicorn` and how is it used with Flask?
**A:** Gunicorn is a production WSGI server: `gunicorn -w 4 -b 0.0.0.0:8000 app:app`. Options: `--workers` (process count, recommended 2-4 x CPU cores), `--worker-class` (sync, gevent, eventlet), `--timeout`, `--keep-alive`. Flask app object is passed as `module:app`. For async: use gevent workers.

## Q73: How does Flask handle context locals?
**A:** Flask uses `werkzeug.local.LocalProxy` and `werkzeug.local.LocalStack` for thread-local contexts. `request`, `session`, `g`, `current_app` are proxies accessing context-local stacks. This allows multiple requests in same process (threads) without data leakage. Contexts are pushed/pop per request.

## Q74: What is `LocalProxy` in Flask?
**A:** `LocalProxy` is a proxy that forwards operations to a context-local object. `from flask import request` is a `LocalProxy` that resolves to the actual request object from the current request context. Enables thread-safe access. Used for `request`, `session`, `g`, `current_app`.

## Q75: How does Flask handle thread safety?
**A:** Flask uses context locals (thread-local data). Each thread has its own request/application context. Extensions must be context-aware. For multi-threaded WSGI servers (Gunicorn with threaded workers), avoid shared mutable state without locks. Database sessions should be per-request.

## Q76: How do you implement health checks in Flask?
**A:** Simple: `@app.route('/health') def health(): return jsonify(status='healthy')`. Advanced: check DB connectivity, Redis ping, service dependencies. Use blueprints for `/health` and `/ready` endpoints. Return 200 for healthy, 503 for degraded. Separate readiness (dependencies ready) from liveness (process alive).

## Q77: What is Flask's `stream_template`?
**A:** `stream_template('large.html', **context)` renders a template incrementally, sending chunks as they're generated. Useful for large templates with iteration (generates output progressively). Reduces time to first byte. Client receives partial content. Standard `render_template` builds full output in memory.

## Q78: How does Flask handle streaming responses?
**A:** Use generator with `Response`: `def generate(): yield "chunk1"; yield "chunk2"; return Response(generate(), mimetype='text/plain')`. For large CSV: `def generate_csv(): yield "header\n"; for row in data: yield f"{row}\n"; return Response(generate_csv(), mimetype='text/csv')`.

## Q79: What is `Response` class in Flask?
**A:** Flask's `Response` (Werkzeug) encapsulates HTTP response. Constructor: `Response(response=None, status=None, headers=None, mimetype=None, content_type=None, direct_passthrough=False)`. Properties: `status_code`, `headers`, `data`, `set_cookie()`, `delete_cookie()`, `content_type`, `content_length`.

## Q80: How do you handle ETags in Flask?
**A:** Automatic in Flask: `response.add_etag()` or use `@app.after_request` to add ETag. Client sends `If-None-Match`. Flask returns `304 Not Modified` if ETag matches. Manual: `from flask import make_response; resp = make_response(data); resp.set_etag(hash); return resp`.

## Q81: What are Flask's URL processors?
**A:** `@app.url_value_preprocessor` runs before route matching (captures values). `@app.url_defaults` injects default values into `url_for()`. Example: inject `locale` variable into all URLs. `@app.url_defaults` modifies `url_for()` output by adding default parameters.

## Q82: How do you use `@app.before_first_request`?
**A:** `@app.before_first_request` runs once before the first request to this process. Used for: initializing caches, loading ML models, warming connections. Deprecated in Flask 2.3+ (use lazy initialization or application factory pattern). Not suitable for multi-process deployments.

## Q83: How does Flask handle request splitting?
**A:** Request splitting attacks exploit parsing differences between Flask/Werkzeug and reverse proxies. Mitigation: use consistent URL decoding, validate `Host` headers, restrict `Content-Type`, limit request size (`MAX_CONTENT_LENGTH`), enable proxy fix (`ProxyFix` middleware) for headers from trusted proxies.

## Q84: What is `ProxyFix` middleware?
**A:** `from werkzeug.middleware.proxy_fix import ProxyFix; app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)`. Adjusts `request.remote_addr`, `request.scheme`, `request.host` based on `X-Forwarded-*` headers. Required when behind reverse proxy (NGINX, ELB).

## Q85: How does Flask handle content negotiation?
**A:** `request.accept_mimetypes.best_match(['application/json', 'text/html'])` selects response format based on client's Accept header. Or use `request.is_json` to detect JSON requests. Flask-RESTful handles this automatically. Manual: check `Accept` header and render appropriate response format.

## Q86: What is `flask.views.MethodView`?
**A:** `MethodView` provides class-based views with methods per HTTP verb: `class UserAPI(MethodView): def get(self, id): ...; def post(self): ...`. Register: `app.add_url_rule('/users/<int:id>', view_func=UserAPI.as_view('user'))`. Organizes related route logic into classes.

## Q87: How do you implement method-based views in Flask?
**A:** `from flask.views import MethodView; class ItemView(MethodView): def get(self, item_id): ...; def post(self): ...; def put(self, item_id): ...; def delete(self, item_id): ...`. `app.add_url_rule('/items/<int:item_id>', view_func=ItemView.as_view('item'))`.

## Q88: What is `flask.views.View`?
**A:** Base class for class-based views. Subclass and implement `dispatch_request()`: `class MyView(View): def dispatch_request(self): return 'Hello'`. Register: `app.add_url_rule('/', view_func=MyView.as_view('myview'))`. Less common than MethodView. Useful for views with single HTTP method.

## Q89: How does Flask handle custom decorators?
**A:** `from functools import wraps; def login_required(f): @wraps(f) def decorated_function(*args, **kwargs): if not session.get('user_id'): return redirect(url_for('login')); return f(*args, **kwargs); return decorated_function`. Apply: `@app.route('/secret') @login_required def secret(): ...`.

## Q90: What is `safe_join` in Flask?
**A:** `from werkzeug.security import safe_join` safely joins path components, preventing directory traversal attacks. Example: `safe_join(app.root_path, user_input_path)`. Raises `NotFound` if resulting path is outside base directory. Essential when serving user-provided file paths.

## Q91: How does Flask handle XSS prevention?
**A:** Jinja2 auto-escapes HTML variables: `{{ user_input }}` escapes `<>&"'`. Use `|safe` filter only for trusted HTML. For JSON in HTML: `{{ data|tojson }}` produces safe JSON. Set `Content-Security-Policy` headers. Use Flask's `escape()` function for manual escaping.

## Q92: What is content security policy in Flask?
**A:** CSP prevents XSS and data injection. Set via response headers: `@app.after_request def add_csp(response): response.headers['Content-Security-Policy'] = "default-src 'self'"; return response`. Directives: `script-src`, `style-src`, `img-src`, `connect-src`, `frame-ancestors`. Use Flask-Talisman for CSP management.

## Q93: What is Flask-Talisman?
**A:** Flask-Talisman adds security headers: Content-Security-Policy, Strict-Transport-Security, X-Content-Type-Options, X-Frame-Options, X-XSS-Protection. Usage: `Talisman(app)` or `Talisman(app, content_security_policy=...)`. Force HTTPS, configure CSP, prevent clickjacking. Important for production deployments.

## Q94: How does Flask handle CORS?
**A:** Flask-CORS extension. `from flask_cors import CORS; CORS(app)` allows all origins. Specific: `CORS(app, origins=['https://example.com'])`. Per-route: `@cross_origin(origins='*')`. Proxies preflight (OPTIONS) requests. Configure `supports_credentials`, `allow_headers`, `expose_headers`.

## Q95: How do you create a REST API with Flask only (no extensions)?
**A:** `@app.route('/api/users', methods=['GET']) def get_users(): return jsonify(User.query.all())`. `@app.route('/api/users', methods=['POST']) def create_user(): data = request.get_json(); user = User(**data); db.session.add(user); db.session.commit(); return jsonify(user.to_dict()), 201`.

## Q96: How does Flask handle accept headers for content negotiation?
**A:** `request.accept_mimetypes` parses `Accept` header. `request.accept_mimetypes.best_match(['application/json', 'text/html'])` returns preferred format. `request.is_json` checks if request expects JSON. Use in view to return different formats based on client preference.

## Q97: What is the `stream_with_context` decorator?
**A:** `from flask import stream_with_context` preserves request context during streaming responses. Without it, context is lost after the view returns. Usage: `return Response(stream_with_context(generate()), mimetype='text/plain')`. Required when streaming code accesses `request`, `session`, `g`, or `current_app`.

## Q98: How does Flask handle template inheritance?
**A:** Base template `base.html`: `{% block content %}{% endblock %}`. Child: `{% extends "base.html" %}{% block content %}...{% endblock %}`. Multiple blocks: `title`, `head`, `scripts`. Super: `{{ super() }}` includes parent block content. Allows DRY template organization.

## Q99: What are Flask template filters?
**A:** Built-in filters: `{{ name|upper }}`, `{{ date|format_datetime }}`, `{{ text|truncate(100) }}`, `{{ list|join(', ') }}`, `{{ value|default('N/A') }}`, `{{ value|safe }}`. Custom: `@app.template_filter('reverse') def reverse_filter(s): return s[::-1]`. Filters can accept arguments.

## Q100: How do you handle database connection pooling in Flask?
**A:** Flask-SQLAlchemy handles connection pooling via SQLAlchemy's `pool_size` and `pool_recycle`. Config: `SQLALCHEMY_ENGINE_OPTIONS = {'pool_size': 10, 'pool_recycle': 3600, 'pool_pre_ping': True}`. For raw connections: use `connection_pool` from `sqlalchemy.pool`. `pool_pre_ping` tests connections before use.
