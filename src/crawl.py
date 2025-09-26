import os
import json
import asyncio
from typing import Dict
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, LLMConfig, CacheMode
from crawl4ai import LLMExtractionStrategy

load_dotenv()

class FAQ(BaseModel):
    faq_question: str = Field(..., description="Frequently Asked Questions in the webpage")
    faq_answer: str = Field(..., description="Answers for the above Freaquently Asked Question")

async def extract_structured_data_using_llm(
    provider: str, api_token: str = None, extra_headers: Dict[str, str] = None
):
    print(f"\n--- Extracting Structured Data with {provider} ---")

    if api_token is None and provider != "ollama":
        print(f"API token is required for {provider}. Skipping this example.")
        return

    browser_config = BrowserConfig(headless=True)

    extra_args = {"temperature": 0, "top_p": 0.9, "max_tokens": 2000}
    if extra_headers:
        extra_args["extra_headers"] = extra_headers

    crawler_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS,
        word_count_threshold=1,
        page_timeout=80000,
        extraction_strategy=LLMExtractionStrategy(
            llm_config = LLMConfig(provider=provider,api_token=api_token),
            schema=OpenAIModelFee.model_json_schema(),
            extraction_type="schema",
            instruction="""From the crawled content, populate the Frequently Asked Questions and Answers in the list of shared format""",
            extra_args=extra_args,
        ),
    )

    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(
            url="https://www.greatwaysinc.com/faq-details_faq_19", config=crawler_config
        )
        print(result.extracted_content)

if __name__ == "__main__":

    asyncio.run(
        extract_structured_data_using_llm(
            provider="openai/gpt-4o", api_token=os.getenv("OPENAI_API_KEY")
        )
    )

