import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.deep_crawling import BFSDeepCrawlStrategy
from crawl4ai.content_scraping_strategy import LXMLWebScrapingStrategy
from crawl4ai.deep_crawling.filters import (
    FilterChain,
    ContentTypeFilter
)

async def main():
    
    prune_filter = PruningContentFilter(
        threshold=0.5,
        threshold_type="dynamic",
        min_word_threshold=50
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
        async for result in await crawler.arun("https://www.greatwaysinc.com/", config=config):

            print(f"URL: {result.url}")
            print(f"Depth: {result.metadata.get('depth', 0)}")
            if not result.success:
                print("Crawl error:", result.error_message)

if __name__ == "__main__":
    asyncio.run(main())
