# Streamlit Interview Questions and Answers

## Q1: What is Streamlit?
**A:** Streamlit is an open-source Python library for building interactive web applications for data science, machine learning, and AI projects. It allows developers to create full-featured web apps using only Python (no HTML, CSS, or JavaScript required). Apps are built by writing Python scripts that are re-run when interactions occur.

## Q2: How does Streamlit differ from traditional web frameworks?
**A:** Streamlit uses a unique reactive model — the entire script re-runs from top to bottom on every user interaction. This simplifies development (no callback functions, no request/response handling) but means state is not preserved between runs. Traditional frameworks (Flask, Django) use explicit routing, request handling, and persistent server-side state.

## Q3: What are the core concepts of Streamlit?
**A:** Core concepts: 1) Script re-run — every interaction triggers a full re-run, 2) Widgets — interactive elements (buttons, sliders, text inputs), 3) Caching — @st.cache_data and @st.cache_resource prevent redundant computations, 4) Session state — st.session_state preserves data across re-runs, 5) Layout — columns, sidebar, expanders, containers organize the UI.

## Q4: How do you install and run a Streamlit app?
**A:** Install: pip install streamlit. Run: streamlit run app.py (opens in browser). Development options: streamlit run app.py --server.port 8501, --server.headless true (no auto-open). For production: deploy to Streamlit Community Cloud, Hugging Face Spaces, or custom server.

## Q5: What is the execution model of Streamlit?
**A:** The entire script executes from top to bottom on: 1) initial page load, 2) every widget interaction (slider change, button click), 3) programmatic rerun via st.experimental_rerun() (now st.rerun()). Widget values become the arguments — e.g., st.slider('x', 0, 10) returns the current value. This means no callbacks needed.

## Q6: How do you handle state persistence across re-runs?
**A:** Use st.session_state — a dictionary-like object that persists across re-runs. Initialize: if 'count' not in st.session_state: st.session_state.count = 0. Update: st.session_state.count += 1. Access anywhere in the script. Also used for: storing data, tracking widget values, sharing data between functions, and maintaining complex state.

## Q7: What is the difference between st.cache_data and st.cache_resource?
**A:** @st.cache_data caches data (DataFrames, arrays, strings) — hashed by value, thread-safe. @st.cache_resource caches resources (database connections, model objects, API clients) — returns the same object reference, not recreated. Use cache_data for expensive computations returning serializable data; use cache_resource for non-serializable resources.

## Q8: How does st.cache_data work?
**A:** @st.cache_data decorates a function. Streamlit hashes the function name + arguments. On subsequent calls with the same arguments, the cached result is returned instead of re-executing. Parameters: ttl (time-to-live), max_entries (cache size), persist="disk" (save to disk). The function must return a pickleable/serializable value.

## Q9: What is the purpose of st.rerun()?
**A:** st.rerun() (formerly st.experimental_rerun()) programmatically triggers a full script re-run. Useful after modifying st.session_state or when a background process completes. Use sparingly to avoid infinite loops. Typically called in combination with session state updates.

## Q10: What are widgets in Streamlit?
**A:** Widgets are interactive UI elements that return values. Common widgets: st.button (boolean), st.slider (numeric range), st.selectbox (dropdown), st.multiselect (multiple selection), st.text_input (text), st.number_input (numeric), st.checkbox (boolean), st.radio (single choice), st.date_input (date), st.file_uploader (file upload).

## Q11: How do you handle button clicks in Streamlit?
**A:** st.button('Click me') returns True only on the re-run where the button was clicked. Pattern: if st.button('Process'): run_process(). Each button press is one-shot — the next re-run returns False. For toggle behavior, use st.checkbox or session state.

## Q12: How do you create a form in Streamlit?
**A:** st.form('my_form') wraps widgets and a submit button — widgets inside a form don't trigger re-runs until the submit button is pressed. Must include st.form_submit_button() inside. Useful for multi-widget input without re-running on each change.

