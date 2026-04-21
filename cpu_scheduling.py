def get_input(prompt, cast=int, validate=None, err_msg="Invalid input."):
    while True:
        try:
            val = cast(input(prompt))
            if validate and not validate(val):
                print(err_msg)
            else:
                return val
        except ValueError:
            print("Please enter a valid number.")


def get_list_input(prompt, n, cast=int, validate=None, err_msg="Invalid value."):
    while True:
        try:
            values = list(map(cast, input(prompt).split()))
            if len(values) != n:
                print(f"Expected {n} values, got {len(values)}. Try again.")
                continue
            if validate:
                invalid = [v for v in values if not validate(v)]
                if invalid:
                    print(err_msg)
                    continue
            return values
        except ValueError:
            print("Please enter valid numbers separated by spaces.")


def print_results(algo_name, processes, ct, bt, at, pr=None):
    tat = [ct[i] - at[i] for i in range(len(processes))]
    wt  = [tat[i] - bt[i] for i in range(len(processes))]

    avg_wt  = sum(wt)  / len(wt)
    avg_tat = sum(tat) / len(tat)

    print(f"\n{'─'*55}")
    print(f"  {algo_name}")
    print(f"{'─'*55}")

    header = f"{'Process':<10}{'Arrival':<10}{'Burst':<10}"
    if pr:
        header += f"{'Priority':<10}"
    header += f"{'Completion':<12}{'Waiting':<10}{'Turnaround':<10}"
    print(header)
    print("─" * (55 + (10 if pr else 0)))

    for i, p in enumerate(processes):
        row = f"{p:<10}{at[i]:<10}{bt[i]:<10}"
        if pr:
            row += f"{pr[i]:<10}"
        row += f"{ct[i]:<12}{wt[i]:<10}{tat[i]:<10}"
        print(row)

    print(f"\n  Avg Waiting Time   : {avg_wt:.2f}")
    print(f"  Avg Turnaround Time: {avg_tat:.2f}")


def fcfs(processes, at, bt):
    n = len(processes)
    order = sorted(range(n), key=lambda i: at[i])
    ct = [0] * n
    time = 0

    for i in order:
        time = max(time, at[i])
        time += bt[i]
        ct[i] = time

    print_results("FCFS (First Come First Serve)", processes, ct, bt, at)


def sjf_non_preemptive(processes, at, bt):
    n = len(processes)
    ct = [0] * n
    done = [False] * n
    time = 0

    for _ in range(n):
        available = [i for i in range(n) if at[i] <= time and not done[i]]
        if not available:
            time = min(at[i] for i in range(n) if not done[i])
            available = [i for i in range(n) if at[i] <= time and not done[i]]

        idx = min(available, key=lambda i: bt[i])
        time += bt[idx]
        ct[idx] = time
        done[idx] = True

    print_results("SJF Non-Preemptive (Shortest Job First)", processes, ct, bt, at)


def srtf(processes, at, bt):
    n = len(processes)
    remaining = bt[:]
    ct = [0] * n
    done = 0
    time = 0
    total_bt = sum(bt)

    while done < n:
        available = [i for i in range(n) if at[i] <= time and remaining[i] > 0]
        if not available:
            time += 1
            continue

        idx = min(available, key=lambda i: remaining[i])
        remaining[idx] -= 1
        time += 1

        if remaining[idx] == 0:
            ct[idx] = time
            done += 1

    print_results("SRTF Preemptive (Shortest Remaining Time First)", processes, ct, bt, at)


def priority_non_preemptive(processes, at, bt, pr):
    n = len(processes)
    ct = [0] * n
    done = [False] * n
    time = 0

    for _ in range(n):
        available = [i for i in range(n) if at[i] <= time and not done[i]]
        if not available:
            time = min(at[i] for i in range(n) if not done[i])
            available = [i for i in range(n) if at[i] <= time and not done[i]]

        idx = min(available, key=lambda i: pr[i])
        time += bt[idx]
        ct[idx] = time
        done[idx] = True

    print_results("Priority Non-Preemptive (lower number = higher priority)", processes, ct, bt, at, pr)


def round_robin(processes, at, bt, tq):
    n = len(processes)
    remaining = bt[:]
    ct = [0] * n
    time = 0
    queue = []
    added = [False] * n

    # Seed queue with processes that arrive at or before time 0
    first_arrival = min(at)
    for i in range(n):
        if at[i] <= first_arrival:
            queue.append(i)
            added[i] = True
    time = first_arrival

    while queue:
        idx = queue.pop(0)
        exec_time = min(tq, remaining[idx])
        time += exec_time
        remaining[idx] -= exec_time

        # Enqueue newly arrived processes
        for i in range(n):
            if not added[i] and at[i] <= time:
                queue.append(i)
                added[i] = True

        if remaining[idx] == 0:
            ct[idx] = time
        else:
            queue.append(idx)

    print_results("Round Robin", processes, ct, bt, at)


# ─────────────────────── MAIN ───────────────────────

print("\n╔══════════════════════════════════════╗")
print("║     CPU Scheduling Simulator         ║")
print("╚══════════════════════════════════════╝\n")

n = get_input("Enter number of processes: ", validate=lambda x: x >= 1,
              err_msg="Must have at least 1 process.")

processes = [f"P{i+1}" for i in range(n)]

at = get_list_input(f"Enter {n} arrival time(s): ", n,
                    validate=lambda x: x >= 0, err_msg="Arrival times must be >= 0.")

bt = get_list_input(f"Enter {n} burst time(s): ", n,
                    validate=lambda x: x >= 1, err_msg="Burst times must be >= 1.")

pr = get_list_input(f"Enter {n} priority value(s) (lower = higher priority): ", n,
                    validate=lambda x: x >= 1, err_msg="Priority must be >= 1.")

tq = get_input("Enter time quantum for Round Robin: ",
               validate=lambda x: x >= 1, err_msg="Time quantum must be >= 1.")

fcfs(processes, at, bt)
sjf_non_preemptive(processes, at, bt)
srtf(processes, at, bt)
priority_non_preemptive(processes, at, bt, pr)
round_robin(processes, at, bt, tq)
