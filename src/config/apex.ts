/**
 * APEX MASTER CONFIGURATION (MAXIMUM COVERAGE)
 * ==========================================================
 * Strategy: "Zero-Server" Architecture
 * Hosting: Static (Cloudflare Pages / GitHub Pages / Vercel)
 * Backend: Firebase + Client-Side APIs
 * Monetization: AdSense (Primary) + Non-Intrusive Backups
 * Analytics: 8-Layer Redundancy
 * ==========================================================
 */

export const APEX_CONFIG = {
  // ========================================================================
  // 1. MONETIZATION STACK (The Revenue Engine)
  // Strategy: AdSense primary, non-intrusive backups only
  // ========================================================================
  monetization: {
    // [PRIMARY] Google AdSense
    adsense: {
      publisherId: 'ca-pub-XXXXXXXXXXXXXXXX',
      autoAds: true,
      lazyLoad: true,
      enabled: true,
    },

    // [BACKUP] A-ADS (Anonymous Ads) - Clean crypto banners
    aads: {
      unitId: '2425642',
      size: 'Adaptive',
      enabled: true,
    },

    // [DONATIONS] Ko-Fi - 0% Fees
    kofi: {
      username: 'chirag127',
      label: 'Support Me',
      enabled: true,
    },

    // [AFFILIATE] Amazon Associates
    amazon: {
      trackingId: 'chirag127-20',
      marketplace: 'US',
      enabled: true,
    },

    // DISABLED: Intrusive ad networks
    adsterra: { enabled: false },
    monetag: { enabled: false },
    hilltopads: { enabled: false },
    coinzilla: { enabled: false },
  },

  // ========================================================================
  // 2. ANALYTICS STACK (8-Layer Redundancy)
  // Strategy: Capture 100% of data with AdBlock-resistant tools
  // ========================================================================
  tracking: {
    // [STANDARD] Google Analytics 4
    ga4: {
      measurementId: 'G-BPSZ007KGR',
      enabled: true,
    },

    // [HEATMAPS] Microsoft Clarity
    clarity: {
      projectId: 'v9yyfdb222',
      enabled: true,
    },

    // [BACKUP RECORDINGS] Yandex Metrica
    yandex: {
      tagId: 106547626,
      webvisor: true,
      clickmap: true,
      enabled: true,
    },

    // [PRODUCT DATA] Mixpanel
    mixpanel: {
      token: '54c23accec03549caca40b0a7efab7d6',
      enabled: true,
    },

    // [SERVER SIDE] Cloudflare Web Analytics - Cannot be blocked
    cloudflare: {
      token: '333c0705152b4949b3eb0538cd4c2296',
      enabled: true,
    },

    // [PRIVACY] GoatCounter
    goatcounter: {
      code: 'chirag127',
      enabled: true,
    },

    // [JOURNEYS] Amplitude
    amplitude: {
      apiKey: 'd1733215e7a8236a73912adf86ac450b',
      enabled: true,
    },

    // [AUTO-CAPTURE] Heap
    heap: {
      appId: '3491046690',
      enabled: true,
    },
  },

  // ========================================================================
  // 3. RELIABILITY STACK (Error Tracking & Monitoring)
  // Strategy: Detect client-side errors since we have no server logs
  // ========================================================================
  reliability: {
    // [PRIMARY] Sentry
    sentry: {
      dsn: 'https://45890ca96ce164182a3c74cca6018e3e@o4509333332164608.ingest.de.sentry.io/4509333334458448',
      enabled: true,
    },

    // [BACKUP] Honeybadger
    honeybadger: {
      apiKey: 'hbp_d5yADoevD4dyItN7Bu5bqNevwqgjaJ3ns2lE',
      enabled: true,
    },

    // [REAL-TIME] Rollbar
    rollbar: {
      accessToken: 'f06dfc71b1c840e6a101d8dd317146f2',
      enabled: true,
    },

    // [STABILITY] Bugsnag
    bugsnag: {
      apiKey: '84afb61cb3bf458037f4f15eeab394c4',
      enabled: true,
    },

    // [UPTIME] Cronitor RUM
    cronitor: {
      rumKey: '205a4c0b70da8fb459aac415c1407b4d',
      enabled: true,
    },
  },

  // ========================================================================
  // 4. BAAS & ENGAGEMENT STACK (Serverless Backend)
  // Strategy: Add dynamic features without hosting
  // ========================================================================
  baas: {
    // [CORE] Firebase (Auth + DB)
    firebase: {
      config: {
        apiKey: 'AIzaSyCx--SPWCNaIY5EJpuJ_Hk28VtrVhBo0Ng',
        authDomain: 'fifth-medley-408209.firebaseapp.com',
        projectId: 'fifth-medley-408209',
        storageBucket: 'fifth-medley-408209.firebasestorage.app',
        messagingSenderId: '1017538017299',
        appId: '1:1017538017299:web:bd8ccb096868a6f394e7e6',
      },
      enabled: true,
    },

    // [SUPPORT] Tawk.to Live Chat
    tawkto: {
      sourceUrl: 'https://embed.tawk.to/6968e3ea8783b31983eb190b/1jf0rkjhp',
      enabled: true,
    },

    // [COMMENTS] Giscus via GitHub Discussions
    giscus: {
      repo: 'chirag127/finsuite',
      repoId: 'R_kgDOQ6Jz_Q',
      categoryId: 'DIC_kwDOQ6Jz_c4C1VQo',
      enabled: true,
    },

    // [EMAIL] MailerLite
    mailerlite: {
      apiKey: 'mlsn.6bc1e1ae5ce788bf939db506b25d8b3e020e53b761b55cf515353882dfd71f51',
      enabled: true,
    },

    // [EXPERIMENTS] GrowthBook A/B Testing
    growthbook: {
      clientKey: 'sdk-BamkgvyjaSFKa0m6',
      enabled: true,
    },

    // [CAPTCHA] Cloudflare Turnstile
    turnstile: {
      siteKey: '',
      enabled: false,
    },
  },

  // ========================================================================
  // 5. UTILITY STACK (Frontend Assets)
  // ========================================================================
  utility: {
    fonts: {
      families: ['Inter:wght@400;600', 'JetBrains+Mono:wght@400;500'],
      display: 'swap',
      enabled: true,
    },
    icons: {
      provider: 'cdnjs',
      enabled: true,
    },
    translate: {
      defaultLang: 'en',
      enabled: false,
    },
  },

  // ========================================================================
  // 6. DEPLOYMENT CONFIGURATION
  // ========================================================================
  deployment: {
    cloudflare: {
      projectName: 'finsuite',
      domain: 'money.chirag127.in',
      enabled: true,
    },
    netlify: {
      siteId: '7a955d56-e3ba-4c81-aaeb-53677727ff99',
      domain: 'finsuite.netlify.app',
      enabled: true,
    },
    vercel: {
      projectId: 'prj_Zb3N3SQpBfmwcrd0NFeqmRbS1UlV',
      domain: 'finsuite.vercel.app',
      enabled: true,
    },
    surge: {
      domain: 'finsuite.surge.sh',
      enabled: true,
    },
    neocities: {
      sitename: 'chirag127',
      domain: 'chirag127.neocities.org',
      enabled: true,
    },
    githubPages: {
      repo: 'chirag127/finsuite',
      domain: 'chirag127.github.io/finsuite',
      enabled: true,
    },
  },
};

export default APEX_CONFIG;
