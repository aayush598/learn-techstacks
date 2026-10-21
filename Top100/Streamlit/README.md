# Streamlit Interview Questions and Answers

## Q1: What is Streamlit?
**A:** Streamlit is an open-source Python library for building interactive web applications for data science, machine learning, and AI projects. It allows developers to create full-featured web apps using only Python (no HTML, CSS, or JavaScript required). Apps are built by writing Python scripts that are re-run when interactions occur.

**Code:**
```python
import streamlit as st

st.title("My first Streamlit app")
st.write("Hello from a data app built in pure Python!")
```

## Q2: How does Streamlit differ from traditional web frameworks?
**A:** Streamlit uses a unique reactive model — the entire script re-runs from top to bottom on every user interaction. This simplifies development (no callback functions, no request/response handling) but means state is not preserved between runs. Traditional frameworks (Flask, Django) use explicit routing, request handling, and persistent server-side state.

**Code:**
```python
import streamlit as st

x = st.slider("Pick a value", 0, 100)
st.write(f"The whole script re-runs with x = {x}")
```

## Q3: What are the core concepts of Streamlit?
**A:** Core concepts: 1) Script re-run — every interaction triggers a full re-run, 2) Widgets — interactive elements (buttons, sliders, text inputs), 3) Caching — @st.cache_data and @st.cache_resource prevent redundant computations, 4) Session state — st.session_state preserves data across re-runs, 5) Layout — columns, sidebar, expanders, containers organize the UI.

**Code:**
```python
import streamlit as st

count = st.session_state.get("count", 0)
if st.button("Increment"):
    count += 1
    st.session_state.count = count
st.write(f"Script re-run, widget-driven, cached, session value: {count}")
```

## Q4: How do you install and run a Streamlit app?
**A:** Install: pip install streamlit. Run: streamlit run app.py (opens in browser). Development options: streamlit run app.py --server.port 8501, --server.headless true (no auto-open). For production: deploy to Streamlit Community Cloud, Hugging Face Spaces, or custom server.

**Code:**
```python
# Terminal commands
#   pip install streamlit
#   streamlit run app.py
#   streamlit run app.py --server.port 8501 --server.headless true

import streamlit as st

st.write("The app that streamlit run launches")
```

## Q5: What is the execution model of Streamlit?
**A:** The entire script executes from top to bottom on: 1) initial page load, 2) every widget interaction (slider change, button click), 3) programmatic rerun via st.experimental_rerun() (now st.rerun()). Widget values become the arguments — e.g., st.slider('x', 0, 10) returns the current value. This means no callbacks needed.

**Code:**
```python
import streamlit as st

st.session_state.runs = st.session_state.get("runs", 0) + 1
st.write(f"This script has executed {st.session_state.runs} time(s)")

if st.button("Force another re-run"):
    st.rerun()
```

## Q6: How do you handle state persistence across re-runs?
**A:** Use st.session_state — a dictionary-like object that persists across re-runs. Initialize: if 'count' not in st.session_state: st.session_state.count = 0. Update: st.session_state.count += 1. Access anywhere in the script. Also used for: storing data, tracking widget values, sharing data between functions, and maintaining complex state.

**Code:**
```python
import streamlit as st

if "count" not in st.session_state:
    st.session_state.count = 0

if st.button("Click me"):
    st.session_state.count += 1

st.write("Count:", st.session_state.count)
```

## Q7: What is the difference between st.cache_data and st.cache_resource?
**A:** @st.cache_data caches data (DataFrames, arrays, strings) — hashed by value, thread-safe. @st.cache_resource caches resources (database connections, model objects, API clients) — returns the same object reference, not recreated. Use cache_data for expensive computations returning serializable data; use cache_resource for non-serializable resources.

**Code:**
```python
import streamlit as st

@st.cache_data
def compute_data(n):
    return list(range(n))  # serializable: cached by value

@st.cache_resource
def get_connection():
    return {"client": "shared", "conn": "reused"}  # same object returned

st.write(compute_data(5))
st.write(get_connection())
```

## Q8: How does st.cache_data work?
**A:** @st.cache_data decorates a function. Streamlit hashes the function name + arguments. On subsequent calls with the same arguments, the cached result is returned instead of re-executing. Parameters: ttl (time-to-live), max_entries (cache size), persist="disk" (save to disk). The function must return a pickleable/serializable value.

**Code:**
```python
import time
import streamlit as st

@st.cache_data(ttl=60, max_entries=5)
def expensive(n):
    time.sleep(1)  # would make every call slow without caching
    return [i ** 2 for i in range(n)]

st.write(expensive(100))  # runs the first time, cached afterwards
```

## Q9: What is the purpose of st.rerun()?
**A:** st.rerun() (formerly st.experimental_rerun()) programmatically triggers a full script re-run. Useful after modifying st.session_state or when a background process completes. Use sparingly to avoid infinite loops. Typically called in combination with session state updates.

**Code:**
```python
import streamlit as st

if "n" not in st.session_state:
    st.session_state.n = 0

if st.button("Increment and rerun"):
    st.session_state.n += 1
    st.rerun()

st.write("n =", st.session_state.n)
```

## Q10: What are widgets in Streamlit?
**A:** Widgets are interactive UI elements that return values. Common widgets: st.button (boolean), st.slider (numeric range), st.selectbox (dropdown), st.multiselect (multiple selection), st.text_input (text), st.number_input (numeric), st.checkbox (boolean), st.radio (single choice), st.date_input (date), st.file_uploader (file upload).

**Code:**
```python
import streamlit as st

st.button("Button")
st.slider("Slider", 0, 100)
st.selectbox("Selectbox", ["A", "B", "C"])
st.multiselect("Multiselect", ["x", "y", "z"])
st.text_input("Text input")
st.number_input("Number input")
st.checkbox("Checkbox")
st.radio("Radio", ["Yes", "No"])
st.date_input("Date input")
st.file_uploader("File uploader")
```

## Q11: How do you handle button clicks in Streamlit?
**A:** st.button('Click me') returns True only on the re-run where the button was clicked. Pattern: if st.button('Process'): run_process(). Each button press is one-shot — the next re-run returns False. For toggle behavior, use st.checkbox or session state.

**Code:**
```python
import streamlit as st

if st.button("Process data"):
    result = [i * 2 for i in range(5)]
    st.write("Processed:", result)

st.write("Button is one-shot; it returns True only on the click run.")
```

## Q12: How do you create a form in Streamlit?
**A:** st.form('my_form') wraps widgets and a submit button — widgets inside a form don't trigger re-runs until the submit button is pressed. Must include st.form_submit_button() inside. Useful for multi-widget input without re-running on each change.

**Code:**
```python
import streamlit as st

with st.form("my_form"):
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    submitted = st.form_submit_button("Submit")

if submitted:
    st.write(f"{name}, age {age}")
```

## Q13: What is the difference between st.form and regular widget placement?
**A:** Without form: every widget interaction triggers a re-run (good for immediate feedback, bad for many widgets). With form: widgets don't trigger re-runs until form_submit_button is pressed (batch input, fewer re-runs). Use forms when multiple related inputs are needed.

**Code:**
```python
import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.subheader("Without form")
    st.text_input("A", key="noform_a")   # each keystroke re-runs
    st.slider("B", 0, 10, key="noform_b")

with col2:
    st.subheader("With form")
    with st.form("batch"):
        st.text_input("A")
        st.slider("B", 0, 10)
        st.form_submit_button("Submit once")
```

