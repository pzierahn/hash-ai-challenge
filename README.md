# Recruit

## Introduction

Hiring for a high-context role is difficult to scale without losing the reasoning behind a shortlist. This project is a local, evidence-first recruiting workflow for HASH's Berlin Technical Founder's Associate role. It turns a role brief into a reproducible candidate search, evaluates publicly available profile data against explicit criteria, and produces a ranked shortlist with personalized outreach drafts.

The workflow uses the Coresignal Employee Multi-source API for candidate-profile data and an LLM for structured extraction, assessment, and outreach writing. It preserves the inputs and intermediate outputs needed to inspect how a candidate reached the final shortlist.

## Setup And Installation

### Prerequisites

- Python 3.14 or later
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Coresignal API key with access to the Employee Multi-source API
- An OpenAI API key for the notebooks' default models

### Install

From the repository root, create the environment and install the project dependencies:

```bash
uv sync
source .venv/bin/activate
```

Set the required API keys in the same shell before opening Jupyter:

```bash
export CORESIGNAL_API_KEY="..."
export OPENAI_API_KEY="..."
```

The notebooks use OpenAI models by default. Some cells include commented Anthropic alternatives; set `ANTHROPIC_API_KEY` as well when choosing those models. Start Jupyter from the repository root so the relative paths used by the notebooks resolve correctly:

```bash
jupyter lab
```

## Project Structure

```text
openings/       Role briefs used as the source material for a search and assessment.
notebooks/      The end-to-end, runnable recruiting workflow.
recruit/        Reusable profile cache, API client, Pydantic models, and scoring helpers.
spi/            Local candidate data, criteria, assessments, and CSV exports.
docs/           Challenge brief, HASH mission, and Coresignal API schema reference.
```

`recruit/db.py` caches fetched Coresignal profiles locally and fetches missing profiles on demand. `recruit/pydantic.py` defines the structured role-requirements schema, while `recruit/score.py` applies the deterministic score: required criteria count double, and candidates must receive at least a moderate rating on every required criterion to qualify for the shortlist.

## Processing Steps

Run the notebooks from the `notebooks/` directory in the order below. The selected role is set near the top of each notebook; change the `job_description_path` consistently to process another file in `openings/`.

1. **[01_search_query.ipynb](notebooks/01_search_query.ipynb)**: reads the selected role brief, derives a structured job profile, and generates a Coresignal Elasticsearch DSL candidate query using the API schema in `docs/coresignal/`.
2. **[01_resumes.ipynb](notebooks/01_resumes.ipynb)**: submits the candidate query to Coresignal, retrieves the returned profiles, and stores the public profile data under `spi/coresignal/employee_multi_source/`.
3. **[02_job_criterion.ipynb](notebooks/02_job_criterion.ipynb)**: extracts up to three objectively verifiable required criteria and five to eight preferred criteria from the role brief. Its output is `spi/requirements.json`.
4. **[03_candidate_assessment.ipynb](notebooks/03_candidate_assessment.ipynb)**: evaluates each cached candidate against every criterion, records a rating and supporting evidence, calculates the weighted score, and writes one assessment per candidate to `spi/assessments/`.
5. **[04_shortlist_outreach.ipynb](notebooks/04_shortlist_outreach.ipynb)**: combines assessment records with profile links, filters candidates who meet all required criteria, drafts formal and creative outreach messages, and exports the final analysis-ready CSV.

## Outputs And Review

- `spi/requirements.json`: the extracted must-have and nice-to-have criteria used for assessment.
- `spi/assessments/`: per-candidate structured assessments with evidence for every rating. Review these records before relying on a model-generated score.
- `spi/assessments.csv`: all candidates ranked by weighted score, including their LinkedIn URL and criterion ratings.
- `spi/short_list.csv`: candidates who meet every required criterion.
- `spi/final_short_list_with_outreaches.csv`: the shortlist augmented with formal and creative, candidate-specific outreach drafts.

Shortlist decisions are deliberately auditable: candidates are admitted only when each required criterion is rated `strong` or `moderate`; preferred criteria affect ranking but not eligibility. The CSV exports can be opened in a spreadsheet or loaded into another analysis tool for human review, workflow decisions, and follow-up.
