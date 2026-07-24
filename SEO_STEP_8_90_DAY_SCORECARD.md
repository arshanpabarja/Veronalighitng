# Verona Lighting — Step 8 Search Console Scorecard

Campaign window: 24 July–22 October 2026  
Market: Iran  
Search type: Web  
Primary language: Persian

## Success definition

The campaign’s ranking objective is:

- A complete seven-day period with an average Search Console position of 5.0 or
  better for either «چراغ خطی توکار» or «چراغ مگنتی»
- Data filtered to Iran and Web Search
- At least 20 impressions in that seven-day period
- The ranking URL must be its assigned landing page, not an unrelated product,
  article, or English page

Average position is directional, not a fixed live rank. Personalized manual
searches are not the campaign score.

## Assigned landing pages

| Query cluster | Primary Persian URL |
|---|---|
| چراغ خطی توکار | https://veronalighting.co/linear/c/recessed/ |
| چراغ مگنتی | https://veronalighting.co/low-voltage-magneto/ |

Supporting articles and products should help these URLs rank; they should not
replace them as the principal commercial result.

## One-time setup after deployment

1. Open Search Console and select the `veronalighting.co` property.
2. Confirm `https://veronalighting.co/sitemap.xml` shows Success.
3. Inspect these six URLs and request indexing after the deployment:
   - https://veronalighting.co/linear/c/recessed/
   - https://veronalighting.co/low-voltage-magneto/
   - https://veronalighting.co/news/trimmed-vs-trimless-recessed-linear-lighting/
   - https://veronalighting.co/news/recessed-linear-lighting-knauf-ceiling-installation/
   - https://veronalighting.co/news/what-is-magnetic-track-lighting/
   - https://veronalighting.co/news/recessed-surface-suspended-magnetic-track/
4. For each live test confirm:
   - Page fetch: Successful
   - Crawl allowed: Yes
   - Indexing allowed: Yes
   - User-declared canonical matches the inspected URL
5. Do not resubmit the sitemap if its existing status is Success.

## Weekly export

Run this every Monday using the previous complete Monday–Sunday period:

1. Performance → Search results.
2. Search type: Web.
3. Add Country: Iran.
4. Set the exact seven-day date range.
5. Enable Clicks, Impressions, Average CTR, and Average position.
6. Export the Queries table as CSV.
7. Export the Pages table as CSV.
8. Generate the scorecard:

```text
python manage.py analyze_search_console \
  --queries path/to/Queries.csv \
  --pages path/to/Pages.csv \
  --period "YYYY-MM-DD to YYYY-MM-DD" \
  --output reports/seo/YYYY-MM-DD.md
```

The command groups Persian query variants, checks all priority pages, identifies
queries in positions 6–20, flags low-CTR top-10 queries, and lists priority pages
that did not appear in the export.

## 90-day review cadence

### Days 1–14 — discovery and indexing

- Confirm priority URLs are indexed or have a clear pending crawl state.
- Record impressions, but do not judge rankings from very small samples.
- Fix only confirmed crawling, canonical, structured-data, or rendering issues.
- Keep titles and primary URLs stable.

### Days 15–35 — impressions and query matching

- Confirm impressions are increasing for both target clusters.
- Check which URL Google shows for each target query.
- If an article ranks instead of the intended category, strengthen its contextual
  link to the category and keep the intent distinction clear.
- Expand content only when Search Console reveals a useful missing query.

### Days 36–60 — positions 6–20

- Prioritize queries already receiving impressions at positions 6–20.
- Improve the most relevant section of the assigned landing page.
- Add one useful internal link from a closely related product, project, or guide.
- Pursue the relevant earned links from the Step 7 authority plan.

### Days 61–90 — top-10 CTR and consolidation

- For queries in positions 1–10 with weak CTR, revise the title or description to
  better match the visible search intent.
- Do not change URLs.
- Check whether two Verona pages compete for the same query.
- Preserve the stronger page and redirect or reposition only when the data shows
  sustained cannibalization.

## Decision thresholds

| Signal | Minimum evidence | Action |
|---|---:|---|
| No impressions | 14 complete days | Inspect indexing and discovery |
| Position 6–20 | 5+ weekly impressions | Improve alignment and add one relevant link |
| Position 1–10, low CTR | 10+ weekly impressions and CTR below 3% | Test title/description |
| Wrong Verona URL ranking | Two consecutive weekly exports | Strengthen intent and internal-link ownership |
| Decline | Two complete weekly periods | Audit indexing, canonical, intent and competitors |
| Top-5 milestone | 20+ weekly impressions and position ≤5 | Confirm assigned URL and protect the page |

## What not to do

- Do not change titles every few days.
- Do not create another page targeting the same primary keyword.
- Do not request indexing repeatedly for unchanged URLs.
- Do not treat a zero row in the Performance export as proof of non-indexing.
- Do not use personalized manual Google searches as the ranking report.
- Do not buy bulk backlinks to force short-term movement.

## Weekly record

Each weekly report should retain:

- Exact export period and filters
- Clicks and impressions by target cluster
- Average position and CTR
- Ranking URL for each target query
- Indexed/not-indexed status changes
- Links earned during that week
- One action selected for the next week
- What was deliberately left unchanged
