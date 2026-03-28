# Projects Deep Dive

**Q1. Describe your project "ScriptVector: Hindi Manhwa Content Generator". What were the main challenges?**
**Answer:** ScriptVector uses Gemini API and Agno Agents to automate the generation of long-form Hindi content specifically tailored to Manhwa (webcomics). 
The core challenge was maintaining contextual continuity. Standard LLM calls are stateless, so a story generated in chapter 1 might be forgotten by the LLM in chapter 3. I solved this by integrating an SQLite database to store generated context, character traits, and plot points, creating a custom memory retrieval pipeline that feeds this specific world-state back into the prompt for subsequent generations.

**Q2. Explain the architecture of "OpenRTL.ai".**
**Answer:** OpenRTL.ai is an AI-assisted RTL (Register-Transfer Level) code generation tool. The frontend is built on Streamlit for user interaction. The backend is powered by FastAPI, which exposes RESTful APIs. When a user requests Verilog code, the API creates an asynchronous job. Because AI generation can take seconds to minutes, I designed asynchronous endpoints where the user receives a Job ID immediately and the backend processes the LLM prompt concurrently. The status and generated Verilog code are stored in an SQLite database, monitored via Pandas on the dashboard.

**Q3. How does your "Marketing AI Agent Integration" project work?**
**Answer:** This project acts as an automated marketing team. I integrated APIs from Gemini, Groq, and Hugging Face to generate high-quality text and images. I then integrated the Gmail, Twitter, and YouTube APIs.
The system allows a user to input a single marketing prompt (e.g., "Promote our new AI tool"). The backend agents split the task: one agent writes a thread and posts to Twitter, another drafts a newsletter and sends it via Gmail, and another organizes assets on Google Drive. It is all glued together via a Flask backend and controlled via a protected Streamlit dashboard.

**Q4. What is Cocotb2-Migrator? Explain Abstract Syntax Trees (AST) in this context.**
**Answer:** Cocotb is a Python-based testing framework for hardware design. Between versions 1.x and 2.x, significant API structural changes occurred, breaking old testbenches. 
I created a tool published on PyPI that automates this migration contextually. I used **LibCST** (which uses a Concrete Syntax Tree, a variation of an Abstract Syntax Tree). By converting Python code into a tree structure representing the syntax, my tool programmatically identifies deprecated function calls and structural patterns, and rewrites the tree with the new syntax before compiling it back into raw Python code. This avoids the terrible edge-cases associated with simple Regex find/replaces.

**Q5. In your IEEE Published paper on "Real-Time Face Mask Detection", how did you optimize the ML model?**
**Answer:** For real-time applications (especially video streams), inference speed is just as important as accuracy. We optimized the model by utilizing advanced preprocessing algorithms to normalize and resize the inputs rapidly. We applied transfer learning using a lightweight architecture (like MobileNetV2) rather than a heavy CNN, significantly reducing the parameter count while maintaining accuracy. We also distributed the inference pipeline to ensure it could handle enterprise healthcare camera loads.
