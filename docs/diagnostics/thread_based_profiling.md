# Thread based profiling

*Percona Server for MySQL* now uses thread based profiling by default, instead of process based profiling. This was implemented because with process based profiling, threads on the server, other than the one being profiled, can affect the profiling information.

## Version specific information

* 8.0.12-1: The feature was ported from *Percona Server for MySQL* 5.7.
  
Thread based profiling is using the information provided by the kernel [getrusage](https://kernel.org/doc/man-pages/online/pages/man2/getrusage.2.html) function. Since the 2.6.26 kernel version, thread based resource usage is available with the **RUSAGE_THREAD**. This means that the thread based profiling will be used if you’re running the 2.6.26 kernel or newer, or if the **RUSAGE_THREAD** has been ported back.

This feature is enabled by default if your system supports it, in other cases it uses process based profiling.
