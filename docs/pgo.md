# Profile-Guided Optimization (PGO) and non-PGO builds

Starting with [Percona Server for MySQL {{release}}](release-notes/{{release}}.md), Percona publishes a mixture of Profile-Guided Optimization (PGO) and non-PGO builds. With PGO, the compiler uses profiling data from representative workloads to guide optimization, which can improve throughput and reduce latency for typical database workloads compared with non-PGO builds.

To install Percona Server for MySQL, see [Install Percona Server for MySQL from repositories](installation.md).

## Benefits of PGO builds

PGO builds are a good default when they are available for your platform. Advantages include the following:

* **Higher performance for typical workloads** — Hot code paths are optimized using profiling data from representative database workloads, which can improve query throughput and reduce latency compared with non-PGO builds.

* **No application changes** — PGO is a compile-time optimization. You install and run Percona Server for MySQL the same way as a non-PGO build; no extra configuration is required.

* **Production-oriented packaging** — When Percona publishes PGO builds for a platform, they are intended for production use where performance matters.

## Considerations for non-PGO builds

A non-PGO build is not inferior by design. You may receive or choose one for reasons such as the following:

* **Platform availability** — Percona does not yet publish a PGO build for every operating system, architecture, or installation method. In those cases, the non-PGO package is the supported option.

* **Consistency with an existing environment** — Use a non-PGO build when you need to match binaries in a test, staging, or support scenario that already runs a non-PGO package (for example, before validating an upgrade path).

* **Custom source builds** — If you compile Percona Server for MySQL yourself, you control whether PGO is enabled. A non-PGO build may be appropriate when you are not using Percona’s profiling workflow or when you need a simpler reproducible build for development.

* **Workload mismatch (uncommon)** — PGO optimizes for the workloads used during profiling. If your workload is highly unusual and differs sharply from typical OLTP-style database traffic, performance gains may be smaller. This is uncommon in practice; most production deployments still benefit from PGO when it is available.

When both PGO and non-PGO builds are published for the same platform, prefer the PGO build for production unless one of the considerations above applies.

## Which build you receive

In most cases, you do not choose PGO or non-PGO at install time. The build type depends on how Percona packages Percona Server for MySQL for your operating system, architecture, and installation method (APT, DNF/YUM, binary tarball, or Docker). Some platforms ship PGO-enabled packages; others ship non-PGO builds while PGO support is rolled out across the release matrix.

See the [Percona downloads :octicons-link-external-16:](https://www.percona.com/downloads/Percona-Server-{{vers}}/) page and the [Percona Software and Platform Lifecycle :octicons-link-external-16:](https://www.percona.com/services/policies/percona-software-platform-lifecycle#mysql) page for supported platforms for this release.

## Build from source

To control whether PGO is used, compile Percona Server for MySQL yourself. See [Compile Percona Server for MySQL from Source](compile-percona-server.md).