## Q13: What is the difference between st.form and regular widget placement?
**A:** Without form: every widget interaction triggers a re-run (good for immediate feedback, bad for many widgets). With form: widgets don't trigger re-runs until form_submit_button is pressed (batch input, fewer re-runs). Use forms when multiple related inputs are needed.

## Q14: How do you handle file uploads?
**A:** uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx']) returns an UploadedFile object (or None). Access: uploaded_file.read() (bytes), uploaded_file.name, uploaded_file.size. For CSV: pd.read_csv(uploaded_file). Multiple files via accept_multiple_files=True.

## Q15: How do you display DataFrames in Streamlit?
**A:** st.dataframe(df) — interactive, sortable, resizable columns. st.data_editor(df) — editable table (user can modify cells). st.table(df) — static table. st.write(df) — automatic display (recommended default).

## Q16: What is st.data_editor?
**A:** st.data_editor displays an editable DataFrame — users can modify cell values, add/delete rows, and edit column values. Returns the modified DataFrame. Parameters: num_rows="dynamic" (allow add/delete), disabled (columns to protect), column_config (customize display).

## Q17: How do you create charts in Streamlit?
**A:** Multiple charting options: st.line_chart(df) — simple line chart. st.area_chart(df), st.bar_chart(df), st.scatter_chart(df), st.map(df). For custom charts: import matplotlib.pyplot as plt; st.pyplot(fig). Also supports Altair, Plotly, Bokeh, and PyDeck.

## Q18: How do you use Plotly with Streamlit?
**A:** import plotly.express as px; fig = px.scatter(df, x='col1', y='col2'); st.plotly_chart(fig). Plotly charts are interactive (zoom, pan, hover). Pass use_container_width=True to fill column width. Also supports st.plotly_chart(fig, theme="streamlit") for consistent theming.

## Q19: How do you structure page layout in Streamlit?
**A:** st.set_page_config(layout="wide") — use full width. st.sidebar — place elements in sidebar. Columns: col1, col2 = st.columns(2). Containers: st.container(), st.expander("Expand"), st.tabs(["Tab 1", "Tab 2"]). Empty placeholder: st.empty(). st.columns with ratios: st.columns([2, 1]).

## Q20: What are tabs in Streamlit?
**A:** st.tabs(["Tab 1", "Tab 2"]) creates tabbed UI. Usage: tab1, tab2 = st.tabs(["Data", "Chart"]); with tab1: st.dataframe(df); with tab2: st.line_chart(df). Content inside each tab is lazy-loaded. Tabs organize complex dashboards into manageable sections.

## Q21: How do you create multi-page apps in Streamlit?
**A:** Create pages/ directory with page files (e.g., pages/02_Analysis.py). Pages are listed in the sidebar automatically. st.navigation (newer API) provides explicit control. Page config: st.set_page_config(page_title="Title", page_icon="icon"). Pages share session state across navigation.

## Q22: What is st.navigation and st.Page?
**A:** st.navigation and st.Page provide explicit multi-page control: home = st.Page("home.py", title="Home", icon=":house:"); analysis = st.Page("analysis.py", title="Analysis"); pg = st.navigation([home, analysis]); pg.run(). Gives more control than auto-discovery via pages/ directory.

## Q23: How do you add custom CSS to Streamlit?
**A:** st.markdown("""<style> .stButton > button { color: white; background-color: red; } </style>""", unsafe_allow_html=True). Or apply via st.html() (newer API). For global styling, create .streamlit/config.toml with [theme] section. Use CSS selectors to target Streamlit elements.

## Q24: How do you use st.markdown?
**A:** st.markdown("**bold** *italic* `code`") renders Markdown text. Supports: headers, lists, links, images, tables, code blocks, LaTeX ($x^2$), emoji (:rocket:). unsafe_allow_html=True enables raw HTML (use cautiously). Also: st.caption() for small text, st.header(), st.subheader(), st.title() for headings.

## Q25: What is st.write and why is it recommended?
**A:** st.write() is a Swiss-army-knife function that automatically determines how to display its arguments. It renders: strings (as markdown), DataFrames (as interactive table), charts, matplotlib figures, Plotly figures, and more. It's the recommended "try this first" display function as it adapts to the input type.

