from enum import Enum
from typing import Any, Dict, List, Optional

class DataSourceType(Enum):
    PATENT_SEARCH = "Patent Search (PPUBS)"
    FULL_TEXT = "Full Text Documents"
    PDF_DOWNLOAD = "PDF Downloads"
    PROSECUTION_HISTORY = "Prosecution History (ODP)"
    FAMILY_DATA = "Patent Family Data"
    BULK_DATASETS = "Bulk Datasets (PatentsView)"
    TRADEMARK_SEARCH = "Trademark Search"
    TRADEMARK_STATUS = "Trademark Status & Documents (TSDR)"
    TRADEMARK_ASSIGNMENTS = "Trademark Assignments"

# Mapping of DataSourceType to MCP tool names and their expected arguments structure.
DATA_SOURCE_MAPPING: Dict[DataSourceType, Dict[str, Any]] = {
    DataSourceType.PATENT_SEARCH: {
        "tool_name": "search_patents",
        "args": ["query"]
    },
    DataSourceType.FULL_TEXT: {
        "tool_name": "get_full_text",
        "args": ["patent_number"]
    },
    DataSourceType.PDF_DOWNLOAD: {
        "tool_name": "download_pdf",
        "args": ["patent_number"]
    },
    DataSourceType.PROSECUTION_HISTORY: {
        "tool_name": "get_prosecution_history",
        "args": []
    },
    DataSourceType.FAMILY_DATA: {
        "tool_name": "get_patent_family",
        "args": ["patent_number"]
    },
    DataSourceType.BULK_DATASETS: {
        "tool_name": "search_patentsview",
        "args": []
    },
    DataSourceType.TRADEMARK_SEARCH: {
        "tool_name": "search_trademarks",
        "args": ["mark_text"]
    },
    DataSourceType.TRADEMARK_STATUS: {
        "tool_name": "get_trademark_status",
        "args": ["trademark_id"]
    },
    DataSourceType.TRADEMARK_ASSIGNMENTS: {
        "tool_name": "search_assignments",
        "args": []
    }
}

def get_tool_info(source_type: DataSourceType) -> Optional[Dict[str, Any]]:
    return DATA_SOURCE_MAPPING.get(source_type)
