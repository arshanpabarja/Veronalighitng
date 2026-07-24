"""Search Console export analysis for Verona's 90-day SEO campaign."""

from __future__ import annotations

import csv
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from urllib.parse import urlparse


@dataclass(frozen=True)
class SearchMetric:
    dimension: str
    clicks: float
    impressions: float
    ctr: float
    position: float


PRIORITY_URLS = {
    "/linear/c/recessed/": ("چراغ خطی توکار", "recessed-linear"),
    "/low-voltage-magneto/": ("چراغ مگنتی", "magnetic-track"),
    "/linear/c/recessed/sp/sp-narrow/": ("SP NARROW", "recessed-linear"),
    "/linear/c/recessed/BD/bd-narrow/": ("BD NARROW", "recessed-linear"),
    (
        "/low-voltage-magneto/c/magent-small-family/magnet-linear/"
        "magnetar-small-linear/"
    ): ("MAGNETAR SMALL LINEAR", "magnetic-track"),
    (
        "/low-voltage-magneto/c/magent-large4cm-family/magnet-linear/"
        "magnetar-large-linear/"
    ): ("MAGNETAR LARGE LINEAR", "magnetic-track"),
    "/news/trimmed-vs-trimless-recessed-linear-lighting/": (
        "راهنمای لبه‌دار و بدون لبه",
        "recessed-linear",
    ),
    "/news/recessed-linear-lighting-knauf-ceiling-installation/": (
        "راهنمای نصب در کناف",
        "recessed-linear",
    ),
    "/news/what-is-magnetic-track-lighting/": (
        "راهنمای چراغ مگنتی",
        "magnetic-track",
    ),
    "/news/recessed-surface-suspended-magnetic-track/": (
        "راهنمای انواع نصب ریل مگنتی",
        "magnetic-track",
    ),
    "/projects/private-villa/": ("ویلای خصوصی رویان", "authority"),
    "/projects/diamond-boutique/": ("بوتیک دایموند", "authority"),
}


QUERY_TERMS = {
    "recessed-linear": (
        "چراغ خطی توکار",
        "چراغ خطی بدون لبه",
        "چراغ خطی توکار سقفی",
        "چراغ خطی لبه دار",
        "چراغ خطی لبه‌دار",
    ),
    "magnetic-track": (
        "چراغ مگنتی",
        "ریل مگنتی",
        "چراغ ریلی مگنتی",
        "سیستم روشنایی مگنتی",
    ),
    "brand": (
        "verona lighting",
        "veronalighting",
        "ورونا لایتینگ",
        "روشنایی ورونا",
    ),
}


def _parse_number(value: str | None) -> float:
    cleaned = (value or "0").strip().replace(",", "")
    if not cleaned or cleaned in {"-", "~"}:
        return 0.0
    if cleaned.endswith("%"):
        return float(cleaned[:-1]) / 100
    return float(cleaned)


def _find_column(fieldnames, candidates):
    lookup = {field.strip().casefold(): field for field in fieldnames if field}
    for candidate in candidates:
        if candidate.casefold() in lookup:
            return lookup[candidate.casefold()]
    return None


def load_search_console_csv(path, dimension_candidates):
    csv_path = Path(path)
    with csv_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        fieldnames = reader.fieldnames or []
        dimension_column = _find_column(fieldnames, dimension_candidates)
        clicks_column = _find_column(fieldnames, ("Clicks",))
        impressions_column = _find_column(fieldnames, ("Impressions",))
        ctr_column = _find_column(fieldnames, ("CTR",))
        position_column = _find_column(fieldnames, ("Position",))

        required = {
            "dimension": dimension_column,
            "clicks": clicks_column,
            "impressions": impressions_column,
            "ctr": ctr_column,
            "position": position_column,
        }
        missing = [name for name, column in required.items() if column is None]
        if missing:
            raise ValueError(
                f"{csv_path.name} is missing Search Console columns: "
                f"{', '.join(missing)}"
            )

        return [
            SearchMetric(
                dimension=(row.get(dimension_column) or "").strip(),
                clicks=_parse_number(row.get(clicks_column)),
                impressions=_parse_number(row.get(impressions_column)),
                ctr=_parse_number(row.get(ctr_column)),
                position=_parse_number(row.get(position_column)),
            )
            for row in reader
            if (row.get(dimension_column) or "").strip()
        ]


def normalize_query(value):
    return re.sub(
        r"\s+",
        " ",
        value.casefold()
        .replace("ي", "ی")
        .replace("ك", "ک")
        .replace("\u200c", " "),
    ).strip()


def classify_query(query):
    normalized = normalize_query(query)
    for cluster, terms in QUERY_TERMS.items():
        if any(normalize_query(term) in normalized for term in terms):
            return cluster
    return None


def normalize_page(value):
    parsed = urlparse(value)
    path = parsed.path if parsed.scheme or parsed.netloc else value.split("?", 1)[0]
    if not path.startswith("/"):
        path = f"/{path}"
    if path != "/" and not path.endswith("/"):
        path = f"{path}/"
    return path