## Q26: How do you handle errors and exceptions in Streamlit?
**A:** st.error("Message") — red error box. st.warning("Warning") — yellow warning. st.info("Info") — blue info box. st.success("Success") — green success box. st.exception(e) — displays traceback. Use try/except to catch errors and display user-friendly messages instead of crashes.

## Q27: How do you show progress in Streamlit?
**A:** st.progress(progress_value) — progress bar (0.0 to 1.0). st.status("Processing...") — status container with spinner state. with st.spinner("Loading..."): — temporary spinner while executing. st.toast("Saved!") — ephemeral notification. st.snow() / st.balloons() — celebratory animations.

## Q28: What is st.status?
**A:** st.status("Running...") provides a status container with states: running (spinner), complete (checkmark), error. Usage: with st.status("Processing") as status: run(); status.update(label="Done!", state="complete"). Useful for showing multi-step progress with visual feedback.

## Q29: How do you use st.metric?
**A:** st.metric("Revenue", "$10K", delta="$2K") displays a metric with label, value, and optional delta (change indicator). Delta color: green for positive, red for negative. Can include help text. Useful for KPI dashboards. Combine with columns: col1.metric("Sales", 100, 10).

## Q30: How do you create dynamic UI elements?
**A:** Use conditionals: if st.checkbox("Show details"): st.write(details). Dynamic number of widgets via loops over st.session_state lists. st.popover() creates hover/toggle popups. st.container() groups elements. Empty placeholders: placeholder = st.empty(); placeholder.line_chart(data); placeholder.empty().

## Q31: What is the difference between st.empty and st.container?
**A:** st.empty() is a single-element placeholder that can be replaced (clear and rewrite). st.container() is a multi-element container that can hold multiple widgets. Both are mutable: .empty() clears content; you can write into both. Use empty for dynamic content that changes, container for grouped static content.

## Q32: How do you handle long-running computations?
**A:** Use @st.cache_data to cache results. For truly long computations (minutes): display progress with st.progress() inside the function, use st.status() for status updates, break computation into chunks. Consider offloading to background threads with st.rerun() when done. Avoid blocking the UI — use async patterns.

## Q33: What is the session state and how is it scoped?
**A:** st.session_state is a dictionary-like object scoped to a single browser session (tab). It persists across re-runs but not across different users/tabs. Keys are strings. Initialize: if 'key' not in st.session_state: st.session_state.key = value. Widgets with key parameter automatically bind to state. Clear with st.session_state.clear().

## Q34: How do you bind a widget to session state?
**A:** Widgets with a key parameter auto-sync to st.session_state: st.slider('x', 0, 10, key='slider') makes st.session_state.slider available. You can also set st.session_state.slider = 5 before the widget to set initial value. Widget state persists across re-runs.

## Q35: What is the callback parameter in widgets?
**A:** Widgets can have an on_change callback: st.selectbox('Options', ['a', 'b'], on_change=callback_fn, args=(arg,), kwargs={'kw': val}). The callback executes during the re-run triggered by the widget change. Useful for: updating other state, triggering side effects, or validation. Keep callbacks simple.

## Q36: How do you handle secrets in Streamlit?
**A:** Store secrets in .streamlit/secrets.toml (local) or configure in Cloud dashboard. Access: st.secrets["api_key"] or st.secrets["db"]["password"]. Secrets are loaded as environment variables in Cloud. Supported in Community Cloud, self-hosted, and Hugging Face Spaces.

## Q37: How do you deploy a Streamlit app?
**A:** Options: 1) Streamlit Community Cloud (free, connected to GitHub repo), 2) Hugging Face Spaces, 3) Streamlit for Teams, 4) Self-hosted with Docker, 5) AWS/GCP/Azure via custom containers. For Docker: FROM python:3.11; RUN pip install streamlit; COPY app.py; CMD streamlit run app.py --server.port=$PORT.

## Q38: How do you use environment variables in Streamlit?
**A:** Access via os.environ["MY_VAR"] (standard Python). Set locally: export MY_VAR=value. Set in Cloud: via Secrets/Env vars. st.secrets is an alias for environment variables in Cloud. For local dev: use .streamlit/secrets.toml or .env with python-dotenv.

