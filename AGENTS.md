# AGENTS.md

This file provides guidance to Codex (Codex.ai/code) when working with code in this repository.

## Repository Overview

Swe-SE-SCI (Swedish Software Engineering - Science Citation Index) is a tool that tracks and analyzes Swedish Software Engineering researchers and their publications. It identifies scholars with permanent positions at Swedish research organizations who have first-authored publications in SCI-listed SE journals.

The system:
1. Reads a list of candidate scholars from a CSV file
2. Mines their publication data from a local DBLP XML dump
3. Analyzes research interests and affiliation topics
4. Generates statistics and tables for display
5. Maps publications to SWEBOK (Software Engineering Body of Knowledge) areas

## Project Structure

- `swesesci/`: Core modules
  - `scholar.py`: Core data class for researchers
  - `publication.py`: Publication data class with journal/conference classification
  - `scholar_reader.py`: Reads input scholar data
  - `dblp_dump.py`: Downloads the monthly DBLP XML dump, streams it, and replays each scholar's records as per-person XML
  - `scholar_miner.py`: Mines publication data from the DBLP dump
  - `scholar_analyzer.py`: Analyzes research interests
  - `scholar_tabulator.py`: Generates HTML tables
  - `scholar_visualizer.py`: Creates visualizations (commented out in main script)
- `swe-se-sci.py`: Main entry point script
- `templates/`: HTML templates for output
- `test/`: Test cases for validation
- `history/`: Historical HTML outputs organized by year/month

## Commands for Development

### Running the Application

To run the full application:
```bash
python swe-se-sci.py
```

The app expects an `input_scholars.csv` file with candidate scholars.

The DBLP web API (dblp.org/pid/*.xml) is behind a bot check, so scholars are mined from the monthly DBLP XML dump hosted on Dagstuhl DROPS. Unless it is already in `dblp_dump/` (gitignored), `swe-se-sci.py` downloads the newest snapshot (about 1.1 GB) and the DTD it references, and removes older snapshots. Snapshots are published a few days into each month; until then the previous month is used, and without network access the most recent local dump. Set `DBLP_DUMP` to use a specific dump file. Mining makes two passes over the dump and takes several minutes.

### Running Tests

To run all tests:
```bash
pytest
```

To run a specific test file:
```bash
pytest test/test_2_onescholar.py
```

Tests 2-5 read `test/dblp_test_dump.xml.gz`, a small subset of the dump with the test scholars, and write their results to `test/output/` so they do not overwrite the application output in `output/`. To regenerate it from a newer dump (expected values in the tests may then need updating):
```bash
python test/make_test_dump.py dblp_dump/dblp-2026-09-01.xml.gz
```

To run with coverage:
```bash
coverage run -m pytest
coverage report
```

### Linting

For basic syntax checking:
```bash
flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
```

For full style checking:
```bash
flake8 . --count --max-complexity=10 --max-line-length=127 --statistics
```

## Dependencies

- Python 3.9+
- Required packages (main):
  - sortedcontainers
  - pandas
  - nltk (with 'punkt_tab' and 'stopwords' downloads)
  - jinja2 (for templating)
  - xml.sax, pyexpat, gzip (built-in, for parsing the DBLP XML dump)

- Development dependencies:
  - pytest
  - coverage
  - flake8

## Data Flow

1. `scholar_reader.py` reads scholar data from CSV
2. `scholar_miner.py` collects each scholar's DBLP records from the local dump via `dblp_dump.py`
3. Publications are filtered (removes editorial work, etc.)
4. Publications are mapped to SWEBOK knowledge areas
5. `scholar_analyzer.py` calculates statistics and research interests
6. `scholar_tabulator.py` generates HTML tables using templates

## Rating System

The system uses two unique metrics:
- SSS Contribution: Weighted value of publications with focus on first-authored SCI papers
- SSS Rating: Based on weighted harmonic mean of SCI ratio and first-author ratio

## Achievement System

The repository implements a "badge" system for researchers based on their publications in specific SWEBOK knowledge areas:
- Bronze: 1+ publications
- Silver: 3+ publications 
- Gold: 5+ publications
- Platinum: 10+ publications

## Imported Claude Cowork project instructions
