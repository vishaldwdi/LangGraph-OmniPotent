import requests
from langchain.tools import BaseTool


def load_github_file(url: str) -> str:
    """Load a file from GitHub raw content."""
    try:
        raw_url = url.replace("github.com", "raw.githubusercontent.com").replace(
            "/blob/", "/"
        )
        response = requests.get(raw_url)
        response.raise_for_status()
        return response.text
    except Exception as e:
        return f"Error loading GitHub file: {str(e)}"


class LoadLocalFileTool(BaseTool):
    """Tool for loading local files."""

    name = "load_local_file"
    description = (
        "Useful for when you need to load a local file to understand its content"
    )

    def _run(self, file_path: str) -> str:
        """Load and return the contents of a local file."""
        try:
            with open(file_path) as file:
                return file.read()
        except Exception as e:
            return f"Error loading file: {str(e)}"

    async def _arun(self, file_path: str) -> str:
        """Async version of file loading."""
        return self._run(file_path)
