import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig
from crawl4ai.content_filter_strategy import PruningContentFilter
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

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
        markdown_generator=md_generator,
    )
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun("https://www.greatwaysinc.com/", config=config)
        print(result.markdown.fit_markdown)

if __name__ == "__main__":
    asyncio.run(main())