## Q14: How do you handle file uploads?
**A:** uploaded_file = st.file_uploader("Choose a file", type=['csv', 'xlsx']) returns an UploadedFile object (or None). Access: uploaded_file.read() (bytes), uploaded_file.name, uploaded_file.size. For CSV: pd.read_csv(uploaded_file). Multiple files via accept_multiple_files=True.

**Code:**
```python
import pandas as pd
import streamlit as st

uploaded = st.file_uploader("Choose a CSV", type=["csv"])
if uploaded is not None:
    st.write(uploaded.name, uploaded.size, "bytes")
    df = pd.read_csv(uploaded)
    st.dataframe(df)
```

## Q15: How do you display DataFrames in Streamlit?
**A:** st.dataframe(df) — interactive, sortable, resizable columns. st.data_editor(df) — editable table (user can modify cells). st.table(df) — static table. st.write(df) — automatic display (recommended default).

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

st.dataframe(df)    # interactive / sortable
st.data_editor(df)  # editable
st.table(df)        # static
st.write(df)        # auto-recommended default
```

## Q16: What is st.data_editor?
**A:** st.data_editor displays an editable DataFrame — users can modify cell values, add/delete rows, and edit column values. Returns the modified DataFrame. Parameters: num_rows="dynamic" (allow add/delete), disabled (columns to protect), column_config (customize display).

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"name": ["alice", "bob"], "score": [90, 85]})
edited = st.data_editor(df, num_rows="dynamic")
st.write("Your edits:", edited)
```

## Q17: How do you create charts in Streamlit?
**A:** Multiple charting options: st.line_chart(df) — simple line chart. st.area_chart(df), st.bar_chart(df), st.scatter_chart(df), st.map(df). For custom charts: import matplotlib.pyplot as plt; st.pyplot(fig). Also supports Altair, Plotly, Bokeh, and PyDeck.

**Code:**
```python
import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": range(10), "y": [i ** 2 for i in range(10)]})

st.line_chart(df)  # built-in

fig, ax = plt.subplots()          # custom matplotlib
ax.plot(df["x"], df["y"])
st.pyplot(fig)
```

## Q18: How do you use Plotly with Streamlit?
**A:** import plotly.express as px; fig = px.scatter(df, x='col1', y='col2'); st.plotly_chart(fig). Plotly charts are interactive (zoom, pan, hover). Pass use_container_width=True to fill column width. Also supports st.plotly_chart(fig, theme="streamlit") for consistent theming.

**Code:**
```python
import plotly.express as px
import streamlit as st

df = px.data.iris()
fig = px.scatter(df, x="sepal_length", y="sepal_width", color="species")
st.plotly_chart(fig, use_container_width=True, theme="streamlit")
```

## Q19: How do you structure page layout in Streamlit?
**A:** st.set_page_config(layout="wide") — use full width. st.sidebar — place elements in sidebar. Columns: col1, col2 = st.columns(2). Containers: st.container(), st.expander("Expand"), st.tabs(["Tab 1", "Tab 2"]). Empty placeholder: st.empty(). st.columns with ratios: st.columns([2, 1]).

**Code:**
```python
import streamlit as st

st.set_page_config(layout="wide")
st.sidebar.title("Sidebar")

col1, col2 = st.columns([2, 1])
with col1:
    st.write("Wider column")
with col2:
    st.write("Narrower column")

with st.expander("Expand for more"):
    st.write("Hidden content")
```

## Q20: What are tabs in Streamlit?
**A:** st.tabs(["Tab 1", "Tab 2"]) creates tabbed UI. Usage: tab1, tab2 = st.tabs(["Data", "Chart"]); with tab1: st.dataframe(df); with tab2: st.line_chart(df). Content inside each tab is lazy-loaded. Tabs organize complex dashboards into manageable sections.

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": range(5), "y": [i * 2 for i in range(5)]})

tab1, tab2 = st.tabs(["Data", "Chart"])
with tab1:
    st.dataframe(df)
with tab2:
    st.line_chart(df)
```

## Q21: How do you create multi-page apps in Streamlit?
**A:** Create pages/ directory with page files (e.g., pages/02_Analysis.py). Pages are listed in the sidebar automatically. st.navigation (newer API) provides explicit control. Page config: st.set_page_config(page_title="Title", page_icon="icon"). Pages share session state across navigation.

**Code:**
```python
# app.py (main entry point)
import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")
st.title("Home")

# Create pages/01_Analysis.py next to this file and it
# automatically appears in the sidebar under pages/.
```

## Q22: What is st.navigation and st.Page?
**A:** st.navigation and st.Page provide explicit multi-page control: home = st.Page("home.py", title="Home", icon=":house:"); analysis = st.Page("analysis.py", title="Analysis"); pg = st.navigation([home, analysis]); pg.run(). Gives more control than auto-discovery via pages/ directory.

**Code:**
```python
import streamlit as st

def home():
    st.write("Home content")

def analysis():
    st.write("Analysis content")

pg = st.navigation(
    [st.Page(home, title="Home", icon=":house:"),
     st.Page(analysis, title="Analysis")]
)
pg.run()
```

## Q23: How do you add custom CSS to Streamlit?
**A:** st.markdown("""<style> .stButton > button { color: white; background-color: red; } </style>""", unsafe_allow_html=True). Or apply via st.html() (newer API). For global styling, create .streamlit/config.toml with [theme] section. Use CSS selectors to target Streamlit elements.

**Code:**
```python
import streamlit as st

st.markdown(
    "<style>.stButton > button { color: white; background-color: red; }</style>",
    unsafe_allow_html=True,
)
st.button("I am a red button")
```

## Q24: How do you use st.markdown?
**A:** st.markdown("**bold** *italic* `code`") renders Markdown text. Supports: headers, lists, links, images, tables, code blocks, LaTeX ($x^2$), emoji (:rocket:). unsafe_allow_html=True enables raw HTML (use cautiously). Also: st.caption() for small text, st.header(), st.subheader(), st.title() for headings.

**Code:**
```python
import streamlit as st

st.markdown("# Heading")
st.markdown("**bold** *italic* `code`")
st.markdown("LaTeX: $x^2 + y^2 = 1$")
st.markdown("Emoji: :rocket:")
st.caption("A small caption")
```

## Q25: What is st.write and why is it recommended?
**A:** st.write() is a Swiss-army-knife function that automatically determines how to display its arguments. It renders: strings (as markdown), DataFrames (as interactive table), charts, matplotlib figures, Plotly figures, and more. It's the recommended "try this first" display function as it adapts to the input type.

**Code:**
```python
import pandas as pd
import streamlit as st

st.write("A string renders as markdown")                     # markdown
st.write(pd.DataFrame({"a": [1, 2], "b": [3, 4]}))          # dataframe
st.write([1, 2, 3])                                          # python list
```
## Q26: How do you handle errors and exceptions in Streamlit?
**A:** st.error("Message") — red error box. st.warning("Warning") — yellow warning. st.info("Info") — blue info box. st.success("Success") — green success box. st.exception(e) — displays traceback. Use try/except to catch errors and display user-friendly messages instead of crashes.

**Code:**
```python
import streamlit as st

try:
    result = 1 / 0
