# usptoXsearch

A professional desktop application for accessing and searching USPTO (United States Patent and Trademark Office) data via a Model Context Protocol (MCP) server. Built with Python, PySide6, and the MCP protocol.

## 🚀 Features

- **Unified Search Interface**: A modern GUI to search across multiple patent and trademark datasets.
- **Real-time Previews**: View search results in organized cards within the application.
- **Asynchronous Operations**: All heavy tasks (searching and downloading) are handled in background threads, ensuring a responsive UI.
- **Organized File Management**: Automatically downloads and organizes files into structured directories: `/output/{source_name}/`.
- **MCP Integration**: Acts as an MCP client to communicate seamlessly with the `patent_mcp_server`.

## 🛠️ Supported Data Sources

The application supports a wide range of USPTO data sources via the MCP server, including:
- Patent Search (PPUBS)
- Full Text Documents
- PDF Downloads
- Prosecution History (ODP)
- Patent Family Data
- Bulk Datasets (PatentsView)
- Trademark Search
- Trademark Status & Documents (TSDR)
- Trademark Assignments

## 📦 Prerequisites

- Python 3.12+
- `uv` (recommended for dependency management)
- An active MCP server providing USPTO patent/trademark tools.

## 🚀 Installation & Setup

### Using `uv` (Recommended)
```bash
# Clone the repository
git clone <repository_url>
cd usptoXsearch

# Install dependencies using uv
uv sync

# Run the application
uv run python src/main.py
```

### Using `pip`
```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt  # If available, otherwise use pyproject.toml info

# Run the application
python src/main.py
```

## 🏗️ Architecture

- **Frontend**: PySide6 (Qt for Python) providing a responsive desktop interface.
- **Backend Logic**: Asynchronous workers (`QThread`) for non-blocking I/O operations.
- **MCP Client**: Implements the Model Context Protocol to interact with external tools and data sources.
- **File Management**: Structured local storage management for downloaded patent documents and metadata.

## 📄 License

This project is licensed under the terms specified in the `LICENSE` file (if provided).