# Crawl4AI:
Tool to scrape website and create mardown file from that. It's highly customizable through various parameters
> [!IMPORTANT]
> Crawl4AI has less modules all the core functionalities can be performed using those limited modules
# Important modules:
1. AsyncWebCrawler
2. CrawlerRunConfig
3. BrowserConfig
4. DefaultMarkdownGenerator
5. JsonCssExtractionStrategy
6. Deep Crawling Strategies
## AsyncWebCrawler:
- AsyncWebCrawler is a core class in the Crawl4AI
- All crawls are performed using this class
- It's an asynchronous context manager, which consist of __aenter__ and __aexit__ methods, which takes care of the creation and closing of resource. We can just use it as **async with**
- The constructor takes **BrowserConfig** to configure how the browser should be launched
- `arun()` - method take in URL to crawl and also takes **CrawlerRunConfig** run configurations
- `arun_many()` - method used when multiple URLs should be crawled, this uses concurreny to crawl multiple urls [docs](https://docs.crawl4ai.com/advanced/multi-url-crawling/)
- [refer to docs](https://docs.crawl4ai.com/api/async-webcrawler/)
```python
import asyncio
from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode

async def main():
    browser_conf = BrowserConfig(headless=True)  # or False to see the browser
    run_conf = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS
    )

    async with AsyncWebCrawler(config=browser_conf) as crawler:
        result = await crawler.arun( # Use arun_many when multiple URLs need to be crawled, takes list of URLs
            url="https://example.com",
            config=run_conf
        )
        print(result.markdown)

if __name__ == "__main__":
    asyncio.run(main())
```

## CrawlerRunConfig:
- This is the main data class which is used to configure the crawl run.
- Which has configurable arguments
- We can configure `extraction_strategy`, `word_count_threshold`, `css_selector` etc..
- [refer to docs](https://docs.crawl4ai.com/api/parameters/#2-crawlerrunconfig-controlling-each-crawl)
```python
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig

run_cfg = CrawlerRunConfig(
    wait_for="css:.main-content",
    word_count_threshold=15,
    excluded_tags=["nav", "footer"],
    exclude_external_links=True,
    stream=True,  # Enable streaming for arun_many()
)
```
## BrowserConfig:
- Data class that can be used to configure how the web browsers should behave when we launch the crawl
```python
from crawl4ai import AsyncWebCrawler, BrowserConfig

browser_cfg = BrowserConfig(
    browser_type="chromium",
    headless=True,
    viewport_width=1280,
    viewport_height=720,
    proxy="http://user:pass@proxy:8080",
    user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/116.0.0.0 Safari/537.36",
)
```
## DefaultMarkdownGenerator:
- This class is configured in order to filter output markdown
- `PruningContentFilter` - Performs filter based score, this score is calculated on how the words, links are within each topic in the markdown
```python
prune_filter = PruningContentFilter(
        # Lower → more content retained, higher → more content pruned
        threshold=0.45,           
        # "fixed" or "dynamic"
        threshold_type="dynamic",  
        # Ignore nodes with <5 words
        min_word_threshold=5      
    )
``` 
- `BM25ContentFilter` - Perform filtering based on the user_query, filters only texts that matches the user query based on the statistical property of text instead of vector similarity.
```python
bm25_filter = BM25ContentFilter(
        user_query="startup fundraising tips",
        # Adjust for stricter or looser results
        bm25_threshold=1.2  
    )
```
- also has a way to configure what should appear in the output markdown and what should not
```python
options={
            "ignore_links": True,
            "ignore_images": True,
            "escape_html": False,
        }
```
- filtered markdown can be accessed via `result.markdown.fit_markdown`. Normal `result.markdown` gives unfiltered markdown.
- [refer to docs](https://docs.crawl4ai.com/core/markdown-generation/)
## JsonCssExtractionStrategy:
- Can define schema what all need to be extracted from the html under schema to extract only those specific data
```python
schema = {
        "name": "Crypto Prices",
        "baseSelector": "div.crypto-row",    # Repeated elements
        "fields": [
            {
                "name": "coin_name",
                "selector": "h2.coin-name",
                "type": "text"
            },
            {
                "name": "price",
                "selector": "span.coin-price",
                "type": "text"
            }
        ]
    }

    # 2. Create the extraction strategy
    extraction_strategy = JsonCssExtractionStrategy(schema, verbose=True)

    # 3. Set up your crawler config (if needed)
    config = CrawlerRunConfig(
        # e.g., pass js_code or wait_for if the page is dynamic
        # wait_for="css:.crypto-row:nth-child(20)"
        cache_mode = CacheMode.BYPASS,
        extraction_strategy=extraction_strategy,
    )
```
- Even LLM can be used be used to define JSON Schema as well as can be used to generate content to populate the JSON Schema [refer](https://docs.crawl4ai.com/extraction/llm-strategies/)
- [refer to docs](https://docs.crawl4ai.com/extraction/no-llm-strategies/)

## Deep Crawling Strategies:
- Below classes are used to perform deep crawl, like we can provide the home page url, this will crawl the home page and find all the links and crawl even all the nested URLs. This deep can be configured by parameters
- `BFSDeepCrawlStrategy`, `DFSDeepCrawlStrategy`, and `BestFirstCrawlingStrategy` - This all used for deep crawling
- [refer to docs](https://docs.crawl4ai.com/core/deep-crawling/)

## Important features:
1. Basic Crawl (URL) - Crawls the provided URL and converts the HTML to markdown
2. Deep crawl - Can start with provided URL, finds other links (both internal and external) and crawls that links as well
3. Multiple URL crawl (Concurrency) - Provide list of URLs and will crawl all the links in the list
4. Markdown filters - Can filter various fields at the finally generated markdown (Can be accessed via `result.markdown.fit_markdown`)
5. JSON Schema based extraction - Can provide the Schema and extract based on that schema
6. LLM Based extraction - LLM can be used to define schema, and LLM can be used for extraction

