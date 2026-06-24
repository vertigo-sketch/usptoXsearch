# Changelog

All notable changes to this project will be documented in this file.

## [0.1.0] - 2026-06-23

### Added
- **Core Application Structure**: Implemented the main application entry point and lifecycle management in `src/main.py`.
- **MCP Client Integration**:
    - Created `src/mcp_client/config.py` for server configuration.
    - Implemented `src/mcp_client/mapping.py` with a robust `DataSourceType` Enum and tool mapping for USPTO data sources.
    - Integrated MCP client logic to communicate with the Patent MCP Server.
- **User Interface (PySide6)**:
    - Developed a modern desktop interface in `src/ui/main_window.py`.
    - Implemented a modular UI component architecture, including `ResultCard` for displaying search results.
    - Added real-time loading indicators and error dialogs.
- **Asynchronous Processing**:
    - Implemented `DownloadWorker(QThread)` to handle file downloads without blocking the main GUI thread.
    - Integrated asynchronous searching using background threads/tasks to maintain UI responsiveness.
- **File & Data Management**:
    - Created `src/utils/downloader.py` for asynchronous HTTP downloads of patent documents and text.
    - Enhanced `src/utils/file_manager.py` with organized directory management (`/output/{source}/`) and file listing capabilities.
- **Documentation**:
    - Added comprehensive `README.md` detailing features, installation, architecture, and supported data sources.

### Changed
- Refactored UI components for better modularity (extraction of `ResultCard`).
- Improved error handling in the search and download workflows.