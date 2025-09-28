import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    ContentTypeFilter
)

async def main():

    prune_filter = PruningContentFilter(
        threshold=0.5,
        threshold_type="dynamic",
        # min_word_threshold=10
    )

    md_generator = DefaultMarkdownGenerator(
        content_filter=prune_filter,
        options={
            "ignore_links": True,
            "ignore_images": True,
            "escape_html": False,
        }
    )
    config = CrawlerRunConfig(
        deep_crawl_strategy=BFSDeepCrawlStrategy(
            max_depth=5, 
            include_external=False,
            max_pages=50,
            filter_chain=FilterChain([ContentTypeFilter(allowed_types=["text/html"])])
        ),
        markdown_generator=md_generator,
        scraping_strategy=LXMLWebScrapingStrategy(),
        exclude_all_images=True,
        # verbose=True,
        stream=True,
    )
    async with AsyncWebCrawler() as crawler:
        with open("./references/result.md", "a") as file:
            async for result in await crawler.arun("https://www.greatwaysinc.com/", config=config):
                file.write(f"\n\n# URL: {result.url}\n")
                file.write(result.markdown.fit_markdown)


if __name__ == "__main__":
    asyncio.run(main())