## Q39: What are the theming options in Streamlit?
**A:** Configure in .streamlit/config.toml: [theme] primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font (sans serif/serif/monospace). Programmatic: st.set_page_config(page_title="Title"). No full custom theme switching at runtime (must be per-app config).

## Q40: How do you create a download button?
**A:** st.download_button("Download CSV", data=df.to_csv(), file_name="data.csv", mime="text/csv"). data can be: string, bytes, or file-like. For DataFrames: st.download_button("Download", df.to_csv(index=False), "data.csv"). For images/binary: open file in rb mode and pass bytes.

## Q41: How do you handle images in Streamlit?
**A:** st.image(image, caption="My Image", width=300) — display image from URL, file, numpy array, or PIL. st.image("https://image.png"), st.image(loaded_image). Multiple images: st.image([img1, img2], width=200). Use columns for side-by-side: col1.image(img1); col2.image(img2).

## Q42: How do you handle audio and video?
**A:** st.audio(audio_file, format="audio/wav") — play audio from bytes or file. st.video(video_file, format="video/mp4") — play video. Support: local files, URLs (YouTube), byte data, and file uploaders. Controls: autoplay, start_time, subtitles (for video).

## Q43: What is st.chat_input and st.chat_message?
**A:** st.chat_input("Type a message...") — chat input box, returns string (or None). st.chat_message("user"): — message container with avatar. Pattern: prompt = st.chat_input("Say something"); if prompt: st.chat_message("user").write(prompt); st.chat_message("assistant").write(response). Built-in for building chat UIs.

## Q44: How do you build a chatbot in Streamlit?
**A:** Pattern: 1) Initialize messages in session state: if "messages" not in st.session_state: st.session_state.messages = []. 2) Display existing messages: for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"]). 3) Handle input: if prompt := st.chat_input(): append, get response from LLM, append response, st.rerun().

## Q45: How do you use st.chat_input with LLMs?
**A:** Combine with OpenAI API: def get_response(prompt, history): response = client.chat.completions.create(model="gpt-4o", messages=history); return response.choices[0].message.content. Store full message history in session state. Display streaming responses with st.write_stream(response_generator).

## Q46: What is st.write_stream?
**A:** st.write_stream(generator) streams text token by token, updating the UI in real-time. Takes a generator yielding strings. Used with LLM streaming: def stream_response(): for chunk in client.chat.completions.create(..., stream=True): yield chunk.choices[0].delta.content or "". Displays incremental output without blocking.

## Q47: What are the performance best practices for Streamlit?
**A:** 1) Cache computations with @st.cache_data, 2) Use @st.cache_resource for DB connections and models, 3) Lazy-load expensive visualizations, 4) Avoid large data in session state, 5) Use st.empty() for dynamic content, 6) Use st.form for batch inputs, 7) Minimize imports at top level.

## Q48: How do you handle large datasets in Streamlit?
**A:** Use @st.cache_data to avoid re-reading. For display: st.dataframe handles large data with virtual scrolling. For large downloads: use st.download_button with streaming. For processing: use chunked reading (pd.read_csv(chunksize=10000)). Consider using st.data_editor with num_rows="fixed" for performance.

## Q49: How do you connect Streamlit to a database?
**A:** Use st.connection (Streamlit native): conn = st.connection("my_db", type="sql"). conn.query("SELECT * FROM table") returns DataFrame. Supports: PostgreSQL, MySQL, SQLite, Snowflake, BigQuery. For custom connections: create subclass of BaseConnection. Manages connection pooling and secrets automatically.

## Q50: What is st.connection?
**A:** st.connection is Streamlit's unified database connection API (since 1.28). Configured via secrets.toml: [connections.my_db] url="postgresql://...". Usage: conn = st.connection("my_db", type="sql"); df = conn.query("SELECT * FROM table", ttl=3600). Supports caching, pooling, and auto-configuration.

