import { opticParseScrapeAction, phishVisionGuardAction } from './actions/scrape';

export const opticParsePlugin = {
  name: 'opticparse',
  description: 'Autonomous Vision AI Web Scraper, PhishVision Pre-Flight Security Guard & x402 Crypto Paywall Integration for ElizaOS Agents',
  actions: [opticParseScrapeAction, phishVisionGuardAction],
  evaluators: [],
  providers: []
};

export default opticParsePlugin;
export { opticParseScrapeAction, phishVisionGuardAction };
