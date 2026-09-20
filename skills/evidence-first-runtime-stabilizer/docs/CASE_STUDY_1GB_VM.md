# Anonymized field case

This workflow was derived from a real sub-1-GiB Linux VM incident where expensive read-side work overlapped, swap saturated for an extended period, and the kernel eventually OOM-killed the web process.

The durable fix changed workload shape and worker lifetime. Disk cleanup alone was not treated as the root fix.

The final deployed revision was validated through real heavy-worker cycles and a 61-sample production soak.

Identifiers and private infrastructure details are intentionally omitted.