## Q51: How do you connect Streamlit to Snowflake/BigQuery?
**A:** Use st.connection with appropriate dialect: conn = st.connection("snowflake", type="sql"). Configure secrets. For BigQuery: use st.connection("bigquery", type="sql") with Google credentials in secrets. Streamlit manages the connection lifecycle and provides built-in caching.

## Q52: How do you use st.experimental_connection (legacy)?
**A:** st.experimental_connection("my_db", type="sql") is the precursor to st.connection. Same API but experimental. st.connection is now stable. For custom connections: class MyConn(st.experimental_connection): def _connect(self, **kwargs): return create_connection(); def query(self, sql): return self._instance.execute(sql).

## Q53: How do you test Streamlit apps?
**A:** Use streamlit.testing module (v1.36+): from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py"); at.run(); assert at.markdown[0].value == "Expected". Simulates interactions: at.button[0].click().at.run(). Check widget values and outputs. Headless testing without browser.

## Q54: How do you use Streamlit with Docker?
**A:** Dockerfile: FROM python:3.11-slim; WORKDIR /app; COPY requirements.txt .; RUN pip install -r requirements.txt; COPY . .; EXPOSE 8501; CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]. For Cloud Run: use --server.port=$PORT and --server.headless=true.

## Q55: How do you handle authentication in Streamlit?
**A:** Options: 1) st.secrets stored passwords (simple), 2) st.experimental_user (Streamlit Cloud auth), 3) OAuth via third-party (Auth0, Clerk, Firebase), 4) Custom login with st.text_input and session state. Streamlit Community Cloud has built-in auth via st.experimental_user (email-based).

## Q56: What is st.experimental_user?
**A:** st.experimental_user provides authentication info for Streamlit Community Cloud apps. st.experimental_user.email, st.experimental_user.logged_in. Requires enabling auth in app settings. Not available in local dev or other deployment platforms. Use st.secrets for local auth prototyping.

## Q57: How do you configure Streamlit server settings?
**A:** Via .streamlit/config.toml: [server] port=8501, headless=true, enableCORS=false, enableXsrfProtection=true, maxUploadSize=200, runOnSave=true. Or CLI args: --server.port 8501. Environment vars: STREAMLIT_SERVER_PORT=8501.

## Q58: How do you set the maximum upload size?
**A:** In .streamlit/config.toml: [server] maxUploadSize = 200 (in MB, default 200). Adjust for large file uploads. Also consider: client-side chunking for very large files, direct-to-cloud upload (presigned URLs), or file size validation before processing.

## Q59: How do you use caching with data that changes?
**A:** Use @st.cache_data(ttl=3600) for time-based expiration. Use @st.cache_data(max_entries=10) to limit cache size. Clear programmatically: st.cache_data.clear(). Use hash_funcs parameter for custom hashing of unhashable types: @st.cache_data(hash_funcs={pd.DataFrame: hash_dataframe}).

## Q60: What is the hash_funcs parameter in caching?
**A:** hash_funcs provides custom hash functions for unhashable types in cached function arguments. Example: @st.cache_data(hash_funcs={CustomObject: lambda obj: obj.id}). Required when arguments include types Streamlit can't hash (custom objects, database connections). Otherwise, caching fails.

## Q61: How do you debug a Streamlit app?
**A:** 1) st.write() to inspect variables, 2) st.json() for structured data, 3) st.stop() to halt execution at a point, 4) Python logging to terminal (streamlit run outputs logs), 5) st.exception() to show tracebacks, 6) st.help() for object documentation, 7) st.html(debug_info) for custom debugging.

## Q62: What is st.stop?
**A:** st.stop() halts the current script execution without raising an error. Useful for early returns in conditional logic, preventing execution of code below a certain point. Example: if not st.session_state.logged_in: st.warning("Please log in"); st.stop(); # rest of app.

## Q63: How do you format numbers and dates in Streamlit?
**A:** Use column_config in data_editor and dataframe: st.data_editor(df, column_config={"price": st.column_config.NumberColumn(format="$%.2f"), "date": st.column_config.DateColumn(format="DD/MM/YYYY")}). Creates formatted display without modifying underlying data. Also: st.column_config.TextColumn, SelectboxColumn, BarChartColumn, ProgressColumn.

