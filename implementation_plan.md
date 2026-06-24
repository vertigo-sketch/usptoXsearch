# Implementation Plan

[Overview]
Build a professional desktop interface for USPTO data access via the Patent MCP server.

The goal is to create `usptoXsearch`, a PySide6-based application that provides a unified GUI for searching patent and trademark datasets. The app will act as an MCP client, communicating with the `patent_mcp_server` to perform searches, retrieve full text, download PDFs, and access metadata (assignments, litigation, etc.). It will feature a responsive UI with real-time result previews and organized local file management for downloads.

[Types]
Define data structures for search results and MCP tool responses.

- `SearchResult`: A dictionary/dataclass containing `title`, `description`, and `source_type`.
- `MCPToolResponse`: Structured representation of the content returned by MCP tools (text, images, or file paths).
- `DataSourceType`: Enum representing supported sources: `PATENT_SEARCH`, `FULL_TEXT`, `PDF_DOWNLOAD`, `PROSECUTION_HISTORY`, `FAMILY_DATA`, `BULK_DATASETS`, `TRADEMARK_SEARCH`, `TRADEMARK_STATUS`, `TRADEMARK_ASSIGNMENTS`.

[Files]
Modify existing files and create new modules for core logic.

- **New Files:**
    - `src/mcp_client/config.py`: Configuration for MCP server command and arguments.
    - `src/ui/components/result_card.py`: Refactored `ResultCard` widget into its own file.
    - `src/utils/downloader.py`: Logic for handling asynchronous downloads and directory creation.
- **Modified Files:**
    - `src/main.py`: Update to use the correct MCP server command (via config) and handle graceful shutdown.
    - `src/mcp_client/mapping.py`: Expand mapping to include all required USPTO data sources.
    - `src/ui/main_window.py`: Refactor UI layout, implement threading for search/downloads, and connect signals.
    - `src/utils/file_manager.py`: Add support for organized directory creation under `/output/{source}/`.

[Functions]
Implement core logic for MCP communication and file I/O.

- **New Functions:**
    - `mcp_client.config.get_server_params()`: Returns the command and args for the USPTO server.
    - `utils.downloader.download_file(url, target_path)`: Asynchronous download function.
- **Modified Functions:**
    - `MainWindow._on_search()`: Updated to use the expanded mapping.
    - `MainWindow._start_search_async()`: Improved error handling and signal management.

[Classes]
Enhance existing classes for better modularity and responsiveness.

- **New Classes:**
    - `MCPConfig`: Manages server connection parameters.
    - `DownloadWorker(QThread)`: Dedicated thread for file downloads to prevent UI freezing.
- **Modified Classes:**
    - `MainWindow`: Refactored into a cleaner layout with dedicated component widgets.
    - `ResultCard`: Enhanced to support download triggers and better styling.

[Dependencies]
Add necessary libraries for GUI and MCP communication.

- `PySide6`: For the modern desktop interface.
- `mcp`: The Model Context Protocol client library.
- `uv`: Used for all dependency management (via `.python-version` and `pyproject.toml`).

[Testing]
Verify data accuracy and UI responsiveness.

- **Functional Testing:** Verify "Trademark Search" returns accurate results from the MCP server.
- **File I/O Testing:** Confirm files are saved to `/output/{source}/` correctly.
- **Concurrency Testing:** Ensure the GUI remains responsive during long-running searches or downloads.

[Implementation Order]
Execute changes in a logical sequence to ensure stability.

1. Update `src/mcp_client/config.py` and `mapping.py` with correct server parameters.
2. Implement `src/utils/downloader.py` and update `file_manager.py`.
3. Refactor `src/ui/main_window.py` to use the new components and threading logic.
4. Update `src/main.py` for proper lifecycle management of the MCP connection.
5. Perform final integration testing.