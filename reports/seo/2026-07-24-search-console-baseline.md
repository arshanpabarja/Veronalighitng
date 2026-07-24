# Verona Lighting Search Console Baseline

Captured: 24 July 2026  
Performance data available: 19–22 July 2026  
Property: `sc-domain:veronalighting.co`  
Search type: Web

This is an early four-day baseline, not a full weekly scorecard. Search Console
is still processing several reports, and low-volume query rows may be withheld.

## Performance

### All countries

- Clicks: 22
- Impressions: 67
- CTR: 32.8%
- Average position: 8.1

Disclosed query rows:

| Query | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| verona lighting | 8 | 18 | 44.4% | 1.6 |
| linear cove lighting | 0 | 4 | 0% | 58.2 |
| linear led cove lighting | 0 | 2 | 0% | 57.0 |

### Iran

- Clicks: 20
- Impressions: 50
- CTR: 40%
- Average position: 2.8

The only disclosed Iran query was `verona lighting`: 7 clicks, 15 impressions,
46.7% CTR, position 1.0. The difference between totals and disclosed query rows
is expected when Google withholds low-volume queries.

Top disclosed Iran pages:

| Page | Clicks | Impressions | CTR | Position |
|---|---:|---:|---:|---:|
| `/` | 5 | 15 | 33.3% | 1.1 |
| `/decorative/` | 1 | 8 | 12.5% | 6.0 |
| `/products/` | 1 | 5 | 20% | 5.2 |
| `/en/` | 1 | 3 | 33.3% | 3.3 |
| `http://veronalighting.co/` | 0 | 15 | 0% | 8.9 |
| `/industrial/` | 0 | 4 | 0% | 9.5 |
| `/en/products/` | 0 | 1 | 0% | 2.0 |

The HTTP homepage row is historical Performance data. The current HTTPS report
shows 61 HTTPS URLs and 0 non-HTTPS URLs.

## Sitemap and coverage

- Submitted sitemap: `https://veronalighting.co/sitemap.xml`
- Type: Sitemap index
- Submitted: 20 July 2026
- Last read: 23 July 2026
- Status: Success
- Discovered pages: 502
- Discovered videos: 0
- Action: do not resubmit while the status remains Success

The Page indexing and Links reports were still showing “Processing data, please
check again in a day or so.”

## Priority URL inspection

| Cluster | URL | Google status on 24 July |
|---|---|---|
| Recessed linear | `/linear/c/recessed/` | Not indexed — unknown to Google |
| Magnetic track | `/low-voltage-magneto/` | Indexed |
| Recessed product | `/linear/c/recessed/sp/sp-narrow/` | Indexed |
| Recessed product | `/linear/c/recessed/BD/bd-narrow/` | Discovered, currently not indexed |
| Magnetic product | `/low-voltage-magneto/c/magent-small-family/magnet-linear/magnetar-small-linear/` | Indexed |
| Magnetic product | `/low-voltage-magneto/c/magent-large4cm-family/magnet-linear/magnetar-large-linear/` | Not indexed — unknown to Google |
| Recessed guide | `/news/trimmed-vs-trimless-recessed-linear-lighting/` | Not indexed — unknown to Google |
| Recessed guide | `/news/recessed-linear-lighting-knauf-ceiling-installation/` | Not indexed — unknown to Google |
| Magnetic guide | `/news/what-is-magnetic-track-lighting/` | Not indexed — unknown to Google |
| Magnetic guide | `/news/recessed-surface-suspended-magnetic-track/` | Not indexed — unknown to Google |
| Authority project | `/projects/private-villa/` | Indexed |
| Authority project | `/projects/diamond-boutique/` | Discovered, currently not indexed |

Result: 4 of 12 priority URLs are currently indexed. All 12 pass the local
technical audit and are included in the corrected local sitemap. Indexing
requests must wait until the current SEO changes are deployed.

## Structured data

### Product snippets

- Valid: 1
- Invalid: 1
- Critical issue: either `offers`, `review`, or `aggregateRating` should be
  specified
- Affected item: `TRITON`
- Affected URL: `/en/industrial/triton/triton/`
- Last crawled: 24 July 2026
- Validation status: Started on 24 July 2026

The local template now publishes `ItemPage`, not an ineligible `Product`
snippet. Google is still reporting the currently deployed/crawled version.

### Breadcrumbs

- Valid: 48
- Invalid: 2
- `/en/industrial/triton/triton/`: missing `item` in `itemListElement`
- `/applications/office/`: missing `name` or `item.name`

The local templates now give every breadcrumb item both a non-empty `name` and
an absolute `item` URL. The Office validation was already marked Started; the
TRITON item fix must be validated after deployment.

### Other enhancement data

- Merchant listings: 1 valid, 0 invalid
- Unparsable structured data: 0 invalid
- Core Web Vitals: no field data yet

## Deployment-gated next actions

1. Deploy the completed SEO changes.
2. Confirm the deployed sitemap still reports Success; do not submit it again.
3. Test the six URLs listed in `SEO_STEP_8_90_DAY_SCORECARD.md` with URL
   Inspection.
4. Request indexing once for those six URLs after their live tests pass.
5. Validate the remaining Product snippet and Breadcrumb fixes after deployment.
6. Record the first complete Monday–Sunday Iran/Web scorecard; do not judge the
   target keyword campaign from this four-day baseline.