## Q64: What is column_config in Streamlit?
**A:** column_config customizes column display in st.dataframe and st.data_editor. Options: label (header), help (tooltip), width, disabled, required. Type-specific: NumberColumn (format, min, max), TextColumn (max_chars, validate), LinkColumn, ImageColumn, ProgressColumn, ListColumn.

## Q65: How do you create a column with progress bars in a DataFrame?
**A:** st.data_editor(df, column_config={"completion": st.column_config.ProgressColumn("Progress", format="%d%%", min_value=0, max_value=100)}). Displays progress bars inline in the table cell. Works with data_editor and dataframe. Values mapped to bar width based on min/max.

## Q66: How do you use st.fragment?
**A:** @st.fragment decorator creates a lazy-loaded section of the app. The fragment runs independently of the main script and can update itself without re-running the entire app. Useful for: polling data, background updates, periodic refreshes. Parameters: run_every=N seconds for auto-refresh.

## Q67: What is st.query_params?
**A:** st.query_params provides access to URL query parameters: st.query_params["key"] reads, st.query_params["key"] = "value" sets. Enables: deep linking, sharing app state via URL, bookmarkable views. Changes update the URL without full page reload. st.query_params.clear() to reset.

## Q68: How do you handle WebSocket connections in Streamlit?
**A:** Streamlit uses WebSockets internally for server-client communication. For custom WebSocket handling: use st.websocket (experimental) or manage WebSocket connections outside Streamlit (asyncio) and update session state. For real-time data: poll with @st.fragment(run_every=1) or connect via st_websocket_library.

## Q69: How do you use Streamlit with async code?
**A:** Streamlit runs synchronously by default. For async: use asyncio.run() within cached functions, or use st.experimental_fragment with async. For API calls: use synchronous versions (requests) rather than async (httpx) to avoid compatibility issues. Newer versions improve async support.

## Q70: What are common Streamlit anti-patterns?
**A:** 1) Modifying session state inside cached functions, 2) Large data in session state (should use cache), 3) Expensive computations without caching, 4) Widget callbacks that modify the same widget's value (infinite loop), 5) Using st.stop() excessively, 6) Not using st.form for multi-widget input.

## Q71: How do you handle multiple users and concurrency?
**A:** Each user gets their own session with isolated session state. Streamlit server handles concurrency via thread-per-session. For shared state across users: use external storage (database, Redis). For rate limiting: implement at the application or infrastructure level. For computation: use background workers.

## Q72: What is the Streamlit config system?
**A:** Streamlit uses a layered config system (highest to lowest priority): 1) CLI flags, 2) Environment variables, 3) config.toml file, 4) Default values. Config file path: .streamlit/config.toml (project-level) or ~/.streamlit/config.toml (global). Covers server, theme, browser, runner, and logger settings.

## Q73: How do you enable CORS in Streamlit?
**A:** Streamlit doesn't typically need CORS as apps are opened directly. For embedding in iframes: --server.enableCORS=true. For custom domains: configure --server.enableXsrfProtection=false (if needed). For production: use a reverse proxy (nginx, Caddy) to handle CORS.

## Q74: How do you embed Streamlit in iframes?
**A:** Set --server.enableCORS=false and --server.enableXsrfProtection=false. Use iframe: <iframe src="https://yourapp.streamlit.app?embed=true" width="800" height="600"></iframe>. The ?embed=true removes some UI chrome. For Streamlit Cloud, embedding must be enabled in app settings.

## Q75: What is the difference between Streamlit and Dash?
**A:** Streamlit: simpler, Python-only, script re-run model, faster prototyping, less customizable. Dash: callback-based, React components, more customizable, steeper learning curve, enterprise features (authentication, URL routing). Streamlit is better for data scientists; Dash for production dashboards with complex interactions.