except ZeroDivisionError as e:
    st.error("Cannot divide by zero")
    st.warning("Check your inputs")
    st.exception(e)  # shows the full traceback in the app
```

## Q27: How do you show progress in Streamlit?
**A:** st.progress(progress_value) — progress bar (0.0 to 1.0). st.status("Processing...") — status container with spinner state. with st.spinner("Loading..."): — temporary spinner while executing. st.toast("Saved!") — ephemeral notification. st.snow() / st.balloons() — celebratory animations.

**Code:**
```python
import time
import streamlit as st

with st.spinner("Loading..."):
    time.sleep(1)

bar = st.progress(0.0)
for i in range(10):
    time.sleep(0.05)
    bar.progress((i + 1) / 10)

st.toast("Done!")
```

## Q28: What is st.status?
**A:** st.status("Running...") provides a status container with states: running (spinner), complete (checkmark), error. Usage: with st.status("Processing") as status: run(); status.update(label="Done!", state="complete"). Useful for showing multi-step progress with visual feedback.

**Code:**
```python
import time
import streamlit as st

with st.status("Processing data...") as status:
    time.sleep(1)
    status.update(label="Step 1 complete")
    time.sleep(1)
    status.update(label="Step 2 complete")
    time.sleep(1)
    status.update(label="Done!", state="complete")
```

## Q29: How do you use st.metric?
**A:** st.metric("Revenue", "$10K", delta="$2K") displays a metric with label, value, and optional delta (change indicator). Delta color: green for positive, red for negative. Can include help text. Useful for KPI dashboards. Combine with columns: col1.metric("Sales", 100, 10).

**Code:**
```python
import streamlit as st

col1, col2 = st.columns(2)
col1.metric("Revenue", "$10K", delta="$2K")
col2.metric("Churn", "4%", delta="-1%")
```

## Q30: How do you create dynamic UI elements?
**A:** Use conditionals: if st.checkbox("Show details"): st.write(details). Dynamic number of widgets via loops over st.session_state lists. st.popover() creates hover/toggle popups. st.container() groups elements. Empty placeholders: placeholder = st.empty(); placeholder.line_chart(data); placeholder.empty().

**Code:**
```python
import streamlit as st

placeholder = st.empty()
placeholder.write("Static first render")

if st.button("Swap content"):
    placeholder.info("Dynamically replaced without a full element rebuild")

if st.checkbox("Show details"):
    st.write("Extra details revealed dynamically")
```

## Q31: What is the difference between st.empty and st.container?
**A:** st.empty() is a single-element placeholder that can be replaced (clear and rewrite). st.container() is a multi-element container that can hold multiple widgets. Both are mutable: .empty() clears content; you can write into both. Use empty for dynamic content that changes, container for grouped static content.

**Code:**
```python
import streamlit as st

placeholder = st.empty()        # single slot, fully replaceable
if st.button("Update"):
    placeholder.write("Changed content")

with st.container():            # holds many elements
    st.write("First element in the container")
    st.button("Button inside the container")
```

## Q32: How do you handle long-running computations?
**A:** Use @st.cache_data to cache results. For truly long computations (minutes): display progress with st.progress() inside the function, use st.status() for status updates, break computation into chunks. Consider offloading to background threads with st.rerun() when done. Avoid blocking the UI — use async patterns.

**Code:**
```python
import time
import streamlit as st

@st.cache_data
def compute(n):
    total = 0
    for i in range(n):
        time.sleep(0.1)
        total += i
    return total

if st.button("Run the long computation"):
    with st.spinner("Computing..."):
        st.write("Result:", compute(10))
```

## Q33: What is the session state and how is it scoped?
**A:** st.session_state is a dictionary-like object scoped to a single browser session (tab). It persists across re-runs but not across different users/tabs. Keys are strings. Initialize: if 'key' not in st.session_state: st.session_state.key = value. Widgets with key parameter automatically bind to state. Clear with st.session_state.clear().

**Code:**
```python
import streamlit as st

if "user" not in st.session_state:
    st.session_state.user = "guest"

st.write("Scoped to THIS tab/session:", st.session_state.user)

if st.button("Clear session"):
    st.session_state.clear()
    st.rerun()
```

## Q34: How do you bind a widget to session state?
**A:** Widgets with a key parameter auto-sync to st.session_state: st.slider('x', 0, 10, key='slider') makes st.session_state.slider available. You can also set st.session_state.slider = 5 before the widget to set initial value. Widget state persists across re-runs.

**Code:**
```python
import streamlit as st

st.slider("Pick a number", 0, 100, key="slider")
st.write("Live session state value:", st.session_state.slider)
```

## Q35: What is the callback parameter in widgets?
**A:** Widgets can have an on_change callback: st.selectbox('Options', ['a', 'b'], on_change=callback_fn, args=(arg,), kwargs={'kw': val}). The callback executes during the re-run triggered by the widget change. Useful for: updating other state, triggering side effects, or validation. Keep callbacks simple.

**Code:**
```python
import streamlit as st

def on_change():
    st.session_state.last_value = st.session_state.num

st.number_input("Number", value=0, key="num", on_change=on_change)
st.write("Last value recorded by the callback:",
         st.session_state.get("last_value", "none yet"))
```

## Q36: How do you handle secrets in Streamlit?
**A:** Store secrets in .streamlit/secrets.toml (local) or configure in Cloud dashboard. Access: st.secrets["api_key"] or st.secrets["db"]["password"]. Secrets are loaded as environment variables in Cloud. Supported in Community Cloud, self-hosted, and Hugging Face Spaces.

**Code:**
```python
import streamlit as st

# .streamlit/secrets.toml
#   api_key = "sk-1234"
#   [db]
#   password = "s3cret"

if "api_key" in st.secrets:
    st.write("API key is configured (length):",
             len(st.secrets["api_key"]))
else:
    st.error("Missing api_key in secrets.toml")
```

## Q37: How do you deploy a Streamlit app?
**A:** Options: 1) Streamlit Community Cloud (free, connected to GitHub repo), 2) Hugging Face Spaces, 3) Streamlit for Teams, 4) Self-hosted with Docker, 5) AWS/GCP/Azure via custom containers. For Docker: FROM python:3.11; RUN pip install streamlit; COPY app.py; CMD streamlit run app.py --server.port=$PORT.

**Code:**
```python
# Dockerfile
FROM python:3.11-slim
RUN pip install streamlit
COPY app.py .
CMD ["streamlit", "run", "app.py", "--server.port=8501"]
```

## Q38: How do you use environment variables in Streamlit?
**A:** Access via os.environ["MY_VAR"] (standard Python). Set locally: export MY_VAR=value. Set in Cloud: via Secrets/Env vars. st.secrets is an alias for environment variables in Cloud. For local dev: use .streamlit/secrets.toml or .env with python-dotenv.

**Code:**
```python
import os
import streamlit as st

# Terminal: export MY_VAR=world
value = os.environ.get("MY_VAR", "default")
st.write("MY_VAR =", value)
```

## Q39: What are the theming options in Streamlit?
**A:** Configure in .streamlit/config.toml: [theme] primaryColor, backgroundColor, secondaryBackgroundColor, textColor, font (sans serif/serif/monospace). Programmatic: st.set_page_config(page_title="Title"). No full custom theme switching at runtime (must be per-app config).

**Code:**
```python
# .streamlit/config.toml
[theme]
primaryColor = "#7C1F80"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"

