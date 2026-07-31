import sys
import re

def parse_line(line):
    # Match SPAWN lines
    spawn_match = re.search(r'\[(.*?)\] \[SPAWN\] pid (\d+) spawned child pid (\d+)', line)
    if spawn_match:
        timestamp, parent_pid, child_pid = spawn_match.groups()
        return f"At {timestamp}, process {parent_pid} created a new process, {child_pid}."

    # Match EXEC lines
    exec_match = re.search(r'\[(.*?)\] \[EXEC\] (\S+) \(pid (\d+)\)', line)
    if exec_match:
        timestamp, program, pid = exec_match.groups()
        return f"At {timestamp}, process {pid} started running the program {program}."

    # Match OPEN lines
    open_match = re.search(r'\[(.*?)\] \[OPEN\] (\S+) \(pid (\d+)\) -> (\S+)', line)
    if open_match:
        timestamp, comm, pid, filepath = open_match.groups()
        return f"At {timestamp}, {comm} (pid {pid}) opened the file {filepath}."

    # Match CONNECT lines
    connect_match = re.search(r'\[(.*?)\] \[CONNECT\] (\S+) \(pid (\d+)\)', line)
    if connect_match:
        timestamp, comm, pid = connect_match.groups()
        return f"At {timestamp}, {comm} (pid {pid}) attempted a network connection."

    return None  # line didn't match any known pattern


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 narrator.py <logfile>")
        sys.exit(1)

    filename = sys.argv[1]

    with open(filename, "r") as f:
        lines = f.readlines()

    print(f"=== Sentinel Investigation Report ===\n")

    summary_started = False
    for line in lines:
        if "SENTINEL CASE SUMMARY" in line:
            summary_started = True
            print("\n--- Case Summary ---")
            continue

        if summary_started:
            print(line.strip())
            continue

        sentence = parse_line(line)
        if sentence:
            print(sentence)

if __name__ == "__main__":
    main()