## Q76: How do you use Streamlit with machine learning models?
**A:** 1) Load model with @st.cache_resource (runs once), 2) Get user input via widgets, 3) Preprocess input, 4) Run model.predict(), 5) Display results. Example: model = st.cache_resource(load_model)(); input_data = st.text_input("Enter features"); if input_data: result = model.predict([parse(input_data)]); st.write(result).

## Q77: How do you use Streamlit with LangChain?
**A:** Build chat UI: st.chat_message for history, st.chat_input for input, st.write_stream for streaming responses. Use session state for message history. Cache LangChain chain: @st.cache_resource def load_chain(): return create_rag_chain(retriever, model). Chain.invoke(input, config=...) with streaming callbacks.

## Q78: How do you create a PDF viewer or report in Streamlit?
**A:** Display PDF: st.write with iframe: st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True). For generated PDFs: use st.download_button with reportlab/weasyprint. For PDF parsing: PyPDF2, pdfplumber. For slides: st.slides (Streamlit Labs).

## Q79: How do you use Streamlit with Plotly Dashboards?
**A:** Combine Plotly with Streamlit: import plotly.express as px; fig = px.scatter(df, x='x', y='y', color='category'); st.plotly_chart(fig, use_container_width=True). Use st.selectbox to change chart parameters, st.slider for date ranges. Plotly charts are interactive with hover, zoom, and selection.

## Q80: How do you handle real-time data updates?
**A:** Options: 1) @st.fragment(run_every=5) — auto-refresh every 5 seconds, 2) st.rerun() triggered by external events, 3) WebSocket connection via custom component, 4) Polling with time.sleep() in a loop (not recommended — blocks UI). For true real-time: use custom component with WebSocket.

## Q81: How do you use st.popover?
**A:** st.popover("Settings") creates a toggleable popup container. Usage: with st.popover("Filters"): option = st.selectbox("Category", options); value = st.slider("Range"). The popover shows/hides on click. Useful for: filters, settings, and secondary controls without cluttering the main UI.

## Q82: What are Streamlit's accessibility features?
**A:** Streamlit supports: semantic HTML, ARIA labels via help parameter on widgets (help="Description for screen readers"), keyboard navigation, focus management, high contrast themes, and configurable fonts. st.set_page_config provides page title and icon. Custom CSS can improve accessibility further.

## Q83: How do you create custom Streamlit components?
**A:** Custom components use HTML/JS/TS to add new UI elements. Use streamlit-component-template. Steps: 1) Create Python API, 2) Build frontend with any framework (React, Vue, Svelte), 3) Use Streamlit's component API to send/receive data. Publish via PyPI. Example components: st_aggrid, streamlit-plotly-events.

## Q84: What is the Streamlit Component API?
**A:** The component API allows bidirectional communication between Python and frontend. Python side: component = declare_component("my_component", url="http://localhost:3001"); value = component(arg="data"). Frontend: StreamlitComponent class from streamlit-component-lib handles callbacks and data serialization.

## Q85: How do you use Streamlit's session state across pages?
**A:** st.session_state is shared across all pages in a multi-page app. A value set on page 1 is accessible on page 2. Use for: user authentication, shared data, app-wide settings, navigation state. Clear on logout: for key in list(st.session_state.keys()): del st.session_state[key].

## Q86: How do you use Streamlit with Google Analytics?
**A:** Inject GA script via st.markdown with unsafe_allow_html: st.markdown('<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXX"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag("js", new Date()); gtag("config", "G-XXXXX");</script>', unsafe_allow_html=True). Track custom events via st.markdown with JS.

## Q87: How do you use Streamlit with Snowflake?
**A:** conn = st.connection("snowflake", type="sql") configured via secrets.toml with account, user, password, warehouse, database, schema. Or use Snowpark: from snowflake.snowpark import Session; session = Session.builder.configs(st.secrets["snowflake"]).create(). Streamlit in Snowflake (SiS) provides native integration.

## Q88: What is Streamlit in Snowflake (SiS)?
**A:** SiS allows running Streamlit apps directly inside Snowflake, with native SQL/Snowpark access. Apps are stored as stages in Snowflake. Benefits: no data movement (compute near data), built-in authentication, automatic scaling. Limitations: limited Python packages, no custom components.

