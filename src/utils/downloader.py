import httpx
from typing import Union


async def download_bytes(url: str) -> bytes:
    """
    Asynchronously downloads a file from the given URL and returns its content as bytes.

    Args:
        url: The URL of the file to download.

    Returns:
        bytes: The content of the downloaded file.

    Raises:
        httpx.HTTPStatusError: If the HTTP request returned an error status code.
        httpx.RequestError: If there was an error while making the request.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.content


async def download_text(url: str) -> str:
    """
    Asynchronously downloads text content from the given URL and returns it as a string.

    Args:
        url: The URL of the text to download.

    Returns:
        str: The downloaded text content.

    Raises:
        httpx.HTTPStatusError: If the HTTP request returned an error status code.
        httpx.RequestError: If there was an error while making the request.
    """
    async with httpx.AsyncClient(follow_redirects=True) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text