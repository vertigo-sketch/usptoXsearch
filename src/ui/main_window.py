from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLineEdit, QComboBox, QPushButton, QScrollArea, 
    QLabel, QFrame, QMessageBox
)
from PySide6.QtCore import Qt, QObject, Signal, QThread
from src.utils.file_manager import FileManager
from src.ui.components.result_card import ResultCard

class DownloadWorker(QThread):
    """Dedicated thread for file downloads to prevent UI freezing."""
    finished = Signal(str, str)  # sub_dir, filename
    error = Signal(str)

    def __init__(self, filename: str, content: str, sub_dir: str):
        super().__init__()
        self.filename = filename
        self.content = content
        self.sub_dir = sub_dir

    def run(self):
        import time
        try:
            # Simulate network delay
            time.sleep(1) 
            fm = FileManager()
            fm.save_text_file(self.content, self.filename, self.sub_dir)
            self.finished.emit(self.sub_dir, self.filename)
        except Exception as e:
            self.error.emit(str(e))

class WorkerSignals(QObject):
    """Signals to communicate from the background thread to the GUI."""
    results_ready = Signal(list, str)
    error_occurred = Signal(str)
    loading_started = Signal()
    loading_finished = Signal()
    download_completed = Signal(str, str)
    download_error = Signal(str)

class MainWindow(QMainWindow):
    def __init__(self, manager):
        super().__init__()
        self.manager = manager
        self.file_manager = FileManager()
        self.setWindowTitle("usptoXsearch")
        self.resize(900, 700)

        # Signals for thread-safe communication
        self.signals = WorkerSignals()
        self.signals.results_ready.connect(self._on_results_received)
        self.signals.error_occurred.connect(self._on_error_received)
        self.signals.loading_started.connect(self._on_loading_started)
        self.signals.loading_finished.connect(self._on_loading_finished)
        self.signals.download_completed.connect(self._on_download_finished)
        self.signals.download_error.connect(self._on_error_received)

        # Main Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- Top Control Panel ---
        control_panel = QFrame()
        control_panel.setStyleSheet("background-color: #f8f9fa; border-bottom: 1px solid #dee2e6;")
        control_layout = QHBoxLayout(control_panel)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter search query...")
        self.search_input.returnPressed.connect(self._on_search)
        
        self.data_source_dropdown = QComboBox()
        self.data_source_dropdown.addItems([
            "Patent Search (PPUBS)",
            "Full Text Documents",
            "PDF Downloads",
            "Prosecution History (ODP)",
            "Patent Family Data",
            "Bulk Datasets (PatentsView)",
            "Trademark Search",
            "Trademark Status & Documents (TSDR)",
            "Trademark Assignments"
        ])

        self.search_button = QPushButton("Search")
        self.search_button.clicked.connect(self._on_search)
        self.search_button.setStyleSheet("padding: 5px 15px;")

        control_layout.addWidget(self.search_input, stretch=4)
        control_layout.addWidget(self.data_source_dropdown, stretch=2)
        control_layout.addWidget(self.search_button, stretch=0)

        main_layout.addWidget(control_panel)

        # --- Bottom Preview Panel ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("background-color: #ffffff; border: none;")
        
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.scroll_area.setWidget(self.results_container)

        main_layout.addWidget(self.scroll_area)

    def _on_search(self):
        query = self.search_input.text().strip()
        source = self.data_source_dropdown.currentText()
        
        if not query:
            return

        print(f"Searching for '{query}' in {source}")
        self._start_search_async(query, source)

    def _start_search_async(self, query: str, source: str):
        """Schedules the search task on the background loop."""
        from src.mcp_client.mapping import get_tool_info
        import asyncio

        self.signals.loading_started.emit()
        
        # We need to run this in a way that we can wait for it and handle results/errors
        async def search_task():
            try:
                # 1. Get tool info from mapping
                from src.mcp_client.mapping import DataSourceType
                try:
                    source_enum = DataSourceType(source)
                except ValueError:
                    self.signals.error_occurred.emit(f"Invalid data source: {source}")
                    return

                tool_info = get_tool_info(source_enum)
                if not tool_info:
                    self.signals.error_occurred.emit(f"No tool mapped for source: {source}")
                    return

                tool_name = tool_info["tool_name"]
                arg_names = tool_info.get("args", [])
                
                # Map the search input to the first expected argument name, if any
                if arg_names:
                    args = {arg_names[0]: query}
                else:
                    args = {"query": query}

                # 2. Call the MCP tool
                results = await self.manager.call_tool(tool_name, args)
                self.signals.results_ready.emit(results, source)
            except Exception as e:
                self.signals.error_occurred.emit(str(e))
            finally:
                self.signals.loading_finished.emit()

        # Schedule the coroutine in the manager's event loop
        future = self.manager.run_async(search_task())
        
        # We need to handle the completion of this future on the main thread 
        # to avoid blocking, but since we are using signals inside search_task,
        # it should be fine as long as we don't block here.
        # However, for robust error handling from the future itself:
        def check_future():
            try:
                future.result()
            except Exception as e:
                self.signals.error_occurred.emit(f"Task failed: {str(e)}")

        import threading
        threading.Thread(target=check_future, daemon=True).start()

    def _on_results_received(self, results: list, source: str):
        # Clear previous results
        while self.results_layout.count() > 0:
            item = self.results_layout.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        if not results:
            self._show_empty_state()
            return

        for result in results:
            # Assuming the tool returns a list of dicts where each dict has 'title' and 'description'
            # This depends on how MCP server returns data. 
            # For now, we try to extract it or use defaults.
            title = result.get("title", "No Title")
            desc = result.get("description", str(result)) # Fallback to string representation of the dict
            
            # In a real app, we'd pass the actual data source and filename/id to the card
            card = ResultCard(title, desc, source)
            if "Downloads" in source or "Documents" in source:
                card.show_download_button()
            
            card.download_requested.connect(self._on_result_download_requested)
            self.results_layout.addWidget(card)

    def _on_result_download_requested(self, data_source: str, title: str):
        """Handles the download request by using a DownloadWorker."""
        filename = f"{title.replace(' ', '_').lower()}.txt"
        content = f"Simulated content for {title} from source: {data_source}"
        
        self.worker = DownloadWorker(filename, content, data_source)
        self.worker.finished.connect(self._on_download_finished)
        self.worker.error.connect(self._on_download_failed)
        self.worker.start()

    def _on_download_finished(self, sub_dir: str, filename: str):
        QMessageBox.information(self, "Download Complete", f"Successfully downloaded file to {sub_dir}/{filename}")

    def _on_download_failed(self, error_msg: str):
        QMessageBox.critical(self, "Download Error", f"An error occurred during download:\n{error_msg}")

    def _on_error_received(self, error_msg: str):
        from PySide6.QtWidgets import QMessageBox
        QMessageBox.critical(self, "Error", f"An error occurred:\n{error_msg}")

    def _on_loading_started(self):
        self.search_button.setEnabled(False)
        self.search_input.setEnabled(False)
        self.data_source_dropdown.setEnabled(False)

    def _on_loading_finished(self):
        self.search_button.setEnabled(True)
        self.search_input.setEnabled(True)
        self.data_source_dropdown.setEnabled(True)

    def _show_empty_state(self):
        label = QLabel("No results found.")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: #7f8c8d; font-size: 14px;")
        self.results_layout.addWidget(label)