# And per-page in Python:
import streamlit as st
st.set_page_config(page_title="Themed app", page_icon="🎨")
```

## Q40: How do you create a download button?
**A:** st.download_button("Download CSV", data=df.to_csv(), file_name="data.csv", mime="text/csv"). data can be: string, bytes, or file-like. For DataFrames: st.download_button("Download", df.to_csv(index=False), "data.csv"). For images/binary: open file in rb mode and pass bytes.

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})

st.download_button(
    "Download CSV",
    data=df.to_csv(index=False),
    file_name="data.csv",
    mime="text/csv",
)
```

## Q41: How do you handle images in Streamlit?
**A:** st.image(image, caption="My Image", width=300) — display image from URL, file, numpy array, or PIL. st.image("https://image.png"), st.image(loaded_image). Multiple images: st.image([img1, img2], width=200). Use columns for side-by-side: col1.image(img1); col2.image(img2).

**Code:**
```python
import numpy as np
import streamlit as st

img = np.random.rand(100, 100, 3)              # RGB numpy array
st.image(img, caption="Generated image", width=200)

col1, col2 = st.columns(2)
with col1:
    st.image(img, caption="Left", width=150)
with col2:
    st.image(img, caption="Right", width=150)
```

## Q42: How do you handle audio and video?
**A:** st.audio(audio_file, format="audio/wav") — play audio from bytes or file. st.video(video_file, format="video/mp4") — play video. Support: local files, URLs (YouTube), byte data, and file uploaders. Controls: autoplay, start_time, subtitles (for video).

**Code:**
```python
import streamlit as st

with open("audio.mp3", "rb") as f:
    st.audio(f.read(), format="audio/mp3")

st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
```

## Q43: What is st.chat_input and st.chat_message?
**A:** st.chat_input("Type a message...") — chat input box, returns string (or None). st.chat_message("user"): — message container with avatar. Pattern: prompt = st.chat_input("Say something"); if prompt: st.chat_message("user").write(prompt); st.chat_message("assistant").write(response). Built-in for building chat UIs.

**Code:**
```python
import streamlit as st

prompt = st.chat_input("Say something")
if prompt:
    st.chat_message("user").write(prompt)
    st.chat_message("assistant").write(f"You said: {prompt}")
```

## Q44: How do you build a chatbot in Streamlit?
**A:** Pattern: 1) Initialize messages in session state: if "messages" not in st.session_state: st.session_state.messages = []. 2) Display existing messages: for msg in st.session_state.messages: st.chat_message(msg["role"]).write(msg["content"]). 3) Handle input: if prompt := st.chat_input(): append, get response from LLM, append response, st.rerun().

**Code:**
```python
import streamlit as st

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input("Ask something"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.messages.append(
        {"role": "assistant", "content": "Echo: " + prompt})
    st.rerun()
```

## Q45: How do you use st.chat_input with LLMs?
**A:** Combine with OpenAI API: def get_response(prompt, history): response = client.chat.completions.create(model="gpt-4o", messages=history); return response.choices[0].message.content. Store full message history in session state. Display streaming responses with st.write_stream(response_generator).

**Code:**
```python
import streamlit as st
from openai import OpenAI

client = OpenAI(api_key=st.secrets["openai"]["api_key"])

def get_response(messages):
    resp = client.chat.completions.create(
        model="gpt-4o-mini", messages=messages)
    return resp.choices[0].message.content

if prompt := st.chat_input("Ask the model"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st.write(get_response([{"role": "user", "content": prompt}]))
```

## Q46: What is st.write_stream?
**A:** st.write_stream(generator) streams text token by token, updating the UI in real-time. Takes a generator yielding strings. Used with LLM streaming: def stream_response(): for chunk in client.chat.completions.create(..., stream=True): yield chunk.choices[0].delta.content or "". Displays incremental output without blocking.

**Code:**
```python
import streamlit as st

def word_stream():
    for word in ["Hello", " ", "Streamlit", " ", "world", "!"]:
        yield word

st.write_stream(word_stream())  # renders tokens as they arrive
```

## Q47: What are the performance best practices for Streamlit?
**A:** 1) Cache computations with @st.cache_data, 2) Use @st.cache_resource for DB connections and models, 3) Lazy-load expensive visualizations, 4) Avoid large data in session state, 5) Use st.empty() for dynamic content, 6) Use st.form for batch inputs, 7) Minimize imports at top level.

**Code:**
```python
import streamlit as st

@st.cache_data
def load_data():
    return {"rows": 1000}

@st.cache_resource
def get_client():
    return {"conn": "reused connection"}

st.write(load_data())
st.write(get_client())
```

## Q48: How do you handle large datasets in Streamlit?
**A:** Use @st.cache_data to avoid re-reading. For display: st.dataframe handles large data with virtual scrolling. For large downloads: use st.download_button with streaming. For processing: use chunked reading (pd.read_csv(chunksize=10000)). Consider using st.data_editor with num_rows="fixed" for performance.

**Code:**
```python
import pandas as pd
import streamlit as st

@st.cache_data
def load_big_data():
    return pd.DataFrame({"x": range(100_000)})

df = load_big_data()
st.dataframe(df.head(50))  # virtual scrolling handles the rest
```

## Q49: How do you connect Streamlit to a database?
**A:** Use st.connection (Streamlit native): conn = st.connection("my_db", type="sql"). conn.query("SELECT * FROM table") returns DataFrame. Supports: PostgreSQL, MySQL, SQLite, Snowflake, BigQuery. For custom connections: create subclass of BaseConnection. Manages connection pooling and secrets automatically.

**Code:**
```python
import streamlit as st

conn = st.connection(
    "local_db",
    type="sql",
    url="sqlite:///chinook.db",
)

df = conn.query("SELECT * FROM albums LIMIT 5")
st.dataframe(df)
```

## Q50: What is st.connection?
**A:** st.connection is Streamlit's unified database connection API (since 1.28). Configured via secrets.toml: [connections.my_db] url="postgresql://...". Usage: conn = st.connection("my_db", type="sql"); df = conn.query("SELECT * FROM table", ttl=3600). Supports caching, pooling, and auto-configuration.

**Code:**
```python
import streamlit as st

conn = st.connection("my_db", type="sql")

df = conn.query("SELECT * FROM users", ttl=3600)
st.dataframe(df)
```
## Q51: How do you connect Streamlit to Snowflake/BigQuery?
**A:** Use st.connection with appropriate dialect: conn = st.connection("snowflake", type="sql"). Configure secrets. For BigQuery: use st.connection("bigquery", type="sql") with Google credentials in secrets. Streamlit manages the connection lifecycle and provides built-in caching.

**Code:**
```python
import streamlit as st

# Snowflake connection configured via secrets.toml
conn = st.connection("snowflake", type="sql")

df = conn.query("SELECT * FROM my_db.hr.employees LIMIT 10")
st.dataframe(df)
```

## Q52: How do you use st.experimental_connection (legacy)?
**A:** st.experimental_connection("my_db", type="sql") is the precursor to st.connection. Same API but experimental. st.connection is now stable. For custom connections: class MyConn(st.experimental_connection): def _connect(self, **kwargs): return create_connection(); def query(self, sql): return self._instance.execute(sql).

**Code:**
```python
import streamlit as st

# Legacy API (superseded by st.connection)
conn = st.experimental_connection("my_db", type="sql")

df = conn.query("SELECT 1 AS x")
st.write(df)
```

