import { opticParseScrapeAction } from './actions/scrape';

export const opticParsePlugin = {
  name: 'opticparse',
  description: 'Autonomous Vision AI Web Scraper & x402 Crypto Paywall Integration for ElizaOS Agents',
  actions: [opticParseScrapeAction],
  evaluators: [],
  providers: []
};

export default opticParsePlugin;
