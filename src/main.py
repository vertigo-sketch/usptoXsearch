import sys
from PySide6.QtWidgets import QApplication, QMessageBox
from src.ui.main_window import MainWindow
from src.mcp_client.manager import MCPManager
from src.mcp_client.config import get_server_params

def main():
    app = QApplication(sys.argv)
    
    # Get server configuration from the config module
    command, args = get_server_params()

    manager = MCPManager(command, args)
    
    window = MainWindow(manager)
    window.show()
    
    try:
        app.exec()
    finally:
        # We need a way to gracefully disconnect the manager when the app exits.
        # Since we are in a separate thread, we'll use run_async for the disconnect.
        import asyncio
        asyncio.run(manager.disconnect())

if __name__ == "__main__":
    main()