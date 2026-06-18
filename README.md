<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    
</head>
<body>

<h1>Autonomous Research Analyst</h1>

<p align="center">
    <a href="https://research-ai-2rar.onrender.com" target="_blank">
        <img src="https://img.shields.io/badge/Live%20Demo-View%20Application-success?style=for-the-badge&logo=render" alt="Live Demo">
    </a>
</p>

<p align="center">
    <a href="https://research-ai-2rar.onrender.com" target="_blank">
        <strong>Live Application →</strong>
    </a>
</p>

<p>
An AI-powered multi-agent research platform that autonomously conducts market research,
validates information, generates executive-level reports, and exports professional PDF documents.
The system combines planning, web search, fact verification, report writing, and document generation
into a fully automated research workflow.
</p>

<hr>

<h2>Project Overview</h2>

<p>
Autonomous Research Analyst is designed to simulate the workflow of a professional consulting firm
such as McKinsey, Gartner, Deloitte, or BCG.
</p>

<p>
Instead of manually researching a topic, users simply provide a research query and the platform:
</p>

<ol>
    <li>Creates a structured research plan</li>
    <li>Searches trusted web sources</li>
    <li>Validates and summarizes findings</li>
    <li>Generates a professional analyst report</li>
    <li>Exports the report as a PDF</li>
</ol>

<p>
The entire process is powered by multiple specialized AI agents working together in an autonomous workflow.
</p>

<hr>

<h2>Key Features</h2>

<ul>
    <li>Multi-Agent AI Architecture</li>
    <li>Automated Research Planning</li>
    <li>Web Search Integration</li>
    <li>Fact Verification and Confidence Scoring</li>
    <li>Professional Business Report Generation</li>
    <li>PDF Export with Structured Formatting</li>
    <li>Interactive Streamlit Dashboard</li>
    <li>Real-Time Agent Status Tracking</li>
    <li>Research Pipeline Visualization</li>
    <li>Downloadable Executive Reports</li>
</ul>

<hr>

<h2>System Architecture</h2>

<pre>
User Query
    |
    v
Planner Agent
    |
    v
Search Agent
    |
    v
Fact Check Agent
    |
    v
Report Writer Agent
    |
    v
PDF Generator
    |
    v
Final Research Report
</pre>

<hr>

<h2>AI Agent Workflow</h2>

<h3>1. Planner Agent</h3>

<p>
Responsible for converting a user topic into a structured research plan.
</p>

<p><strong>Example Input:</strong></p>

<pre>
Analyze Electric Vehicle Market in India
</pre>

<p><strong>Example Output:</strong></p>

<pre>
1. Market Overview
2. Key Players
3. Government Policies
4. Infrastructure Development
5. Consumer Adoption
6. Supply Chain Analysis
7. Challenges
8. Future Outlook
</pre>

<hr>

<h3>2. Search Agent</h3>

<p>
Uses Tavily Search to gather relevant information from trusted online sources.
</p>

<p><strong>Responsibilities:</strong></p>

<ul>
    <li>Search multiple sources</li>
    <li>Retrieve relevant content</li>
    <li>Collect source URLs</li>
    <li>Prepare research data for verification</li>
</ul>

<hr>

<h3>3. Fact Check Agent</h3>

<p>
Analyzes research findings and validates the quality of information.
</p>

<p><strong>Responsibilities:</strong></p>

<ul>
    <li>Remove weak claims</li>
    <li>Identify key insights</li>
    <li>Extract important statistics</li>
    <li>Assign confidence scores</li>
</ul>

<p><strong>Confidence Levels:</strong></p>

<ul>
    <li>High</li>
    <li>Medium</li>
    <li>Low</li>
</ul>

<hr>

<h3>4. Report Writer Agent</h3>

<p>
Generates a professional consulting-style research report.
</p>

<p>
The report follows a structured format inspired by leading consulting firms.
</p>

<p><strong>Report Sections:</strong></p>

<ul>
    <li>Executive Summary</li>
    <li>Industry Overview</li>
    <li>Market Analysis</li>
    <li>Competitive Landscape</li>
    <li>Technology & Innovation</li>
    <li>Regulatory Environment</li>
    <li>Challenges & Risks</li>
    <li>Opportunities</li>
    <li>Future Outlook</li>
    <li>Strategic Recommendations</li>
    <li>Conclusion</li>
</ul>

<hr>

<h3>5. PDF Generator</h3>

<p>
Converts the final report into a professional PDF document.
</p>

