"""Command-line interface for the Candidate Ranker."""

from __future__ import annotations

import sys
from pathlib import Path

import click
from rich.console import Console
from rich.table import Table

from candidate_ranker.config import AppConfig, configure_logging, load_config
from candidate_ranker.embedding import EmbeddingEngine
from candidate_ranker.io import load_candidates_from_dir, load_job_description
from candidate_ranker.io.export import export_csv, export_json
from candidate_ranker.pipeline import RankingPipeline

console = Console()


@click.group()
@click.option("--config", "-c", type=click.Path(exists=True), help="Path to YAML config file")
@click.option("--verbose", "-v", is_flag=True, help="Enable debug logging")
@click.pass_context
def cli(ctx: click.Context, config: str | None, verbose: bool) -> None:
    """candidate-ranker — AI-powered candidate ranking system.

    Ranks candidates against job descriptions by understanding
    semantic fit, skills, experience, and behavioral signals.
    """
    cfg = load_config(config)
    if verbose:
        cfg.logging.level = "DEBUG"
    configure_logging(cfg.logging)
    ctx.ensure_object(dict)
    ctx.obj["config"] = cfg


@cli.command()
@click.argument("jd", type=click.Path(exists=True))
@click.argument("candidates_dir", type=click.Path(exists=True))
@click.option("--top-n", type=int, default=20, help="Number of top candidates (default: 20)")
@click.option("--output", "-o", type=click.Path(), default=None, help="Output file path (default: output/ranked_<jd_name>.csv)")
@click.option("--format", "fmt", type=click.Choice(["csv", "json", "both"]), default=None, help="Output format (default: from config)")
@click.pass_context
def rank(
    ctx: click.Context,
    jd: str,
    candidates_dir: str,
    top_n: int,
    output: str | None,
    fmt: str | None,
) -> None:
    """Rank candidates against a job description.

    JD is a JSON file with 'title' and 'description' fields.

    CANDIDATES_DIR is a directory of JSON candidate profile files.
    """
    cfg: AppConfig = ctx.obj["config"]
    fmt = fmt or cfg.export.default_format

    console.print(f"[bold]Loading:[/] {jd}")
    console.print(f"[bold]Candidates:[/] {candidates_dir}")

    embedder = EmbeddingEngine(cfg.embedding)
    pipeline = RankingPipeline(config=cfg, embedder=embedder)
    jd_obj = load_job_description(jd)
    candidates = load_candidates_from_dir(candidates_dir)

    if not candidates:
        console.print("[red]No candidates found. Exiting.[/]")
        sys.exit(1)

    with console.status("[bold green]Ranking candidates..."):
        ranked = pipeline.rank(jd_obj, candidates, top_n=top_n)

    # Write output
    if output is None:
        stem = Path(jd).stem
        output = Path("output") / f"ranked_{stem}.csv"

    output_path = Path(output)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    exported = []
    if fmt in ("csv", "both"):
        csv_path = output_path.with_suffix(".csv") if fmt == "csv" else output_path
        export_csv(ranked, csv_path)
        exported.append(str(csv_path))
    if fmt in ("json", "both"):
        json_path = output_path.with_suffix(".json") if fmt == "json" else output_path.parent / f"{output_path.stem}.json"
        export_json(ranked, json_path)
        exported.append(str(json_path))

    for path in exported:
        console.print(f"[green]Written:[/] {path}")

    # Render results table
    render_results(ranked)


def render_results(ranked: list) -> None:
    table = Table(title=f"Top {len(ranked)} Ranked Candidates")
    table.add_column("Rank", style="cyan", justify="right")
    table.add_column("Name", style="white")
    table.add_column("Overall", style="green", justify="right")
    table.add_column("Semantic", style="blue", justify="right")
    table.add_column("Skills", style="magenta", justify="right")
    table.add_column("Experience", style="yellow", justify="right")
    table.add_column("Behavioral", style="dim", justify="right")

    for rc in ranked:
        table.add_row(
            str(rc.rank),
            rc.name,
            f"{rc.overall_score:.2f}",
            f"{rc.semantic_similarity:.2f}",
            f"{rc.skill_match:.2f}",
            f"{rc.experience_relevance:.2f}",
            f"{rc.behavioral_signals:.2f}",
        )

    console.print(table)


@cli.command()
def generate() -> None:
    """Generate sample job descriptions and candidate profiles."""
    from candidate_ranker.io.generator import generate_all
    generate_all()


@cli.command()
def info() -> None:
    """Display system information and configuration."""
    cfg = AppConfig()
    console.print("[bold]Candidate Ranker[/]")
    console.print(f"  Embedding model: {cfg.embedding.model_name}")
    console.print(f"  Top-N: {cfg.pipeline.top_n}")
    console.print(f"  Scoring weights:")
    for k, v in cfg.scoring.model_dump().items():
        console.print(f"    {k}: {v * 100:.0f}%")


def main() -> None:
    cli()


if __name__ == "__main__":
    main()
