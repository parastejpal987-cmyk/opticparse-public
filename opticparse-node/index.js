const axios = require('axios');

class OpticParse {
  /**
   * Initialize the OpticParse Node SDK
   * @param {string} apiKey - Your OpticParse API Key
   * @param {string} [baseURL] - Optional base URL if self-hosting
   */
  constructor(apiKey, baseURL = 'https://api.opticparse.com') {
    if (!apiKey) {
      throw new Error('OpticParse API Key is required');
    }
    
    this.client = axios.create({
      baseURL,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      }
    });
  }

  /**
   * Scrape and extract structured data from a URL using Vision AI
   * @param {Object} params - The scraping parameters
   * @param {string} params.target_url - The URL to scrape
   * @param {string} params.extraction_query - The natural language query of what to extract
   * @param {Object} [params.response_schema] - Optional JSON schema to enforce the output format
   * @param {boolean} [params.vision_mode=true] - Use computer vision to read the screen (default: true)
   * @returns {Promise<Object>} The extracted JSON data
   */
  async extract({ target_url, extraction_query, response_schema = null, vision_mode = true, ...rest }) {
    try {
      const response = await this.client.post('/api/vision-scrape', {
        target_url,
        extraction_query,
        response_schema,
        vision_mode,
        ...rest
      });
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  /**
   * Submit an asynchronous heavy scraping job to Cloudflare Queues
   * @param {Object} params - The scraping parameters (same as extract)
   * @returns {Promise<Object>} The queued job ID and status URL
   */
  async extractAsync(params) {
    try {
      const response = await this.client.post('/v2/scrape_async', params);
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  /**
   * Check a URL for phishing and malicious threats using PhishVision
   * @param {string} url - The URL to scan
   * @returns {Promise<Object>} The threat analysis report
   */
  async scanThreat(url) {
    try {
      const response = await this.client.post('/api/scan', { url });
      return response.data;
    } catch (error) {
      this._handleError(error);
    }
  }

  _handleError(error) {
    if (error.response) {
      throw new Error(`OpticParse API Error [${error.response.status}]: ${JSON.stringify(error.response.data)}`);
    } else if (error.request) {
      throw new Error('OpticParse API Error: No response received from server');
    } else {
      throw new Error(`OpticParse SDK Error: ${error.message}`);
    }
  }
}

module.exports = OpticParse;