<p><strong>PDF Features:</strong></p>

<ul>
    <li>Cover Page</li>
    <li>Report Title</li>
    <li>Generation Date</li>
    <li>Table of Contents</li>
    <li>Structured Headings</li>
    <li>Page Numbers</li>
    <li>Professional Formatting</li>
</ul>

<hr>

<h2>Technology Stack</h2>

<table border="1" cellpadding="10">
    <tr>
        <th>Category</th>
        <th>Technology</th>
    </tr>
    <tr>
        <td>Frontend</td>
        <td>Streamlit</td>
    </tr>
    <tr>
        <td>LLM</td>
        <td>Google Gemini 2.5 Flash</td>
    </tr>
    <tr>
        <td>Framework</td>
        <td>LangChain</td>
    </tr>
    <tr>
        <td>Search Engine</td>
        <td>Tavily Search API</td>
    </tr>
    <tr>
        <td>PDF Generation</td>
        <td>ReportLab</td>
    </tr>
    <tr>
        <td>Programming Language</td>
        <td>Python</td>
    </tr>
    <tr>
        <td>Environment Management</td>
        <td>Python Dotenv</td>
    </tr>
</table>

<hr>

<h2>Project Structure</h2>

<pre>
research-agent/
│
├── app/
│   │
│   ├── agents/
│   │   ├── planner_agent.py
│   │   ├── search_agent.py
│   │   ├── fact_check_agent.py
│   │   └── report_writer_agent.py
│   │
│   ├── tools/
│   │   └── search_tool.py
│   │
│   └── services/
│       └── pdf_generator.py
│
├── streamlit_app.py
├── requirements.txt
├── .env
├── README.html
└── .gitignore
</pre>

<hr>

<h2>Installation</h2>

<h3>Clone Repository</h3>

<pre>
git clone https://github.com/yourusername/autonomous-research-analyst.git

cd autonomous-research-analyst
</pre>

<h3>Create Virtual Environment</h3>

<pre>
python -m venv venv
</pre>

<h3>Activate Environment</h3>

<pre>
venv\Scripts\activate
</pre>

<h3>Install Dependencies</h3>

<pre>
pip install -r requirements.txt
</pre>

<hr>

<h2>Environment Variables</h2>

<p>Create a <strong>.env</strong> file in the root directory:</p>

<pre>
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY

TAVILY_API_KEY=YOUR_TAVILY_API_KEY
</pre>

<hr>

<h2>Running the Application</h2>

<pre>
streamlit run streamlit_app.py
</pre>

<hr>

<h2>Sample Research Topics</h2>

<ul>
    <li>Analyze Electric Vehicle Market in India</li>
    <li>Future of Agentic AI in Healthcare</li>
    <li>Global Semiconductor Industry Outlook</li>
    <li>Impact of Generative AI on Customer Service</li>
    <li>Cloud Computing Market Trends 2030</li>
    <li>Indian FinTech Industry Analysis</li>
    <li>Future of Autonomous Vehicles</li>
</ul>

<hr>

<h2>Potential Future Enhancements</h2>

<ul>
    <li>LangGraph Workflow Integration</li>
    <li>Multi-Agent Orchestration</li>
    <li>Citation Agent</li>
    <li>Memory Layer</li>
    <li>Research Chat Interface</li>
    <li>Interactive Charts & Graphs</li>
    <li>DOCX Export</li>
    <li>PowerPoint Export</li>
    <li>RAG-based Knowledge Retrieval</li>
    <li>Research History Dashboard</li>
</ul>

<hr>

<h2>Learning Outcomes</h2>

<p>
This project demonstrates practical experience with:
</p>

<ul>
    <li>Agentic AI Systems</li>
    <li>Multi-Agent Workflows</li>
    <li>LLM Application Development</li>
    <li>Prompt Engineering</li>
    <li>Tool Calling</li>
    <li>Information Retrieval</li>
    <li>Fact Verification Pipelines</li>
    <li>Report Generation Systems</li>
    <li>Python Backend Development</li>
    <li>AI Product Engineering</li>
</ul>

<hr>

<h2>Author</h2>

<p>
<strong>Ayush Saxena</strong><br>
B.Tech Computer Science Engineering<br>
SRM Institute of Science and Technology (SRMIST)<br>
AI Engineering | Agentic AI | Generative AI
</p>

<hr>

<h2>License</h2>

<p>
This project is intended for educational, research, and portfolio purposes.
</p>

</body>
</html>