def aggregate_metrics(rows):
    clicks = sum(row.clicks for row in rows)
    impressions = sum(row.impressions for row in rows)
    weighted_position = sum(row.position * row.impressions for row in rows)
    return {
        "clicks": clicks,
        "impressions": impressions,
        "ctr": clicks / impressions if impressions else 0,
        "position": weighted_position / impressions if impressions else 0,
    }


def _metric_row(label, metric):
    return (
        f"| {label} | {metric['clicks']:.0f} | "
        f"{metric['impressions']:.0f} | {metric['ctr']:.1%} | "
        f"{metric['position']:.1f} |"
    )


def build_search_console_report(query_rows, page_rows, period_label):
    cluster_metrics = {}
    for cluster in QUERY_TERMS:
        cluster_metrics[cluster] = aggregate_metrics(
            [row for row in query_rows if classify_query(row.dimension) == cluster]
        )

    page_lookup = {normalize_page(row.dimension): row for row in page_rows}
    total_queries = aggregate_metrics(query_rows)
    total_pages = aggregate_metrics(page_rows)

    lines = [
        "# Verona Lighting — Search Console SEO Scorecard",
        "",
        f"Period: {period_label}",
        f"Generated: {date.today().isoformat()}",
        "",
        "## Export totals",
        "",
        "| Export | Clicks | Impressions | CTR | Average position |",
        "|---|---:|---:|---:|---:|",
        _metric_row("Queries", total_queries),
        _metric_row("Pages", total_pages),
        "",
        "Query and page totals can differ because Search Console applies privacy, "
        "aggregation, and row limits.",
        "",
        "## Campaign query clusters",
        "",
        "| Cluster | Clicks | Impressions | CTR | Average position |",
        "|---|---:|---:|---:|---:|",
        _metric_row("چراغ خطی توکار", cluster_metrics["recessed-linear"]),
        _metric_row("چراغ مگنتی", cluster_metrics["magnetic-track"]),
        _metric_row("Brand", cluster_metrics["brand"]),
        "",
        "## Priority Persian pages",
        "",
        "| Page | Clicks | Impressions | CTR | Average position |",
        "|---|---:|---:|---:|---:|",
    ]

    missing_pages = []
    for path, (label, _cluster) in PRIORITY_URLS.items():
        row = page_lookup.get(path)
        if row:
            lines.append(
                _metric_row(
                    f"[{label}](https://veronalighting.co{path})",
                    {
                        "clicks": row.clicks,
                        "impressions": row.impressions,
                        "ctr": row.ctr,
                        "position": row.position,
                    },
                )
            )
        else:
            missing_pages.append(path)
            lines.append(
                f"| [{label}](https://veronalighting.co{path}) | 0 | 0 | — | — |"
            )

    striking_distance = sorted(
        (
            row
            for row in query_rows
            if 5 < row.position <= 20
            and row.impressions >= 5
            and classify_query(row.dimension) in {"recessed-linear", "magnetic-track"}
        ),
        key=lambda row: (-row.impressions, row.position),
    )[:10]
    low_ctr = sorted(
        (
            row
            for row in query_rows
            if 0 < row.position <= 10
            and row.impressions >= 10
            and row.ctr < 0.03
        ),
        key=lambda row: -row.impressions,
    )[:10]

    lines.extend(
        [
            "",
            "## Action queue",
            "",
            "### Ranking positions 6–20",
            "",
        ]
    )
    if striking_distance:
        for row in striking_distance:
            lines.append(
                f"- `{row.dimension}` — position {row.position:.1f}, "
                f"{row.impressions:.0f} impressions: review content alignment "
                "and add one relevant internal or earned link."
            )
    else:
        lines.append("- No target query currently meets the minimum data threshold.")

    lines.extend(["", "### Low-CTR top-10 queries", ""])
    if low_ctr:
        for row in low_ctr:
            lines.append(
                f"- `{row.dimension}` — position {row.position:.1f}, "
                f"CTR {row.ctr:.1%}: review title and description against intent."
            )
    else:
        lines.append("- No query currently meets the minimum data threshold.")

    lines.extend(
        [
            "",
            "### Priority pages absent from this performance export",
            "",
        ]
    )
    if missing_pages:
        lines.extend(f"- https://veronalighting.co{path}" for path in missing_pages)
    else:
        lines.append("- None.")

    lines.extend(
        [
            "",
            "Absence from a Performance export means no row was reported for the "
            "selected period; it does not by itself prove that a page is unindexed.",
            "",
            "## Weekly decision rules",
            "",
            "- Indexed but no impressions: leave metadata stable and strengthen "
            "discovery/internal links before rewriting.",
            "- Position 6–20 with impressions: improve the matching section and earn "
            "one relevant contextual link.",
            "- Position 1–10 with low CTR: test the title and description without "
            "changing the URL.",
            "- Falling impressions across two complete weekly periods: check indexing, "
            "canonical selection, query intent, and competing pages.",
            "- Judge the campaign primarily by impressions and clicks; treat average "
            "position as a directional metric.",
        ]
    )
    return "\n".join(lines) + "\n"
