# Sentinel

A lightweight, on-demand process investigation tool for Linux, built using eBPF/bpftrace. Sentinel traces a target process and every process it spawns, capturing file access, network activity, and syscall behavior in real time — then narrates the findings in plain English.

## Why I Built This

I wanted to genuinely understand kernel-level observability rather than just use pre-built security tools. Sentinel was built from scratch, layer by layer, starting from a single kernel probe and growing into a working investigative tool — the same category of technology (eBPF) that powers production tools like Falco and Tetragon.

## What It Does

- Traces a target process **and every child process it spawns**, automatically, using live parent-child relationship tracking
- Logs every process spawn, program execution, file open, and network connection attempt
- Timestamps every event
- Produces an automatic case summary at the end of each session (processes spawned, files opened, connections attempted, syscall breakdown)
- Includes a Python narrator that converts raw logs into a plain-English investigative report

## How It Works

Sentinel is built on **bpftrace**, a scripting front-end for eBPF — a Linux kernel technology that allows safe, sandboxed programs to run inside the kernel itself. Sentinel attaches to kernel tracepoints (`sched_process_fork`, `sched_process_exec`, `sys_enter_openat`, `sys_enter_connect`, `raw_syscalls:sys_enter`) and maintains a live, self-growing map of every process descended from the target — meaning it correctly attributes activity even to child processes it was never explicitly told to watch.

## Requirements

- Linux with a modern kernel (BTF support recommended — no separate kernel headers needed)
- `bpftrace` installed (`sudo apt install bpftrace` on Debian/Kali/Ubuntu)
- Python 3
- Root privileges (required to load eBPF programs)

## Usage

**1. Find your target process's PID:**
```bash
echo $$          # if targeting your  current shell

**2. Run Sentinel, logging to a timestamped file:**
```bash
sudo bpftrace probe.bt <PID> > sentinel_$(date +%Y%m%d_%H%M%S).log
```

**3. Trigger/observe activity, then stop with Ctrl+C.**

**4. Generate a plain-English report:**
```bash
python3 narrator.py sentinel_<timestamp>.log
```

## Example Output
<img width="796" height="453" alt="image" src="https://github.com/user-attachments/assets/ce416173-fa95-479f-ab00-469ecd17aba9" />
