# Ancient Atlas measurement

Configured October 23, 2026 under ancient.atlas.studio@gmail.com.

- Stream: Ancient Atlas Website, https://theancientatlas.com
- Stream ID: 16191106336
- Measurement ID: G-LZSJ94PNP6
- Google Ads: 839-099-3000, linked through Data manager
- Reporting: America/Los_Angeles, USD

GoatCounter tags remain unchanged. GA4 loads only on the production domain after the visitor chooses Allow analytics. Global Privacy Control disables GA4. Preferences can be reopened using the Analytics preferences button. Declining or withdrawing consent leaves navigation and GoatCounter alone. Analytics consent alone is granted; advertising storage, user data, personalization and Google signals remain disabled.

Enhanced measurement records page/engagement activity. Catalog card views emit atlas_site_view with the catalog site_name; opening a video through the map helper emits atlas_video_open with its valid YouTube video_id. Events are not imported as Ads conversions and no bidding or budgets are changed. Page URLs include only known campaign parameters, and referrers are reduced to their origin. No form values or search text are sent by custom events.

The shared loader is public/assets/js/analytics.js. scripts/install-ga4.py adds it once to published HTML; build.py runs that step after regenerating site pages. Creator and pattern generators include the loader in their templates. New standalone pages can be covered by running the installer.

Validation: node scripts/test-analytics.mjs, node --check public/assets/js/analytics.js, Python generator compilation, full build, loader coverage and preservation of existing GoatCounter tags. The full build also reorders existing videos; those unrelated generated changes were excluded from this change.