## Q53: How do you test Streamlit apps?
**A:** Use streamlit.testing module (v1.36+): from streamlit.testing.v1 import AppTest; at = AppTest.from_file("app.py"); at.run(); assert at.markdown[0].value == "Expected". Simulates interactions: at.button[0].click().at.run(). Check widget values and outputs. Headless testing without browser.

**Code:**
```python
from streamlit.testing.v1 import AppTest

at = AppTest.from_file("app.py", default_timeout=20)
at.run()
assert at.title[0].value == "My App"

at.button[0].click().run()
assert at.markdown[0].value == "Clicked!"
```

## Q54: How do you use Streamlit with Docker?
**A:** Dockerfile: FROM python:3.11-slim; WORKDIR /app; COPY requirements.txt .; RUN pip install -r requirements.txt; COPY . .; EXPOSE 8501; CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.enableCORS=false"]. For Cloud Run: use --server.port=$PORT and --server.headless=true.

**Code:**
```python
# Dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py",
     "--server.port=8501",
     "--server.enableCORS=false"]
```

## Q55: How do you handle authentication in Streamlit?
**A:** Options: 1) st.secrets stored passwords (simple), 2) st.experimental_user (Streamlit Cloud auth), 3) OAuth via third-party (Auth0, Clerk, Firebase), 4) Custom login with st.text_input and session state. Streamlit Community Cloud has built-in auth via st.experimental_user (email-based).

**Code:**
```python
import streamlit as st

user = st.text_input("Username")
password = st.text_input("Password", type="password")

if st.button("Log in"):
    if password == st.secrets.get("app_password"):
        st.session_state.authenticated = True

if not st.session_state.get("authenticated"):
    st.warning("Please log in")
    st.stop()

st.success(f"Welcome, {user}!")
```

## Q56: What is st.experimental_user?
**A:** st.experimental_user provides authentication info for Streamlit Community Cloud apps. st.experimental_user.email, st.experimental_user.logged_in. Requires enabling auth in app settings. Not available in local dev or other deployment platforms. Use st.secrets for local auth prototyping.

**Code:**
```python
import streamlit as st

if st.experimental_user.logged_in:
    st.write("Logged in as:", st.experimental_user.email)
else:
    st.write("Please sign in (Streamlit Cloud auth)")
```

## Q57: How do you configure Streamlit server settings?
**A:** Via .streamlit/config.toml: [server] port=8501, headless=true, enableCORS=false, enableXsrfProtection=true, maxUploadSize=200, runOnSave=true. Or CLI args: --server.port 8501. Environment vars: STREAMLIT_SERVER_PORT=8501.

**Code:**
```python
# .streamlit/config.toml
[server]
port = 8501
headless = true
enableCORS = false
enableXsrfProtection = true
maxUploadSize = 200
runOnSave = true

# Or as CLI / env: streamlit run app.py --server.port 8501
#                    STREAMLIT_SERVER_PORT=8501 streamlit run app.py
```

## Q58: How do you set the maximum upload size?
**A:** In .streamlit/config.toml: [server] maxUploadSize = 200 (in MB, default 200). Adjust for large file uploads. Also consider: client-side chunking for very large files, direct-to-cloud upload (presigned URLs), or file size validation before processing.

**Code:**
```python
# .streamlit/config.toml
[server]
maxUploadSize = 500   # allow uploads up to 500 MB
```
```python
import streamlit as st

uploaded = st.file_uploader("Upload a large file")
if uploaded is not None:
    if uploaded.size > 500 * 1024 * 1024:
        st.error("File too large (max 500 MB)")
    st.write("Name:", uploaded.name)
```

## Q59: How do you use caching with data that changes?
**A:** Use @st.cache_data(ttl=3600) for time-based expiration. Use @st.cache_data(max_entries=10) to limit cache size. Clear programmatically: st.cache_data.clear(). Use hash_funcs parameter for custom hashing of unhashable types: @st.cache_data(hash_funcs={pd.DataFrame: hash_dataframe}).

**Code:**
```python
import streamlit as st

@st.cache_data(ttl=30, max_entries=10)
def get_price():
    return {"price": 100}

st.write(get_price())

if st.button("Force refresh (clear cache)"):
    st.cache_data.clear()
    st.rerun()
```

## Q60: What is the hash_funcs parameter in caching?
**A:** hash_funcs provides custom hash functions for unhashable types in cached function arguments. Example: @st.cache_data(hash_funcs={CustomObject: lambda obj: obj.id}). Required when arguments include types Streamlit can't hash (custom objects, database connections). Otherwise, caching fails.

**Code:**
```python
import streamlit as st

class CustomObject:
    def __init__(self, id):
        self.id = id

@st.cache_data(hash_funcs={CustomObject: lambda o: o.id})
def process(obj):
    return obj.id * 2

st.write(process(CustomObject(21)))
```

## Q61: How do you debug a Streamlit app?
**A:** 1) st.write() to inspect variables, 2) st.json() for structured data, 3) st.stop() to halt execution at a point, 4) Python logging to terminal (streamlit run outputs logs), 5) st.exception() to show tracebacks, 6) st.help() for object documentation, 7) st.html(debug_info) for custom debugging.

**Code:**
```python
import streamlit as st

x = {"a": 1, "b": [2, 3]}
st.write("Inspect variable:", x)   # 1
st.json(x)                          # 2
st.help(st.dataframe)               # 6
```

## Q62: What is st.stop?
**A:** st.stop() halts the current script execution without raising an error. Useful for early returns in conditional logic, preventing execution of code below a certain point. Example: if not st.session_state.logged_in: st.warning("Please log in"); st.stop(); # rest of app.

**Code:**
```python
import streamlit as st

if not st.session_state.get("logged_in"):
    st.warning("Please log in")
    st.stop()           # rest of the script is skipped

st.write("Only reached when logged in")
```

## Q63: How do you format numbers and dates in Streamlit?
**A:** Use column_config in data_editor and dataframe: st.data_editor(df, column_config={"price": st.column_config.NumberColumn(format="$%.2f"), "date": st.column_config.DateColumn(format="DD/MM/YYYY")}). Creates formatted display without modifying underlying data. Also: st.column_config.TextColumn, SelectboxColumn, BarChartColumn, ProgressColumn.

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({
    "price": [9.5, 12.0],
    "date": pd.to_datetime(["2024-01-01", "2024-02-01"]),
})

st.data_editor(
    df,
    column_config={
        "price": st.column_config.NumberColumn(format="$%.2f"),
        "date": st.column_config.DateColumn(format="DD/MM/YYYY"),
    },
)
```

## Q64: What is column_config in Streamlit?
**A:** column_config customizes column display in st.dataframe and st.data_editor. Options: label (header), help (tooltip), width, disabled, required. Type-specific: NumberColumn (format, min, max), TextColumn (max_chars, validate), LinkColumn, ImageColumn, ProgressColumn, ListColumn.

**Code:**
```python
import streamlit as st

