# AI-Powered Web Search Engine

A decoupled, production-ready, full-stack search engine built with **Python**, **Flask**, **Streamlit**, and the **Exa API**. This application features real-time web retrieval, regex term highlighting, multi-criteria filtering, and an intelligent **SQLite** caching layer designed to minimize latency and optimize API overhead.

---

## 🏗️ Architecture & Overview

The project is structured into a clean **two-tier architecture**:

1. **Flask REST API (`app.py` & `processor.py`)**: Handles core business logic, input validation, Exa API communication, regex term highlighting, and SQLite cache persistence.
2. **Streamlit Frontend (`main.py`)**: Serves as a lightweight presentation client that maintains UI session state, captures user queries and filters, and renders interactive output cards.

```
┌─────────────────────────────────┐
│       Streamlit Client          │
│           (main.py)             │
└────────────────┬────────────────┘
                 │  HTTP POST /api/search
                 ▼
┌─────────────────────────────────┐
│        Flask REST API           │
│            (app.py)             │
└────────────────┬────────────────┘
                 │
                 ▼
┌─────────────────────────────────┐      Read/Write      ┌──────────────────┐
│      Engine & Processor         ├─────────────────────►│  SQLite Cache    │
│         (processor.py)          │                      │    (cache.db)    │
└────────────────┬────────────────┘                      └──────────────────┘
                 │
                 │  External Search Request
                 ▼
┌─────────────────────────────────┐
│             Exa API             │
└─────────────────────────────────┘
```

---

## 🚀 Key Features

- **Decoupled Architecture:** Clean boundary between backend REST API endpoints and frontend UI presentation.
- **Composite Key SQLite Caching:** Caches search results based on a deterministic JSON key combining query string, category, domains, and publication date bounds.
- **Regex Match Highlighting:** Automatically bolds search terms within summary extracts using case-insensitive regular expressions (`re`).
- **Granular Search Filters:** Comprehensive support for categories, domain inclusions/exclusions, and publication date ranges.
- **Session State Management:** Persists active results in Streamlit session state across page interactions and re-renders.

---

## 🗄️ Caching Mechanism

To avoid redundant API queries and cut response times for recurring searches, `processor.py` constructs a unique composite key for every query-filter combination:

```json
{
  "query": "quantum computing",
  "category": "research paper",
  "include_domains": ["arxiv.org", "github.com"],
  "exclude_domains": null,
  "start_published_date": "2024-01-01T00:00:00.000Z",
  "end_published_date": "2026-12-31T23:59:59.999Z"
}
```

The key is serialized into `cache.db` under the `search_cache` table:

```sql
CREATE TABLE IF NOT EXISTS search_cache (
    cache_key TEXT PRIMARY KEY,
    response TEXT
);
```

---

## 🔌 API Reference

### `POST /api/search`

Executes a web search with optional filtering criteria.

#### Request Headers
```http
Content-Type: application/json
```

#### Request Body Schema
| Parameter | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `query` | `string` | **Yes** | The core search string. |
| `category` | `string` | No | Category filter (`"company"`, `"research paper"`, `"news"`, `"github"`, `"tweet"`). |
| `include_domains` | `array[string]` | No | List of target domains to restrict search results to. |
| `exclude_domains` | `array[string]` | No | List of domains to exclude from search results. |
| `start_published_date` | `string` | No | ISO 8601 timestamp string for publication lower bound (e.g., `"2024-01-01T00:00:00.000Z"`). |
| `end_published_date` | `string` | No | ISO 8601 timestamp string for publication upper bound (e.g., `"2026-12-31T23:59:59.999Z"`). |

#### Sample Request
```json
{
  "query": "deep learning architectures",
  "category": "research paper",
  "include_domains": ["arxiv.org"],
  "start_published_date": "2024-01-01T00:00:00.000Z",
  "end_published_date": "2026-12-31T23:59:59.999Z"
}
```

#### Sample Success Response (`200 OK`)
```json
{
  "status": "success",
  "results": {
    "source": "exa_api",
    "data": [
      {
        "title": "Attention Is All You Need",
        "url": "https://arxiv.org/abs/1706.03762",
        "summary": "An overview of transformer **deep learning architectures**...",
        "published_date": "2024-02-15T08:00:00.000Z"
      }
    ]
  }
}
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python 3.10+**
- An active **Exa API Key**

### 1. Clone & Set Up Virtual Environment
```bash
git clone https://github.com/YOUR_USERNAME/python-ai-search.git
cd python-ai-search

python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install flask streamlit exa-py python-dotenv requests
```

### 3. Environment Variables
Create a `.env` file in the root directory:
```env
API_KEY=your_exa_api_key_here
```

---

## 🏃 Running the Application

Launch the Flask backend and Streamlit frontend in separate terminal windows:

### Terminal 1: Start Flask REST API Backend
```bash
python app.py
```
*Server runs on `http://localhost:5000`*

### Terminal 2: Start Streamlit Frontend Client
```bash
streamlit run main.py
```
*UI launches automatically at `http://localhost:8501`*
