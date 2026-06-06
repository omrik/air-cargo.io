import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'air-cargo.io',
  description: 'Air cargo tracking API — developer portal, SDKs, and integration guides',
  base: '/air-cargo.io/',
  cleanUrls: true,
  head: [
    ['link', { rel: 'icon', href: '/air-cargo.io/favicon.svg', type: 'image/svg+xml' }],
  ],
  themeConfig: {
    logo: '/air-cargo-logo.svg',
    siteTitle: 'air-cargo.io',
    search: { provider: 'local' },
    socialLinks: [
      { icon: 'github', link: 'https://github.com/omrik/air-cargo.io' },
    ],
    nav: [
      { text: 'Guide', link: '/guide/quickstart', activeMatch: '/guide/' },
      { text: 'API', link: '/api/openapi', activeMatch: '/api/' },
      { text: 'SDKs', link: '/sdks/python', activeMatch: '/sdks/' },
      { text: 'Integrations', link: '/integrations/slack', activeMatch: '/integrations/' },
    ],
    sidebar: {
      '/guide/': [
        { text: 'Quickstart', link: '/guide/quickstart' },
        { text: 'Authentication', link: '/guide/authentication' },
        { text: 'Shipments', link: '/guide/shipments' },
        { text: 'Tracking', link: '/guide/tracking' },
        { text: 'Webhooks', link: '/guide/webhooks' },
        { text: 'Rate Limiting', link: '/guide/rate-limiting' },
        { text: 'Errors', link: '/guide/errors' },
      ],
      '/sdks/': [
        { text: 'Python SDK', link: '/sdks/python' },
      ],
      '/integrations/': [
        { text: 'Slack', link: '/integrations/slack' },
        { text: 'n8n', link: '/integrations/n8n' },
        { text: 'Make', link: '/integrations/make' },
        { text: 'Zapier', link: '/integrations/zapier' },
      ],
    },
    footer: {
      message: 'Built for air cargo logistics.',
      copyright: '© air-cargo.io',
    },
  },
})
