# Pepkio Floor Time — Lab Meeting Clock

Programmatically compute equitable presentation time allocations, dedicated Q&A buffers, and real-time floor time adjustments for research group meetings and journal clubs via the Pepkio Tools API.

# What It Does

Laboratory progress meetings, journal clubs, and departmental seminars frequently run overtime or suffer from disproportionate floor time distribution. Late presenters and junior researchers often face truncated presentation windows or lost Q&A discussion time.

This package interfaces with the Pepkio Tools API to automate meeting moderation calculations. It splits available session time into fair presentation windows and Q&A slots, subtracts global meeting buffers, randomizes speaker order, and dynamically adjusts remaining slots when speakers finish early or late (carryover math).

Programmatic runs require an active internet connection and a Pepkio API key. Calculations are processed via the Pepkio REST API.

# Features

- Equal and weighted presentation time allocation algorithms across meeting participants
- Dedicated global Q&A and transition buffer subtraction
- Dynamic schedule recalculation (carryover math) based on actual elapsed presentation times
- Fisher-Yates presenter queue randomization to eliminate rotation order bias
- Schedule validation to detect time overbooking before meeting commencement
- Structured timetable breakdown with individual talk and Q&A durations
- Manifest inspection and example discovery (`get_manifest`, `list_examples`, `get_example_input`)
- Command-line utility (`pepkio-floor-time-lab-meeting-clock`) for rapid terminal execution

# Installation

```bash
pip install pepkio-floor-time-lab-meeting-clock
```

Set your API key before invoking `run()`:

```bash
export PEPKIO_API_KEY="your-api-key"
```

Obtain an API key from your [Pepkio account settings](https://www.pepkio.com/account/api-keys).

# Quick Example

```python
from pepkio_floor_time_lab_meeting_clock import PepkioClient

with PepkioClient() as client:
    result = client.run({
        "action": "compute_allocations",
        "participants": [
            {"id": "p1", "name": "Dr. Aris Thorne", "weight": 1.0},
            {"id": "p2", "name": "Elena Rostova", "weight": 1.0},
            {"id": "p3", "name": "Marcus Vance", "weight": 1.0},
        ],
        "total_minutes": 60.0,
        "qa_buffer_minutes": 10.0,
        "equal_split": True,
    })

    print("Meeting Status:", result.status)
    if result.result and "slots" in result.result:
        for slot in result.result["slots"]:
            print(f"- {slot['name']}: {slot['talk_minutes']:.1f} min talk + {slot['qa_minutes']:.1f} min Q&A")
```

Run via CLI using manifest examples:

```bash
pepkio-floor-time-lab-meeting-clock run --example compute_equal_split
```

# Typical Use Cases

- Weekly laboratory progress meetings dividing 60–90 minute sessions into equal student/postdoc windows with reserved Q&A.
- Journal club paper reviews balancing background overview, methods analysis, and audience discussion.
- Work-in-Progress (WIP) departmental seminars coordinating rotating presentation slots across multiple benches.
- Thesis defense and committee presentation rehearsals enforcing strict talk limits and committee Q&A time.
- Collaborative consortium workshops maintaining equitable time division across partner research groups.

# Scientific Background

Total available presentation time $T_{\text{talk}}$ is determined by subtracting global buffer time $T_{\text{buffer}}$ from total session duration $T_{\text{total}}$:

$$T_{\text{talk}} = T_{\text{total}} - T_{\text{buffer}}$$

For $N$ participants with relative weights $w_i$, individual presentation time $t_i$ is calculated as:

$$t_i = T_{\text{talk}} \times \frac{w_i}{\sum_{j=1}^N w_j}$$

When real-time carryover is enabled, unused or excess floor time from early presenters is dynamically redistributed across remaining slots, ensuring hard meeting end times are strictly respected.

# Web Application

For researchers who prefer a graphical interface, an interactive web version is available.

Web Application: https://www.pepkio.com/tools/floor-time-lab-meeting-clock

The browser interface provides live visual countdown timers, audible chime alerts, real-time speaker progress toggling, and shareable meeting permalinks.

# Documentation and Resources

GitHub Repository: https://github.com/pepkio/pepkio-floor-time-lab-meeting-clock

Web Application: https://www.pepkio.com/tools/floor-time-lab-meeting-clock

Source code and issue tracking: https://github.com/pepkio/pepkio-floor-time-lab-meeting-clock

# About Pepkio

Pepkio (https://www.pepkio.com/) develops software tools and bioinformatics solutions for life science researchers, including laboratory calculators and analysis services (https://www.pepkio.com/cro).

# Keywords

- lab meeting clock
- floor time calculator
- scientific presentation timer
- lab meeting scheduler
- journal club timer
- research presentation allocator
- speaker time calculator
- Q&A buffer calculator
- weighted presentation timer
- equal time presentation split
- research group timer
- seminar floor time moderator
- presentation queue shuffle
- Fisher-Yates speaker order
- laboratory time manager
- meeting drift adjustment
- presentation carryover math
- thesis defense timer
- conference talk moderator
- departmental seminar scheduler
- work in progress meeting planner
- scientific meeting moderator
- presentation timetable generator
- Python lab meeting client
- pepkio-floor-time-lab-meeting-clock
- how to allocate presentation time for lab meeting
- calculate equal floor time for research group presentations
- balance presentation and Q&A time in scientific seminars
- dynamic carryover calculation for over-time scientific talks
- fair time distribution for journal club paper presentations
- automate laboratory meeting schedule from Python
- Fisher-Yates presenter order randomization for lab meetings
- prevent speaker overtime in departmental research seminars
- Python API for scientific meeting time management
- command line tool for lab meeting talk allocation
- thesis defense practice timer with Q&A buffer
- multi speaker presentation timer with weighted floor time
- balance talk time across graduate students and postdocs
- schedule research group meeting with global buffer minutes
- generate lab meeting schedule CSV from Python API
- interactive lab meeting timer web application
- real time meeting drift correction algorithm
- Pepkio floor time lab meeting clock python package
