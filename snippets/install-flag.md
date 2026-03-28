
The `-y` flag (on `apt` and `apt-get`, `--assumeyes` on `dnf`) tells the package manager to assume affirmative answers so installs do not block on prompts. That suits scripts and unattended installs, but you do not get a last chance to review dependency changes—use it only when you accept that tradeoff.

**`percona-release`** — The `setup` command documents **`-y`** for non-interactive repository configuration, for example:

```{.bash data-prompt="$"}
sudo percona-release setup -y {{pkg}} --scheme https
```

If you use `enable` or `enable-only` instead, see `sudo percona-release --help` and the [Percona Software Repositories documentation](https://docs.percona.com/percona-software-repositories/percona-release.html) for flags your version supports.

**Debian and Ubuntu (`apt`)** — Add `-y` to each `sudo apt install` (or `sudo apt-get install`) you run, for example `sudo apt install -y curl` and `sudo apt install -y percona-server-server`.

To **disable telemetry** during an unattended server install, set `PERCONA_TELEMETRY_DISABLE=1` on the same line (see [Telemetry](telemetry.md) for details):

```{.bash data-prompt="$"}
sudo PERCONA_TELEMETRY_DISABLE=1 apt install -y percona-server-server
```

**RPM-based systems (`dnf` / `yum`)** — Add `-y` (or `yes`) to install commands as supported by your tool. Example with telemetry disabled:

```{.bash data-prompt="$"}
sudo PERCONA_TELEMETRY_DISABLE=1 dnf install -y percona-server-server
```

Use `yum` instead of `dnf` where that is the supported tool on your OS.
