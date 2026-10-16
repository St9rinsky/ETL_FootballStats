# ⚽ ETL Football Stats

A Python-based data engineering project that extracts football match data from the [football-data.org API](https://www.football-data.org/), stores the raw responses in a bronze layer, and processes them with **PySpark** and **Delta Lake** into structured datasets for downstream analysis.

The project explores a layered data pipeline, incremental processing, and maintaining match records across repeated runs.

## Overview

The pipeline is organised around a Bronze-to-Silver flow:

1. **Extract** football match data from football-data.org.
2. **Bronze layer** preserve the source responses as raw JSON so the original API data remains available.
3. **Transform** the extracted data with PySpark into structured match and team records.
4. **Silver layer** write the transformed datasets as Delta tables, providing a more consistent format for downstream querying and analysis.
5. **Update existing data** using Delta Lake merge logic so matching match records can be updated while new records are inserted.

> **Scope:** The repository currently demonstrates the extraction and Bronze/Silver processing flow. A separate Gold analytics layer or dashboard is not documented as an implemented feature here.

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Pipeline implementation and orchestration |
| football-data.org API | Source of football match data |
| PySpark | Distributed-style data processing and transformations |
| Delta Lake | Delta table storage and merge/upsert operations |
| Docker / Docker Compose | Containerised development and execution environment |
| Make | Scripts for common project commands, where configured |

## Pipeline Architecture

```text
football-data.org API
        |
        v
   Data extraction
        |
        v
  Bronze layer
  Raw JSON data
        |
        v
 PySpark transformations
        |
        v
   Silver layer
 Structured Delta tables
 (matches and teams)
        |
        v
 Downstream analysis / querying
```

### Bronze layer

The Bronze layer retains data close to its original source representation. Keeping raw API responses makes it possible to revisit the source data if transformation logic changes.

### Silver layer

The Silver layer converts the raw data into structured datasets for match and team information. PySpark is used to process the data, and Delta Lake stores the results in Delta format.

### Updating records

The pipeline uses Delta Lake merge logic to match incoming match records against existing records. This supports updating records that already exist and inserting new records, rather than blindly appending duplicate match rows on every run.

## Repository Structure

```text
ETL_FootballStats/
├── src/             # Extraction and transformation implementation
├── main.py          # Pipeline entry point
├── requirements.txt # Python dependencies
├── Dockerfile       # Container image configuration
├── compose.yml      # Docker Compose configuration
├── Makefile         # Common project commands
└── LICENSE          # MIT licence
```

The exact files under `src/` contain the individual pipeline components; refer to the source code for implementation details.

## Prerequisites

For local development, install:

- Git
- Python compatible with the dependencies in `requirements.txt`
- Java, as required by the installed PySpark version
- A football-data.org API token

To use the containerised setup, install Docker and the Docker Compose plugin instead. Check the Docker and Compose files for the environment expected by the project.

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/St9rinsky/ETL_FootballStats.git
cd ETL_FootballStats
```

### 2. Configure the API token

Create a `.env` file in the project root if the application configuration expects environment variables from it. Add your own football-data.org token using the variable name referenced in the source code or Compose configuration.

```dotenv
# Use the exact variable name expected by the project
FOOTBALL_DATA_API_KEY=your_api_token_here
```

Do not commit your real API token or other credentials to Git. If the project uses a different variable name, use the name defined in its configuration.

### 3. Install dependencies (local setup)

Create and activate a virtual environment, then install the project requirements.

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the pipeline

Run the entry point from the repository root:

```bash
python main.py
```

The pipeline's output locations and runtime options depend on the project configuration. Inspect the configuration and source modules if you need to change where raw JSON or Delta tables are stored.

## Running with Docker Compose

The repository includes a Dockerfile and `compose.yml`. From the project root, you can build and start the configured services with:

```bash
docker compose up --build
```

Use `docker compose down` to stop and remove the Compose-managed containers. Review `compose.yml` for configured services, mounts, environment variables, and any required ports before running it.

## Data Engineering Concepts Demonstrated

- **API ingestion:** retrieving data from an external data source.
- **Layered data architecture:** separating raw source data from transformed datasets.
- **Distributed data processing:** using PySpark transformations.
- **Lakehouse storage:** persisting structured datasets with Delta Lake.
- **Incremental record maintenance:** using merge operations to update existing match records and insert new records.
- **Containerisation:** providing Docker-based project configuration for a repeatable environment.

## Configuration and Troubleshooting

- **API authentication or rate limits:** verify that your token is valid and that the environment variable name matches the code.
- **Spark startup issues:** confirm that Java is installed and that the Java version is compatible with your PySpark version.
- **Delta Lake compatibility:** PySpark and Delta Lake versions must be compatible with one another; use the versions declared in the project dependencies.
- **File paths and persistence:** check the Compose volume mounts and the pipeline's configured output paths to ensure data is written where expected.
- **Container environment:** if running in Docker, configure environment variables in the way specified by `compose.yml` rather than assuming local shell variables are passed through automatically.

## Future Improvements

Potential next steps for the project include:

- Add a Gold layer with analytics-ready aggregations and business metrics.
- Add automated data-quality checks for required fields, duplicate match identifiers, and valid score values.
- Add tests for extraction, transformations, and Delta merge behaviour.
- Add scheduled orchestration and monitoring if the pipeline needs to run automatically.
- Document example queries and downstream analytical use cases.

These are possible extensions, not claims about current functionality.

## Licence

This project is licensed under the MIT License. See [`LICENSE`](LICENSE) for details.

## Author

**Sello Letswalo** — [GitHub](https://github.com/St9rinsky)
