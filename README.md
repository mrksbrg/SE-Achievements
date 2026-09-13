# Swe-SE-SCI
[![Python application](https://github.com/mrksbrg/SE-Achievements/actions/workflows/python-app.yml/badge.svg)](https://github.com/mrksbrg/SE-Achievements/actions/workflows/python-app.yml)
[![Coverage Status](https://coveralls.io/repos/github/mrksbrg/SE-Achievements/badge.svg?branch=main)](https://coveralls.io/github/mrksbrg/SE-Achievements?branch=main)
[![CodeScene Code Health](https://codescene.io/projects/7137/status-badges/code-health)](https://codescene.io/projects/7137)

Navigating the academic Swedish software engineering landscape can be difficult. Swe-SE-SCI lists all Swedish Software Engineering (SE) scholars with permanent positions at Swedish non-profit research organizations. The ambition is to maintain an index of all Swedish SE scholars with first-authored publications in SCI-listed SE journals, i.e., "SSS scholars". Swe-SE-SCI mines DBLP publication lists to identify typical research topics of Swedish SE research organizations and apparent research interests of SSS scholars.

A reliable and updated index of academic SE in Sweden could bring several benefits. The primary goal is to constitute a gateway for industry to find expertise among researchers – hopefully supporting knowledge transfer, industry-academia collaboration, and more relevant research. Swe-SE-SCI can also be used to find academic partners in new research projects and suitable PhD committee members.

Affiliations are ranked by the number of first-authored SCI publications by SSS scholars. Individual SSS scholars are ranked by their SSS rating – our in-house metric. In contrast to non-decreasing citation-based metrics, the SSS rating fluctuates as it promotes active research with a focus to publish in SCI-listed SE journals. A detailed description is available at http://mrksbrg.com/swesesci/

## Running Swe-SE-SCI

The DBLP web API is behind a bot check, so Swe-SE-SCI mines the monthly [DBLP XML dump](https://drops.dagstuhl.de/entities/collection/10.4230/dblp.xml) published by Schloss Dagstuhl instead. The newest snapshot (about 1.1 GB) is downloaded into `dblp_dump/` when it is not already there, so the first run of a month takes a few minutes longer.

```bash
python swe-se-sci.py
```

The candidate scholars are listed in `input_scholars.csv` and the resulting tables are written to `output/`.
