# Root cause taxonomy

Classify at least:

- memory leak / retention;
- concurrency amplification;
- unbounded queue / fan-out;
- expensive request path;
- subprocess / exec amplification;
- allocator / heap behavior;
- cgroup limit mismatch;
- swap thrash;
- CPU starvation;
- disk pressure;
- I/O blocking;
- restart loop;
- dependency latency;
- capacity exhaustion.

Always separate the final trigger from the structural defect.