st.dataframe(
    {"name": ["alice"], "url": ["https://docs.streamlit.io"]},
    column_config={
        "name": st.column_config.TextColumn("Display name", help="Tooltip"),
        "url": st.column_config.LinkColumn("Docs", display_text="Open docs"),
    },
)
```

## Q65: How do you create a column with progress bars in a DataFrame?
**A:** st.data_editor(df, column_config={"completion": st.column_config.ProgressColumn("Progress", format="%d%%", min_value=0, max_value=100)}). Displays progress bars inline in the table cell. Works with data_editor and dataframe. Values mapped to bar width based on min/max.

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"task": ["A", "B"], "completion": [40, 80]})

st.dataframe(
    df,
    column_config={
        "completion": st.column_config.ProgressColumn(
            "Progress", format="%d%%", min_value=0, max_value=100),
    },
)
```

## Q66: How do you use st.fragment?
**A:** @st.fragment decorator creates a lazy-loaded section of the app. The fragment runs independently of the main script and can update itself without re-running the entire app. Useful for: polling data, background updates, periodic refreshes. Parameters: run_every=N seconds for auto-refresh.

**Code:**
```python
import time
import streamlit as st

@st.fragment(run_every=5)
def clock():
    st.write("Server time:", time.time())

clock()
st.button("Main script — clicking does not rebuild the fragment")
```

## Q67: What is st.query_params?
**A:** st.query_params provides access to URL query parameters: st.query_params["key"] reads, st.query_params["key"] = "value" sets. Enables: deep linking, sharing app state via URL, bookmarkable views. Changes update the URL without full page reload. st.query_params.clear() to reset.

**Code:**
```python
import streamlit as st

key = st.query_params.get("key", "default")
st.write("Read from URL:", key)

if st.button("Set ?key=value in the URL"):
    st.query_params["key"] = "value"
```

## Q68: How do you handle WebSocket connections in Streamlit?
**A:** Streamlit uses WebSockets internally for server-client communication. For custom WebSocket handling: use st.websocket (experimental) or manage WebSocket connections outside Streamlit (asyncio) and update session state. For real-time data: poll with @st.fragment(run_every=1) or connect via st_websocket_library.

**Code:**
```python
import random
import streamlit as st

# Nearest practical equivalent: auto-refreshing fragment
@st.fragment(run_every=2)
def live_updates():
    st.line_chart([random.random() for _ in range(10)])

live_updates()
```

## Q69: How do you use Streamlit with async code?
**A:** Streamlit runs synchronously by default. For async: use asyncio.run() within cached functions, or use st.experimental_fragment with async. For API calls: use synchronous versions (requests) rather than async (httpx) to avoid compatibility issues. Newer versions improve async support.

**Code:**
```python
import asyncio
import streamlit as st

async def fetch_async():
    await asyncio.sleep(0.1)
    return {"data": 42}

@st.cache_data
def fetch():
    return asyncio.run(fetch_async())

st.write(fetch())
```

## Q70: What are common Streamlit anti-patterns?
**A:** 1) Modifying session state inside cached functions, 2) Large data in session state (should use cache), 3) Expensive computations without caching, 4) Widget callbacks that modify the same widget's value (infinite loop), 5) Using st.stop() excessively, 6) Not using st.form for multi-widget input.

**Code:**
```python
import time
import streamlit as st

# Anti-pattern: re-computing expensive work on every re-run.
# Fix: wrap in @st.cache_data.
def load_big_data():
    time.sleep(1)
    return list(range(100))

data = load_big_data()
st.write("Loaded", len(data), "rows")
```

## Q71: How do you handle multiple users and concurrency?
**A:** Each user gets their own session with isolated session state. Streamlit server handles concurrency via thread-per-session. For shared state across users: use external storage (database, Redis). For rate limiting: implement at the application or infrastructure level. For computation: use background workers.

**Code:**
```python
import streamlit as st

# Session state is isolated per user/browser tab
if "user" not in st.session_state:
    st.session_state.user = "anonymous"

st.write("Per-user state:", st.session_state.user)
```

## Q72: What is the Streamlit config system?
**A:** Streamlit uses a layered config system (highest to lowest priority): 1) CLI flags, 2) Environment variables, 3) config.toml file, 4) Default values. Config file path: .streamlit/config.toml (project-level) or ~/.streamlit/config.toml (global). Covers server, theme, browser, runner, and logger settings.

**Code:**
```python
# Priority: CLI flags > env vars > config.toml > defaults
#
# CLI flag:                  streamlit run app.py --server.port 8502
# Env var:                   STREAMLIT_SERVER_PORT=8502 streamlit run app.py
#
# .streamlit/config.toml (lowest explicit layer)
[server]
port = 8501

[theme]
primaryColor = "#1E88E5"
```

## Q73: How do you enable CORS in Streamlit?
**A:** Streamlit doesn't typically need CORS as apps are opened directly. For embedding in iframes: --server.enableCORS=true. For custom domains: configure --server.enableXsrfProtection=false (if needed). For production: use a reverse proxy (nginx, Caddy) to handle CORS.

**Code:**
```python
# streamlit run app.py --server.enableCORS=true
#
# or in .streamlit/config.toml
[server]
enableCORS = true
enableXsrfProtection = true
```

## Q74: How do you embed Streamlit in iframes?
**A:** Set --server.enableCORS=false and --server.enableXsrfProtection=false. Use iframe: <iframe src="https://yourapp.streamlit.app?embed=true" width="800" height="600"></iframe>. The ?embed=true removes some UI chrome. For Streamlit Cloud, embedding must be enabled in app settings.

**Code:**
```python
# Launch flags needed for embedding:
#   streamlit run app.py --server.enableCORS=false --server.enableXsrfProtection=false
#
# Hosting page:
# <iframe src="https://your-app.streamlit.app?embed=true"
#         width="800" height="600"></iframe>
```

## Q75: What is the difference between Streamlit and Dash?
**A:** Streamlit: simpler, Python-only, script re-run model, faster prototyping, less customizable. Dash: callback-based, React components, more customizable, steeper learning curve, enterprise features (authentication, URL routing). Streamlit is better for data scientists; Dash for production dashboards with complex interactions.

**Code:**
```python
# In Streamlit the reactive model replaces Dash callbacks:
import streamlit as st

value = st.slider("Pick a value", 0, 100)  # re-runs on interaction
st.write(f"Value: {value}")
```
## Q76: How do you use Streamlit with machine learning models?
**A:** 1) Load model with @st.cache_resource (runs once), 2) Get user input via widgets, 3) Preprocess input, 4) Run model.predict(), 5) Display results. Example: model = st.cache_resource(load_model)(); input_data = st.text_input("Enter features"); if input_data: result = model.predict([parse(input_data)]); st.write(result).

**Code:**
```python
import streamlit as st
from sklearn.ensemble import RandomForestRegressor

@st.cache_resource
def load_model():
    return RandomForestRegressor(n_estimators=10, random_state=0)

model = load_model()
size = st.slider("House size (m²)", 50, 300, 120)
pred = model.predict([[size]])
st.metric("Predicted price", f"${pred[0]:,.0f}")
```

## Q77: How do you use Streamlit with LangChain?
**A:** Build chat UI: st.chat_message for history, st.chat_input for input, st.write_stream for streaming responses. Use session state for message history. Cache LangChain chain: @st.cache_resource def load_chain(): return create_rag_chain(retriever, model). Chain.invoke(input, config=...) with streaming callbacks.

**Code:**
```python
import streamlit as st
from langchain_openai import ChatOpenAI

@st.cache_resource
def get_model():
    return ChatOpenAI(model="gpt-4o-mini")

if prompt := st.chat_input("Ask your RAG app"):
    st.chat_message("user").write(prompt)
    with st.chat_message("assistant"):
        st.write(get_model().invoke(prompt).content)
```

