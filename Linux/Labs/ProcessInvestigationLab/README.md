
# Process & Service Investigation Lab

Linux administration lab focused on process monitoring, resource analysis, systemd services, logs and process signals on Ubuntu.

## Objective

Investigate a potentially slow Linux system before taking action on its processes or services.

The lab follows a simple troubleshooting methodology:

```text
System slowdown
      ↓
Process identification
      ↓
CPU / Memory analysis
      ↓
PID / PPID
      ↓
Process hierarchy
      ↓
systemd service
      ↓
Logs
      ↓
Decision / Action
```

## Topics Covered

- Linux process monitoring
- PID and PPID
- Parent/child process relationships
- CPU and memory usage
- Process states
- Bash background jobs
- systemd services
- Control Groups (cgroups)
- systemd journal investigation
- Linux signals
- Safe process termination

## Commands Used

### Process inspection

```bash
ps
ps aux
top
```

Sort processes by CPU or memory usage:

```bash
ps aux --sort=-%cpu | head
ps aux --sort=-%mem | head
```

### Process search

```bash
pgrep firefox
pgrep -a firefox
pidof firefox
```

### Process hierarchy

```bash
ps -p PID -o user,pid,ppid,stat,%cpu,%mem,cmd
pstree -p
```

### systemd services

```bash
systemctl status mysql.service
systemctl show mysql.service -p KillSignal -p Restart
```

### Logs

```bash
journalctl -u mysql.service
journalctl -u mysql.service -n 20
journalctl -u mysql.service -f
```

### Process signals

```bash
kill PID
kill -STOP PID
kill -CONT PID
```

## Practical Investigation

During the lab, running processes were analyzed according to their CPU and memory consumption.

A MySQL process was then connected to its systemd service:

```text
mysql.service
      ↓
Main PID
      ↓
mysqld
      ↓
CGroup
      ↓
CPU / Memory / Tasks
```

The service journal was inspected before taking any action.

No errors or warnings were found in the inspected MySQL journal entries.

## Process Hierarchy

PID and PPID were used to trace a process through its parents.

Example observed during the lab:

```text
systemd
   ↓
systemd --user
   ↓
gnome-shell
   ↓
firefox
   ↓
Firefox child process
```

`pstree` was then used to visualize process relationships directly.

## Process States and Signals

A temporary process was created for testing:

```bash
sleep 1000 &
```

Its state was manipulated using Linux signals:

```text
S — Sleeping
      ↓
SIGSTOP
      ↓
T — Stopped
      ↓
SIGCONT
      ↓
S — Sleeping
      ↓
SIGTERM
      ↓
Terminated
```

The lab also introduced the `Z` zombie state and why a zombie cannot simply be killed like a running process.

## Key Takeaway

A process consuming resources should not automatically be killed.

A safer administration workflow is:

```text
Observe
   ↓
Identify
   ↓
Investigate
   ↓
Check service and logs
   ↓
Take action if necessary
```

When a process belongs to a systemd service, managing the service through `systemctl` is generally preferable to directly killing its PID.

## Environment

- Ubuntu Linux
- Bash
- systemd
- procps