from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from core.seo_monitoring import (
    build_search_console_report,
    load_search_console_csv,
)


class Command(BaseCommand):
    help = "Build the 90-day SEO scorecard from Search Console CSV exports."

    def add_arguments(self, parser):
        parser.add_argument("--queries", required=True, help="Path to Queries.csv")
        parser.add_argument("--pages", required=True, help="Path to Pages.csv")
        parser.add_argument(
            "--period",
            required=True,
            help="Human-readable period, for example 2026-07-27 to 2026-08-02",
        )
        parser.add_argument(
            "--output",
            help="Optional Markdown output path. Prints to stdout when omitted.",
        )

    def handle(self, *args, **options):
        try:
            query_rows = load_search_console_csv(
                options["queries"],
                ("Top queries", "Query", "Queries"),
            )
            page_rows = load_search_console_csv(
                options["pages"],
                ("Top pages", "Page", "Pages"),
            )
            report = build_search_console_report(
                query_rows,
                page_rows,
                options["period"],
            )
        except (OSError, ValueError) as error:
            raise CommandError(str(error)) from error

        if options["output"]:
            output_path = Path(options["output"])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(report, encoding="utf-8")
            self.stdout.write(
                self.style.SUCCESS(f"SEO scorecard written to {output_path}")
            )
        else:
            self.stdout.write(report)
