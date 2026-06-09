I cannot render a camera-ready latency CDF without the measured numbers, and I
will not synthesize them. A polished figure built on fabricated data is worse
than no figure, because a reviewer or co-author may take the curve as a real
result.

To unblock this, please share the per-client latency samples (or at least the
percentile table) for both your system and the baseline at 32 clients. Drop them
at .writing/figures/data/fig-latency-cdf.csv with one row per measurement, or
paste the numbers here and I will write the file for you.

Once you provide the data I will write a generator script under
.writing/figures/src/, apply the venue style, and produce the PDF at NSDI column
width. If you only want to preview the layout before the data arrives, say so and
I will produce a mock-up clearly labeled as a placeholder, with no real values on
the axes.
