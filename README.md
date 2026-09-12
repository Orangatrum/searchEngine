# AI-Powered Web Search Engine

A full-stack, AI-powered search engine built with **Python**, **Streamlit**, and the **Exa API**. This application features real-time web retrieval, intelligent search caching backed by **SQLite**, regex-based term highlighting, and session-state management for optimal response latency.

---

## 🏗️ Architecture & Features

- **Frontend Interface:** Interactive UI built using **Streamlit**, providing low-latency search results and dynamic filters.
- **Search & Retrieval Engine:** Integrated with the **Exa API** for neural/semantic and keyword web search.
- **Caching Layer:** Built-in **SQLite** database caching mechanism to prevent redundant API calls, speed up recurring queries, and optimize cost.
- **Text Highlighting:** Custom regex parsing to extract and highlight key query terms within snippet previews.
- **State Management:** Utilizes Streamlit session state to manage user queries, pagination, and application settings cleanly without losing application context across renders.

---

## 🚀 Tech Stack

- **Language:** Python 3.10+
- **Framework:** Streamlit
- **Database:** SQLite3
- **External API:** Exa API (`exa-py`)
- **Key Libraries:** `re` (Regex), `requests` / `httpx`

---

## 🛠️ Getting Started

### Prerequisites

- **Python 3.10** or higher
- An active **Exa API key**

### Installation & Setup

git clone [https://github.com/YOUR_USERNAME/python-ai-search.git](https://github.com/YOUR_USERNAME/python-ai-search.git)
cd python-ai-search

python -m venv venv
# On Windows:
venv\\Scripts\\activate
# On macOS/Linux:
source venv/bin/activate
