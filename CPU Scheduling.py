# -------- CPU Scheduling Algorithms --------

def sort_processes(at, bt, pr):
    processes = sorted(zip(at, bt, pr), key=lambda x: x[0])
    at, bt, pr = zip(*processes)
    return list(at), list(bt), list(pr)


def print_gantt(order, times):
    print("Gantt Chart:")
    for p in order:
        print(f"| P{p} ", end="")
    print("|")

    print(times)


# -------- FCFS --------
def fcfs(n, at, bt):
    ct = [0]*n
    wt = [0]*n
    tat = [0]*n

    order = []
    times = [0]

    ct[0] = at[0] + bt[0]
    order.append(0)
    times.append(ct[0])

    for i in range(1, n):
        ct[i] = max(ct[i-1], at[i]) + bt[i]
        order.append(i)
        times.append(ct[i])

    for i in range(n):
        tat[i] = ct[i] - at[i]
        wt[i] = tat[i] - bt[i]

    print("\n--- FCFS ---")
    print("CT:", ct)
    print("WT:", wt)
    print("TAT:", tat)
    print_gantt(order, times)


# -------- SJF NON PREEMPTIVE --------
def sjf_non_preemptive(n, at, bt):
    completed = [False]*n
    ct = [0]*n
    time = 0

    order = []
    times = [0]

    for _ in range(n):
        idx = -1
        min_bt = float('inf')

        for i in range(n):
            if at[i] <= time and not completed[i] and bt[i] < min_bt:
                min_bt = bt[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        time += bt[idx]
        ct[idx] = time
        completed[idx] = True

        order.append(idx)
        times.append(time)

    tat = [ct[i] - at[i] for i in range(n)]
    wt = [tat[i] - bt[i] for i in range(n)]

    print("\n--- SJF Non-Preemptive ---")
    print("CT:", ct)
    print("WT:", wt)
    print("TAT:", tat)
    print_gantt(order, times)


# -------- SJF PREEMPTIVE (SRTF) --------
def sjf_preemptive(n, at, bt):
    rt = bt[:]
    complete = 0
    time = 0
    ct = [0]*n

    order = []
    times = [0]

    last = -1

    while complete != n:
        idx = -1
        min_rt = float('inf')

        for i in range(n):
            if at[i] <= time and rt[i] > 0 and rt[i] < min_rt:
                min_rt = rt[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        if last != idx:
            order.append(idx)
            times.append(time)
            last = idx

        rt[idx] -= 1
        time += 1

        if rt[idx] == 0:
            complete += 1
            ct[idx] = time

    times.append(time)

    tat = [ct[i] - at[i] for i in range(n)]
    wt = [tat[i] - bt[i] for i in range(n)]

    print("\n--- SJF Preemptive (SRTF) ---")
    print("CT:", ct)
    print("WT:", wt)
    print("TAT:", tat)
    print_gantt(order, times)


# -------- PRIORITY NON PREEMPTIVE --------
def priority_non_preemptive(n, at, bt, pr):
    completed = [False]*n
    ct = [0]*n
    time = 0

    order = []
    times = [0]

    for _ in range(n):
        idx = -1
        highest = float('inf')

        for i in range(n):
            if at[i] <= time and not completed[i] and pr[i] < highest:
                highest = pr[i]
                idx = i

        if idx == -1:
            time += 1
            continue

        time += bt[idx]
        ct[idx] = time
        completed[idx] = True

        order.append(idx)
        times.append(time)

    tat = [ct[i] - at[i] for i in range(n)]
    wt = [tat[i] - bt[i] for i in range(n)]

    print("\n--- Priority Non-Preemptive ---")
    print("CT:", ct)
    print("WT:", wt)
    print("TAT:", tat)
    print_gantt(order, times)


# -------- ROUND ROBIN --------
def round_robin(n, at, bt, tq):
    rt = bt[:]
    ct = [0]*n
    time = 0
    queue = []
    visited = [False]*n

    order = []
    times = [0]

    queue.append(0)
    visited[0] = True

    while queue:
        i = queue.pop(0)

        order.append(i)
        times.append(time)

        if rt[i] > tq:
            time += tq
            rt[i] -= tq
        else:
            time += rt[i]
            ct[i] = time
            rt[i] = 0

        for j in range(n):
            if at[j] <= time and not visited[j]:
                queue.append(j)
                visited[j] = True

        if rt[i] > 0:
            queue.append(i)

    times.append(time)

    tat = [ct[i] - at[i] for i in range(n)]
    wt = [tat[i] - bt[i] for i in range(n)]

    print("\n--- Round Robin ---")
    print("CT:", ct)
    print("WT:", wt)
    print("TAT:", tat)
    print_gantt(order, times)


# -------- MAIN --------
n = int(input("Enter number of processes: "))

at = list(map(int, input("Enter Arrival Times: ").split()))
bt = list(map(int, input("Enter Burst Times: ").split()))
pr = list(map(int, input("Enter Priority: ").split()))
tq = int(input("Enter Time Quantum: "))

at, bt, pr = sort_processes(at, bt, pr)

fcfs(n, at, bt)
sjf_non_preemptive(n, at, bt)
sjf_preemptive(n, at, bt)
priority_non_preemptive(n, at, bt, pr)
round_robin(n, at, bt, tq)
