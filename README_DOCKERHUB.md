# Pepkio Floor Time — Lab Meeting Clock

Run containerized scientific meeting moderation, fair floor-time allocation, and dynamic Q&A buffer calculation via the Pepkio API without local Python dependencies.

# What It Does

The container runs `pepkio-floor-time-lab-meeting-clock`, a command-line client for the Pepkio Floor Time — Lab Meeting Clock REST API. It allows research groups, journal clubs, and seminar organizers to programmatically allocate equitable presentation slots, partition dedicated per-speaker Q&A windows or global meeting buffers, dynamically adjust remaining intervals using carryover math when speakers finish early or late, and randomize presenter queues to eliminate positional order bias.

Calculations execute on Pepkio servers; provide a network connection and an API key with `tools:run` scope for `run` commands. Inspecting manifests and examples does not require an API key.

# Features

- Equal and weighted presentation time allocation algorithms across research group members
- Dedicated global meeting buffer and per-speaker Q&A interval management
- Dynamic schedule recalculation (carryover math) based on actual elapsed presentation durations
- Fisher-Yates presenter queue randomization to prevent long-term presentation order bias
- Schedule validation to detect meeting duration overbooking before sessions begin
- Formatted meeting summary table and CSV export generation
- Preconfigured manifest examples (`compute_equal_split`, `shuffle_participants`, `validate_setup`, `build_summary_csv`)
- Manifest and example inspection without an API key

# Quick Start

```bash
docker pull pepkio/floor-time-lab-meeting-clock:0.1.0
docker run --rm -e PEPKIO_API_KEY="your-key" pepkio/floor-time-lab-meeting-clock:0.1.0 \
  run --example compute_equal_split
```

Manifest only (no API key):

```bash
docker run --rm pepkio/floor-time-lab-meeting-clock:0.1.0 manifest --examples
```

Set `PEPKIO_API_BASE_URL` to override the API host (default: `https://tools.pepkio.com`). Create an API key with **tools:run** scope at https://www.pepkio.com/account/api-keys.

# Quick Example

Calculate equal speaking allocations for three participants in a 60-minute meeting with a 10-minute buffer using the built-in `compute_equal_split` example:

```bash
export PEPKIO_API_KEY="your-key"

docker run --rm \
  -e PEPKIO_API_BASE_URL=https://tools.pepkio.com \
  -e PEPKIO_API_KEY="$PEPKIO_API_KEY" \
  pepkio/floor-time-lab-meeting-clock:0.1.0 run --example compute_equal_split
```

# Typical Use Cases

- Weekly research group meetings dividing 60-minute or 90-minute sessions into equal speaker slots with reserved discussion time
- Journal club literature reviews balancing background overview, methods analysis, and audience questions
- Departmental work-in-progress (WIP) seminars coordinating rotating presentation slots across multiple benches
- Thesis defense and committee presentation rehearsals enforcing strict presentation limits and committee Q&A
- Collaborative consortium workshops maintaining strict floor-time equity across partner research institutions

# Scientific Background

Laboratory group meetings and departmental seminars require balanced time distribution to ensure junior researchers and graduate students receive feedback alongside senior presenters. Unstructured sessions frequently suffer from Parkinson's Law and discussion overruns that compress later presentations.

Total available talk duration $T_{\text{net}}$ is computed by subtracting the reserved buffer $T_{\text{buffer}}$ from total scheduled duration $T_{\text{total}}$:

$$T_{\text{net}} = T_{\text{total}} - T_{\text{buffer}}$$

For $N$ presenters with relative weights $w_i$, allocated floor time $t_i$ is determined by:

$$t_i = T_{\text{net}} \times \frac{w_i}{\sum_{j=1}^N w_j}$$

When dynamic carryover is enabled, elapsed talk variances $\Delta_k = t_k - a_k$ from completed speakers are distributed proportionally across remaining presentation slots, maintaining hard meeting end times without penalizing downstream speakers.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/floor-time-lab-meeting-clock

Web-only features include live visual countdown rings, audible milestone chime alerts, one-click presenter status toggling, and shareable meeting permalinks.

# Documentation and Resources

GitHub Repository (source and Dockerfile): https://github.com/pepkio/pepkio-floor-time-lab-meeting-clock

Web Application: https://www.pepkio.com/tools/floor-time-lab-meeting-clock

PyPI Package: https://pypi.org/project/pepkio-floor-time-lab-meeting-clock/

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

A semantic, AI-native version of this document in the K2F format is available at https://k2f.dev (https://k2f.dev/v/35cb6569010ea7990cdff8e9cf762e3cfe57f6e4eb92a536b3d13322123a606a)
