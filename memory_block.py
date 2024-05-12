class MemoryBlock:
    def __init__(self, base, size, process_id=None):
        self.base = base
        self.size = size
        self.process_id = process_id  # None if the block is free