## Q78: How do you create a PDF viewer or report in Streamlit?
**A:** Display PDF: st.write with iframe: st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>', unsafe_allow_html=True). For generated PDFs: use st.download_button with reportlab/weasyprint. For PDF parsing: PyPDF2, pdfplumber. For slides: st.slides (Streamlit Labs).

**Code:**
```python
import streamlit as st

pdf_url = ("https://www.w3.org/WAI/ER/tests/xhtml/testfiles/"
           "resources/pdf/dummy.pdf")
st.markdown(
    f'<iframe src="{pdf_url}" width="100%" height="600"></iframe>',
    unsafe_allow_html=True,
)
```

## Q79: How do you use Streamlit with Plotly Dashboards?
**A:** Combine Plotly with Streamlit: import plotly.express as px; fig = px.scatter(df, x='x', y='y', color='category'); st.plotly_chart(fig, use_container_width=True). Use st.selectbox to change chart parameters, st.slider for date ranges. Plotly charts are interactive with hover, zoom, and selection.

**Code:**
```python
import plotly.express as px
import streamlit as st

df = px.data.gapminder()
year = st.slider("Year", 1952, 2007, 2007)
fig = px.scatter(
    df[df["year"] == year],
    x="gdpPercap", y="lifeExp", color="continent", log_x=True,
    hover_name="country",
)
st.plotly_chart(fig, use_container_width=True)
```

## Q80: How do you handle real-time data updates?
**A:** Options: 1) @st.fragment(run_every=5) — auto-refresh every 5 seconds, 2) st.rerun() triggered by external events, 3) WebSocket connection via custom component, 4) Polling with time.sleep() in a loop (not recommended — blocks UI). For true real-time: use custom component with WebSocket.

**Code:**
```python
import random
import streamlit as st

@st.fragment(run_every=5)
def live_sensor():
    value = random.randint(0, 100)
    st.metric("Sensor reading", value, delta="live")

live_sensor()
```

## Q81: How do you use st.popover?
**A:** st.popover("Settings") creates a toggleable popup container. Usage: with st.popover("Filters"): option = st.selectbox("Category", options); value = st.slider("Range"). The popover shows/hides on click. Useful for: filters, settings, and secondary controls without cluttering the main UI.

**Code:**
```python
import streamlit as st

with st.popover("Filters"):
    category = st.selectbox("Category", ["A", "B"])
    value = st.slider("Range", 0, 100, 50)

st.write(f"Selected: {category}, range = {value}")
```

## Q82: What are Streamlit's accessibility features?
**A:** Streamlit supports: semantic HTML, ARIA labels via help parameter on widgets (help="Description for screen readers"), keyboard navigation, focus management, high contrast themes, and configurable fonts. st.set_page_config provides page title and icon. Custom CSS can improve accessibility further.

**Code:**
```python
import streamlit as st

st.set_page_config(page_title="Accessible app", page_icon="♿")
st.text_input(
    "Search",
    help="Type here to filter the results (read out by screen readers)",
)
```

## Q83: How do you create custom Streamlit components?
**A:** Custom components use HTML/JS/TS to add new UI elements. Use streamlit-component-template. Steps: 1) Create Python API, 2) Build frontend with any framework (React, Vue, Svelte), 3) Use Streamlit's component API to send/receive data. Publish via PyPI. Example components: st_aggrid, streamlit-plotly-events.

**Code:**
```python
import streamlit as st
import streamlit.components.v1 as components

# Inline custom HTML/JS without building a full component
components.html(
    "<h1>Custom HTML component</h1>"
    "<button onclick=\"alert('Hi from a component')\">Click</button>",
    height=200,
)
```

## Q84: What is the Streamlit Component API?
**A:** The component API allows bidirectional communication between Python and frontend. Python side: component = declare_component("my_component", url="http://localhost:3001"); value = component(arg="data"). Frontend: StreamlitComponent class from streamlit-component-lib handles callbacks and data serialization.

**Code:**
```python
from streamlit.components.v1 import declare_component

# Python API of a custom component (frontend served by the template)
my_component = declare_component("my_component", url="http://localhost:3001")

value = my_component(name="world")   # receives a value back from the frontend
print(value)
```

## Q85: How do you use Streamlit's session state across pages?
**A:** st.session_state is shared across all pages in a multi-page app. A value set on page 1 is accessible on page 2. Use for: user authentication, shared data, app-wide settings, navigation state. Clear on logout: for key in list(st.session_state.keys()): del st.session_state[key].

**Code:**
```python
import streamlit as st

# Set on page 1:
st.session_state["shared"] = "value from page 1"

# Read on page 2 (same session):
st.write("Shared across pages:", st.session_state.get("shared"))

if st.button("Log out (clear all keys)"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()
```

## Q86: How do you use Streamlit with Google Analytics?
**A:** Inject GA script via st.markdown with unsafe_allow_html: st.markdown('<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXX"></script><script>window.dataLayer = window.dataLayer || []; function gtag(){dataLayer.push(arguments);} gtag("js", new Date()); gtag("config", "G-XXXXX");</script>', unsafe_allow_html=True). Track custom events via st.markdown with JS.

**Code:**
```python
import streamlit as st

GA_ID = "G-XXXXXXXXXX"

st.markdown(
    f'''<script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
<script>
window.dataLayer = window.dataLayer || [];
function gtag() {{ dataLayer.push(arguments); }}
gtag("js", new Date());
gtag("config", "{GA_ID}");
</script>''',
    unsafe_allow_html=True,
)
st.write("GA tag injected for pageview tracking")
```

## Q87: How do you use Streamlit with Snowflake?
**A:** conn = st.connection("snowflake", type="sql") configured via secrets.toml with account, user, password, warehouse, database, schema. Or use Snowpark: from snowflake.snowpark import Session; session = Session.builder.configs(st.secrets["snowflake"]).create(). Streamlit in Snowflake (SiS) provides native integration.

**Code:**
```python
import streamlit as st

conn = st.connection("snowflake", type="sql")
df = conn.query("SELECT * FROM analytics.dim_customers LIMIT 10")
st.dataframe(df)
```

## Q88: What is Streamlit in Snowflake (SiS)?
**A:** SiS allows running Streamlit apps directly inside Snowflake, with native SQL/Snowpark access. Apps are stored as stages in Snowflake. Benefits: no data movement (compute near data), built-in authentication, automatic scaling. Limitations: limited Python packages, no custom components.

**Code:**
```python
import streamlit as st

# Inside a SiS app you skip connection setup —
# the session is provided by Snowflake natively.
from snowflake.snowpark.context import get_active_session

session = get_active_session()
df = session.sql("SELECT * FROM my_marketplace_table LIMIT 5").collect()
st.dataframe(df)
```

## Q89: How do you use Streamlit with Hugging Face Spaces?
**A:** Create a Space on HF, set SDK to Streamlit, push code via Git. requirements.txt for dependencies, packages.txt for system deps. Streamlit apps on Spaces benefit from: free GPU (if configured), community features, easy sharing. Access hardware: se选题 GPU upgrade in Space settings.

**Code:**
```python
# requirements.txt (installed on the Space)
streamlit
pandas
```
```python
# app.py
import streamlit as st

st.title("Deployed on Hugging Face Spaces")
st.write("Push this file to your Space's repo to deploy.")
```