## Q89: How do you use Streamlit with Hugging Face Spaces?
**A:** Create a Space on HF, set SDK to Streamlit, push code via Git. requirements.txt for dependencies, packages.txt for system deps. Streamlit apps on Spaces benefit from: free GPU (if configured), community features, easy sharing. Access hardware: se选题 GPU upgrade in Space settings.

## Q90: How do you build a Streamlit app for a hackathon?
**A:** Quick start: 1) pip install streamlit, 2) Create app.py with title and layout, 3) Use st.cache_data for heavy ops, 4) Deploy to Streamlit Cloud (connect GitHub repo, free tier), 5) Polish with st.columns, st.tabs, st.metrics. Focus on working demo over perfect code.

## Q91: How do you use Streamlit with API backends?
**A:** Call REST APIs via requests library: response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {st.secrets['api_key']}"}); data = response.json(). Cache API results with @st.cache_data(ttl=300) to avoid rate limits. Use st.status for API call progress.

## Q92: How do you implement search in Streamlit?
**A:** st.search = st.text_input("Search", placeholder="Type to search..."); filtered_df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]. For better performance: use st.dataframe with built-in column search, or use df.query() for structured search. For full-text: consider Elasticsearch integration.

## Q93: How do you use pagination in Streamlit?
**A:** Implement manual pagination: page_size = 10; total_pages = len(df) // page_size + 1; page = st.selectbox("Page", range(total_pages)); start = page * page_size; st.dataframe(df.iloc[start:start+page_size]). Or use st.dataframe with built-in virtual scrolling (handles large data without explicit pagination).

## Q94: How do you handle user sessions with login?
**A:** Basic approach: st.text_input for username/password, check against st.secrets, set st.session_state.authenticated = True. For OAuth: use Auth0 or Clerk integration. For Streamlit Cloud: use st.experimental_user for email-based auth. Redirect: check auth at app start, st.stop() if not authenticated.

## Q95: How do you use Streamlit with FastAPI?
**A:** Run Streamlit and FastAPI separately. Streamlit handles UI, FastAPI handles API. Communication: Streamlit calls FastAPI via requests (localhost or deployed URL). For auth: share tokens via session state. For deployment: use docker-compose with both services or deploy separately.

## Q96: What is the Streamlit roadmap and future?
**A:** Key focus areas: improved performance (faster re-runs), better multi-page apps, enhanced data editor, native state management, improved theming, better async support, AI/ML integrations, lower latency streaming, and expanded component ecosystem. Streamlit is actively developed by Snowflake.

## Q97: How do you migrate from Streamlit 1.x to 2.x?
**A:** Key changes: st.experimental_* methods promoted to stable (st.connection, st.rerun, st.fragment), deprecated methods removed (st. BetaColumns), improved caching API, new session state semantics. Check deprecation warnings. Main changes: replace st.experimental_rerun with st.rerun, st.cache with @st.cache_data.

## Q98: What are the limitations of Streamlit?
**A:** Limitations: 1) No native multi-user auth (use external), 2) Server-rendered (not SPA), 3) Limited customization (no direct HTML/CSS control), 4) Stateless model (full re-run per interaction), 5) Not ideal for SEO, 6) Limited to Python, 7) Performance with 100+ concurrent users needs scaling, 8) No mobile-first design.

## Q99: How do you scale Streamlit apps?
**A:** Options: 1) Streamlit Cloud (auto-scaling), 2) Manual scaling with Kubernetes, 3) Load balancer + multiple instances (stateless), 4) Separate computation to background workers, 5) Use external databases instead of in-memory, 6) Cache aggressively, 7) Use CDN for static assets, 8) Session affinity for stateful deployments.

## Q100: What are the best Streamlit resources and communities?
**A:** Official: docs.streamlit.io, gallery.streamlit.app (app examples), discuss.streamlit.io (forum), GitHub (source). Community: Awesome Streamlit (curated resources), Streamlit on Reddit, Streamlit Discord, Streamlit Blog, YouTube tutorials, and Streamlit events/conferences.
