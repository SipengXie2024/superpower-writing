#!/usr/bin/env python3
"""
Example usage of the Research Lookup skill.

ResearchLookup routes each query to one of two backends:
  - Parallel Chat API            -> general / web research (default)
  - Perplexity (via OpenRouter)  -> academic queries (paper / citation / DOI lookups)

Routing is automatic (based on academic keywords in the query) and can be
overridden with force_backend. The offline section in main() exercises the
routing logic with no API keys and no network.
"""

import os
from research_lookup import ResearchLookup


def example_automatic_routing():
    """Automatic backend selection based on the query."""
    print("=" * 80)
    print("EXAMPLE 1: Automatic Backend Routing")
    print("=" * 80)
    print()

    research = ResearchLookup()

    # General query -> Parallel Chat API
    query1 = "Recent advances in transformer attention mechanisms 2024"
    print(f"Query: {query1}")
    result1 = research.lookup(query1)
    print(f"Success: {result1.get('success')} | Model: {result1.get('model')}")
    print()

    # Academic query ("find papers ...") -> Perplexity
    query2 = "find papers comparing Raft and Paxos consensus protocols"
    print(f"Query: {query2}")
    result2 = research.lookup(query2)
    print(f"Success: {result2.get('success')} | Model: {result2.get('model')}")
    print()


def example_manual_override():
    """Force a specific backend regardless of the query."""
    print("=" * 80)
    print("EXAMPLE 2: Manual Backend Override")
    print("=" * 80)
    print()

    query = "Explain the mechanism of the Raft consensus algorithm"

    # Force the Parallel Chat API
    research_parallel = ResearchLookup(force_backend="parallel")
    print(f"Query: {query}  [force_backend='parallel']")
    result = research_parallel.lookup(query)
    print(f"Success: {result.get('success')} | Model: {result.get('model')}")
    print()

    # Force Perplexity
    research_perplexity = ResearchLookup(force_backend="perplexity")
    print(f"Query: {query}  [force_backend='perplexity']")
    result = research_perplexity.lookup(query)
    print(f"Success: {result.get('success')} | Model: {result.get('model')}")
    print()


def example_batch_queries():
    """Batch processing; each query is routed independently."""
    print("=" * 80)
    print("EXAMPLE 3: Batch Query Processing")
    print("=" * 80)
    print()

    research = ResearchLookup()
    queries = [
        "Recent benchmarks for LLM inference latency",          # general  -> parallel
        "find papers on deep learning for query optimization",  # academic -> perplexity
        "Statistical power analysis methods",                   # general  -> parallel
    ]

    results = research.batch_lookup(queries, delay=1.0)
    for i, result in enumerate(results):
        print(f"Query {i + 1}: {result.get('query', '')[:50]}...")
        print(f"  Success: {result.get('success')} | Model: {result.get('model')}")
        print()


def example_scientific_writing_workflow():
    """Backend routing across the phases of a writing workflow."""
    print("=" * 80)
    print("EXAMPLE 4: Scientific Writing Workflow")
    print("=" * 80)
    print()

    print("PHASE 1: Literature Review (academic queries -> Perplexity)")
    for query in [
        "find papers on machine learning for compiler optimization 2024",
        "literature on reinforcement learning for database query planning",
        "find articles on distributed data-parallel training",
    ]:
        print(f"  - {query}")
    print()

    print("PHASE 2: Discussion (general synthesis -> Parallel Chat API)")
    for query in [
        "Compare the trade-offs of consensus protocols in distributed systems",
        "Relationship between model interpretability and production adoption",
        "Trade-offs of speculative decoding in LLM inference",
    ]:
        print(f"  - {query}")
    print()


def main():
    """Run the offline routing demo (no API keys or network required)."""
    # The live examples above need real API keys; keep them opt-in.
    # example_automatic_routing()
    # example_manual_override()
    # example_batch_queries()
    # example_scientific_writing_workflow()

    print("=" * 80)
    print("BACKEND ROUTING (offline -- no API calls)")
    print("=" * 80)
    print()

    # Dummy keys so both backends register as available; _select_backend then
    # routes purely on the query, which is what this demo illustrates.
    os.environ.setdefault("PARALLEL_API_KEY", "test")
    os.environ.setdefault("OPENROUTER_API_KEY", "test")
    research = ResearchLookup()

    test_queries = [
        ("find papers on Raft consensus", "perplexity"),
        ("Recent LLM inference benchmarks", "parallel"),
        ("citations for the Paxos paper", "perplexity"),
        ("Explain how a bloom filter works", "parallel"),
        ("literature on cache replacement policies", "perplexity"),
    ]

    for query, expected in test_queries:
        backend = research._select_backend(query)
        status = "✓" if backend == expected else "✗"
        print(f"{status} '{query}'")
        print(f"  -> {backend}")
        print()


if __name__ == "__main__":
    main()