## Q90: How do you build a Streamlit app for a hackathon?
**A:** Quick start: 1) pip install streamlit, 2) Create app.py with title and layout, 3) Use st.cache_data for heavy ops, 4) Deploy to Streamlit Cloud (connect GitHub repo, free tier), 5) Polish with st.columns, st.tabs, st.metrics. Focus on working demo over perfect code.

**Code:**
```python
import random
import streamlit as st

st.set_page_config(page_title="Hackathon Demo", layout="wide")
st.title("🚀 Hackathon Demo")

col1, col2, col3 = st.columns(3)
col1.metric("Users", 1_024, "12%")
col2.metric("Revenue", "$1.2K", "$0.3K")
col3.metric("Latency", "89ms", "-4ms")

df = st.session_state.setdefault("df", {"x": range(10),
                                        "y": [random.random() for _ in range(10)]})
st.line_chart(df)
```

## Q91: How do you use Streamlit with API backends?
**A:** Call REST APIs via requests library: response = requests.get("https://api.example.com/data", headers={"Authorization": f"Bearer {st.secrets['api_key']}"}); data = response.json(). Cache API results with @st.cache_data(ttl=300) to avoid rate limits. Use st.status for API call progress.

**Code:**
```python
import requests
import streamlit as st

@st.cache_data(ttl=300)
def fetch_repo():
    resp = requests.get(
        "https://api.github.com/repos/streamlit/streamlit",
        timeout=10,
    )
    return resp.json()

with st.status("Calling the GitHub API..."):
    data = fetch_repo()
st.write("Stars:", data["stargazers_count"])
```

## Q92: How do you implement search in Streamlit?
**A:** st.search = st.text_input("Search", placeholder="Type to search..."); filtered_df = df[df.apply(lambda row: search_term.lower() in str(row).lower(), axis=1)]. For better performance: use st.dataframe with built-in column search, or use df.query() for structured search. For full-text: consider Elasticsearch integration.

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"name": ["alice", "bob", "carol", "dave"]})

term = st.text_input("Search", placeholder="Type to filter...")
if term:
    df = df[df["name"].str.contains(term, case=False)]

st.dataframe(df)
```

## Q93: How do you use pagination in Streamlit?
**A:** Implement manual pagination: page_size = 10; total_pages = len(df) // page_size + 1; page = st.selectbox("Page", range(total_pages)); start = page * page_size; st.dataframe(df.iloc[start:start+page_size]). Or use st.dataframe with built-in virtual scrolling (handles large data without explicit pagination).

**Code:**
```python
import pandas as pd
import streamlit as st

df = pd.DataFrame({"x": range(100)})
page_size = 10
page = st.selectbox("Page", range(0, len(df), page_size))
st.dataframe(df.iloc[page:page + page_size])
```

## Q94: How do you handle user sessions with login?
**A:** Basic approach: st.text_input for username/password, check against st.secrets, set st.session_state.authenticated = True. For OAuth: use Auth0 or Clerk integration. For Streamlit Cloud: use st.experimental_user for email-based auth. Redirect: check auth at app start, st.stop() if not authenticated.

**Code:**
```python
import streamlit as st

st.text_input("Username", key="username")
st.text_input("Password", type="password", key="password")

if st.button("Log in"):
    valid = st.secrets.get("password") == st.session_state.password
    st.session_state.authenticated = valid

if not st.session_state.get("authenticated"):
    st.warning("Log in to continue")
    st.stop()

st.success(f"Welcome, {st.session_state.username}!")
```

## Q95: How do you use Streamlit with FastAPI?
**A:** Run Streamlit and FastAPI separately. Streamlit handles UI, FastAPI handles API. Communication: Streamlit calls FastAPI via requests (localhost or deployed URL). For auth: share tokens via session state. For deployment: use docker-compose with both services or deploy separately.

**Code:**
```python
# api/main.py
from fastapi import FastAPI

app = FastAPI()

@app.get("/predict")
def predict(text: str):
    return {"prediction": f"processed: {text}"}
```
```python
# app.py (Streamlit UI)
import requests
import streamlit as st

text = st.text_input("Input text")
if st.button("Predict"):
    resp = requests.get(
        "http://localhost:8000/predict", params={"text": text}, timeout=10)
    st.write(resp.json())
```

## Q96: What is the Streamlit roadmap and future?
**A:** Key focus areas: improved performance (faster re-runs), better multi-page apps, enhanced data editor, native state management, improved theming, better async support, AI/ML integrations, lower latency streaming, and expanded component ecosystem. Streamlit is actively developed by Snowflake.

**Code:**
```python
import streamlit as st

# Follow the official changelog / blog for the roadmap.
st.markdown(
    "Track new releases: "
    "[streamlit.io/changelog](https://docs.streamlit.io/develop/quick-reference/changelog)"
)
```

## Q97: How do you migrate from Streamlit 1.x to 2.x?
**A:** Key changes: st.experimental_* methods promoted to stable (st.connection, st.rerun, st.fragment), deprecated methods removed (st. BetaColumns), improved caching API, new session state semantics. Check deprecation warnings. Main changes: replace st.experimental_rerun with st.rerun, st.cache with @st.cache_data.

**Code:**
```python
import streamlit as st

# Before (1.x): @st.cache
# After (2.x):
@st.cache_data
def load():
    return [1, 2, 3]

# Before (1.x): st.experimental_rerun()
if st.button("Rerun"):
    st.rerun()          # After (2.x): st.rerun()

st.write(load())
```

## Q98: What are the limitations of Streamlit?
**A:** Limitations: 1) No native multi-user auth (use external), 2) Server-rendered (not SPA), 3) Limited customization (no direct HTML/CSS control), 4) Stateless model (full re-run per interaction), 5) Not ideal for SEO, 6) Limited to Python, 7) Performance with 100+ concurrent users needs scaling, 8) No mobile-first design.

**Code:**
```python
import streamlit as st

# The stateless model is the main architectural trade-off:
value = st.slider("Any widget", 0, 10)
st.write(f"Every interaction re-runs the whole script (value = {value})")
```

## Q99: How do you scale Streamlit apps?
**A:** Options: 1) Streamlit Cloud (auto-scaling), 2) Manual scaling with Kubernetes, 3) Load balancer + multiple instances (stateless), 4) Separate computation to background workers, 5) Use external databases instead of in-memory, 6) Cache aggressively, 7) Use CDN for static assets, 8) Session affinity for stateful deployments.

**Code:**
```python
import streamlit as st

@st.cache_data
def load_data():
    return {"records": 1_000_000}

# Cache aggressively so a fleet of instances shares the work
st.write("Loaded", load_data()["records"], "records")
```

## Q100: What are the best Streamlit resources and communities?
**A:** Official: docs.streamlit.io, gallery.streamlit.app (app examples), discuss.streamlit.io (forum), GitHub (source). Community: Awesome Streamlit (curated resources), Streamlit on Reddit, Streamlit Discord, Streamlit Blog, YouTube tutorials, and Streamlit events/conferences.

**Code:**
```python
import streamlit as st

st.subheader("Official resources")
st.link_button("Docs", "https://docs.streamlit.io")
st.link_button("Gallery", "https://gallery.streamlit.app")
st.link_button("Forum", "https://discuss.streamlit.io")
st.link_button("GitHub", "https://github.com/streamlit/streamlit")
```