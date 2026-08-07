# Scraping Dynamic Web Pages Without Selectors Using AI Vision (TypeScript/JavaScript Tutorial)

Web scraping has traditionally been a game of cat-and-mouse. You spend hours writing fine-tuned CSS selectors or XPath paths, only for the website to change its layout or class names (especially on modern frameworks with generated CSS class names like `css-1ux802d`), breaking your entire data pipeline overnight.

In this tutorial, we will learn how to build a **selector-free scraper** using **Opticparse**, an AI-powered scraping tool that captures webpage screenshots and uses Gemini's multimodal vision intelligence to extract structured JSON data.

We will use the official **Opticparse JavaScript/TypeScript SDK** to extract data in less than 10 lines of code.

---

## The Concept: AI Vision Scraping
Instead of parsing HTML source code directly, Opticparse:
1. Launches a headless Chromium instance using Playwright.
2. Navigates to the target page and takes a full-page snapshot.
3. Passes the screenshot to an AI Vision Agent (Gemini) along with a text prompt.
4. Returns clean, parsed JSON matching your description.

Because it mimics how a real human looks at the page, it does not care about dynamic CSS class name changes, shadow DOMs, or obfuscated HTML.

---

## Setup & Installation

Install the official client library:

```bash
npm install opticparse-js
```

### Get Your API Key
You can get an API key in two ways:
1. **RapidAPI Hub**: Access the API globally on [RapidAPI's Opticparse Listing](https://rapidapi.com/parastejpal987cmyk/api/opticparse-ai-vision-web-scraper). Subscribe to the Free basic tier to get a RapidAPI Key.
2. **Private Host**: If you hosted the Docker microservice container yourself (e.g. on Render), use your private `OPTICPARSE_API_KEY`.

---

## Code Example: Scraping Hacker News

Let's say we want to scrape the top 5 articles, their link URLs, and score points from the homepage of Hacker News.

Here is how you do it:

```typescript
import { OpticparseClient } from 'opticparse-js';

// Initialize the client. 
// If using the RapidAPI marketplace, set useRapidApi: true
const client = new OpticparseClient({
  apiKey: 'YOUR_RAPIDAPI_KEY_HERE',
  useRapidApi: true
});

async function runScrape() {
  console.log('Scraping Hacker News articles...');
  
  try {
    const data = await client.scrape({
      targetUrl: 'https://news.ycombinator.com',
      extractionQuery: 'Extract the top 5 article titles, their link URLs, and score points as a JSON list of objects.',
      viewportWidth: 1280,
      viewportHeight: 1000
    });

    console.log('Scraped Data Output:');
    console.log(JSON.stringify(data, null, 2));

  } catch (error) {
    console.error('Scraping failed:', error);
  }
}

runScrape();
```

### Sample Output
The client will automatically handle the asynchronous execution, image loading, and return a clean, fully-typed JSON structure:

```json
[
  {
    "title": "Why I still use Vim",
    "url": "https://example.com/vim",
    "points": 142
  },
  {
    "title": "Show HN: Opticparse - AI Visual Scraper",
    "url": "https://github.com/parastejpal987-cmyk/opticparse",
    "points": 98
  }
]
```

---

## Advanced Options

The SDK client supports configuring the browser environment to handle dynamic loading states:

```typescript
const result = await client.scrape({
  targetUrl: 'https://example.com',
  extractionQuery: 'Extract details...',
  
  // Custom screen sizes for responsive layouts
  viewportWidth: 1920,
  viewportHeight: 1080,
  
  // Wait until page is completely loaded ('networkidle' | 'load' | 'domcontentloaded')
  waitUntil: 'networkidle',
  
  // Adjust timeout threshold (in milliseconds) for slower connections
  timeout: 45000 
});
```

---

## Running from the Command Line (CLI)

The package also includes a built-in CLI tool to inspect scraping outputs from your terminal before writing any code.

```bash
# Run a test query via RapidAPI
npx opticparse scrape \
  --url "https://example.com" \
  --query "Extract the page header text" \
  --key "YOUR_RAPIDAPI_KEY" \
  --rapidapi
```

---

## Conclusion
Visual AI web scraping solves the biggest bottleneck in data harvesting: code maintenance. Try integrating **Opticparse** in your next project to build reliable, self-healing scraping workflows.

* Check out the [RapidAPI Listing](https://rapidapi.com/parastejpal987cmyk/api/opticparse-ai-vision-web-scraper) to get started for free.
* Give feedback and read more options on the [NPM package repository](https://www.npmjs.com/package/opticparse-js).
