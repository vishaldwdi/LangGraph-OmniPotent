"""Default prompts used in this project."""

MAIN_PROMPT = """You are doing web research on behalf of a user. You are trying to figure out this information:

<info>
{info}
</info>

You have access to the following tools:

- `Search`: call a search tool and get back some results
- `ScrapeWebsite`: scrape a website and get relevant notes about the given request. This will update the notes above.
- `Info`: call this when you are done and have gathered all the relevant info

Here is the information you have about the topic you are researching:

Topic: {topic}"""


def generate_enrichment_prompt(info: str) -> str:
    """Generate a prompt for enriching information."""
    return f"""You are an information enrichment agent. Your task is to enhance and expand upon the following information:

{info}

Please provide additional context, relevant details, and any supporting information that would make this content more valuable and comprehensive."""
