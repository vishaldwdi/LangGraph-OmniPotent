"""Code checking functionality for the engineering agent.

This module provides utilities for extracting and validating Python code
from markdown-formatted text, as well as checking code for errors.
"""

import re

from engineer_agent.state import AgentState


def extract_python_code(text: str) -> str:
    """Extract Python code from markdown-formatted text.

    Args:
        text: Input text containing markdown code blocks

    Returns:
        Extracted Python code as a string
    """
    pattern = r"```python\s*(.*?)\s*(```|$)"
    matches = re.findall(pattern, text, re.DOTALL)
    return matches


error_parsing = """Make sure your response contains a code block in the following format:

```python
...
```

When trying to parse out that code block, got this error: {error}"""


def check(state: AgentState) -> AgentState:
    """Check the generated code for errors and validity.

    Args:
        state: Current agent state containing messages and context

    Returns:
        Updated agent state with check results
    """
    last_answer = state["messages"][-1]
    try:
        code_blocks = extract_python_code(last_answer.content)
    except Exception as e:
        return {
            "messages": [
                {"role": "user", "content": error_parsing.format(error=str(e))}
            ]
        }
    if len(code_blocks) == 0:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": error_parsing.format(error="Did not find a code block!"),
                }
            ]
        }
    if len(code_blocks) > 1:
        return {
            "messages": [
                {
                    "role": "user",
                    "content": error_parsing.format(
                        error="Found multiple code blocks!"
                    ),
                }
            ]
        }
    return {"code": f"```python\n{code_blocks[0][0]}\n```"}
