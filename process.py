class Process:
    next_pid = 1  # Class variable to keep track of the next process ID

    def __init__(self, memory_required):
        self.pid = Process.next_pid
        self.memory_required = memory_required
        Process.next_pid += 1
