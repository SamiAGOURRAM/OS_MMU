from memory_block import *
from process import *


class MemoryManager:
    def __init__(self, total_memory, strategy_id):
        self.total_memory = total_memory
        strategies = {1: 'first_fit', 2: 'next_fit', 3: 'best_fit', 4: 'worst_fit'}
        self.strategy = strategies[strategy_id]
        self.memory_blocks = [MemoryBlock(0, total_memory, None)]
        self.last_allocated_index = 0

    def allocate_memory(self, memory_required):
        if self.strategy == 'first_fit':
            return self.first_fit(memory_required)
        elif self.strategy == 'next_fit':
            return self.next_fit(memory_required)
        elif self.strategy == 'best_fit':
            return self.best_fit(memory_required)
        elif self.strategy == 'worst_fit':
            return self.worst_fit(memory_required)
        
    def convert_virtual_to_physical(self, pid, virtual_address):
        for block in self.memory_blocks:
            if block.process_id == pid:
                if 0 <= virtual_address < block.size:
                    physical_address = block.base + virtual_address
                    return f"Physical Address: {physical_address}"
                else:
                    return "Error: Virtual address is out of the process's address space"
        return "Error: No process found with the given ID"

    def first_fit(self, memory_required):
        for index, block in enumerate(self.memory_blocks):
            if block.process_id is None and block.size >= memory_required:
                return self.allocate_block(index, memory_required)
        return None

    def next_fit(self, memory_required):
        # Start from last allocated block
        n = len(self.memory_blocks)
        for i in range(n):
            index = (self.last_allocated_index + i) % n
            block = self.memory_blocks[index]
            if block.process_id is None and block.size >= memory_required:
                return self.allocate_block(index, memory_required)
        return None

    def best_fit(self, memory_required):
        best_index = None
        min_size = float('inf')

        # Loop through all memory blocks to find the best fit
        for index, block in enumerate(self.memory_blocks):
            if block.process_id is None and block.size >= memory_required:
                if block.size < min_size:
                    min_size = block.size
                    best_index = index

        # If a suitable block is found, allocate the memory
        if best_index is not None:
            return self.allocate_block(best_index, memory_required)
        return None


    def worst_fit(self, memory_required):
        worst_index = None
        max_size = 0
        for index, block in enumerate(self.memory_blocks):
            if block.process_id is None and block.size >= memory_required and block.size > max_size:
                max_size = block.size
                worst_index = index
        if worst_index is not None:
            return self.allocate_block(worst_index, memory_required)
        return None
    
    def allocate_block(self, index, memory_required):
        block = self.memory_blocks[index]
        # Check if the block size is exactly what is required
        if block.size == memory_required:
            # Simply allocate this block to the new process
            self.memory_blocks[index].process_id = Process.next_pid
        else:
            # Split the block
            new_block = MemoryBlock(block.base + memory_required, block.size - memory_required, None)
            self.memory_blocks[index] = MemoryBlock(block.base, memory_required, Process.next_pid)
            self.memory_blocks.insert(index + 1, new_block)
        self.last_allocated_index=index
        return Process(memory_required)


    def free_memory(self, pid):
        for i, block in enumerate(self.memory_blocks):
            if block.process_id == pid:
                block.process_id = None  # Mark the block as free
                self.merge_free_blocks()
                return "Memory freed for Process ID {}".format(pid)
        return "No process found with ID {}".format(pid)

    def merge_free_blocks(self):
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]
            if current.process_id is None and next_block.process_id is None:
                # Merge current and next block
                current.size += next_block.size
                self.memory_blocks.pop(i + 1)  # Remove next block
            else:
                i += 1

    def print_memory_map(self):
        for block in self.memory_blocks:
            status = 'Free' if block.process_id is None else f'Allocated to Process {block.process_id}'
            print(f'Base: {block.base}, Size: {block.size}, Status: {status}')


def run_tests():
    print("Initializing Memory Manager with 10000 KB of memory and Best Fit strategy...")
    mm = MemoryManager(10000, 3)  # Using Best Fit (strategy ID 3)

    print("\nCreating Process 1: 3000 KB")
    mm.allocate_memory(3000)
    print("\nCreating Process 2: 4000 KB")
    mm.allocate_memory(4000)
    print("\nCreating Process 3: 2000 KB")
    mm.allocate_memory(2000)

    print("\nMemory Map after allocations:")
    mm.print_memory_map()

    print("\nDeleting Process 2")
    mm.free_memory(2)  # Assuming process 2 corresponds to the second process created

    print("\nMemory Map after freeing Process 2:")
    mm.print_memory_map()

    print("\nAttempting to allocate 3500 KB (should reuse freed space of 4000 KB)")
    mm.allocate_memory(3500)

    print("\nFinal Memory Map:")
    mm.print_memory_map()

if __name__ == "__main__":
    run_tests()


