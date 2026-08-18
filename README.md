# Pepkio Floor Time — Lab Meeting Clock

Python client for the Pepkio `floor-time-lab-meeting-clock` REST API: split speaking time fairly across lab members, shuffle participant order, validate meeting setups, and build post-meeting summary exports.

## Quick Start

```python
from pepkio_floor_time_lab_meeting_clock import PepkioClient

client = PepkioClient(api_key="your-api-key")

# Compute equal speaking time split for 3 participants in a 30 min meeting with 5 min Q&A
result = client.run({
    "action": "compute_allocations",
    "participants": [
        {"id": "1", "name": "Alice", "weight": 1},
        {"id": "2", "name": "Bob", "weight": 1},
        {"id": "3", "name": "Carol", "weight": 1}
    ],
    "total_minutes": 30,
    "qa_buffer_minutes": 5,
    "equal_split": True
})

print(result.status)  # "completed"
print(result.result["slots"])
```

## CLI Usage

```bash
# Fetch tool manifest
pepkio-floor-time-lab-meeting-clock manifest

# Run example
pepkio-floor-time-lab-meeting-clock run --example compute_equal_split
```
