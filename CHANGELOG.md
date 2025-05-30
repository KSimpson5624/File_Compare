## [v3.0] - 2025-05-29

### Changed
- Rewrote file comparison logic to use `collections.Counter`.
- Removed redundant union logic for further optimization.
- Mean comparison time reduced from 33.2ms to 0.169ms.

![v3.0 Benchmark](benchmark_mean_time.png)
