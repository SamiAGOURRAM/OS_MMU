from memory_block import *
from process import *
from memory_manager import *
import sys

def run_mmu_cli():
    if len(sys.argv) != 3:
        print("Usage: python mmu.py <total_memory_kb> <strategy_id>")
        print("Strategies: 1 for First Fit, 2 for Next Fit, 3 for Best Fit, 4 for Worst Fit")
        return

    try:
        total_memory = int(sys.argv[1])
        strategy_id = int(sys.argv[2])
    except ValueError:
        print("Error: Please provide valid integers for memory size and strategy ID.")
        return

    mm = MemoryManager(total_memory, strategy_id)


    while True:
        try:
            command = input("> ").strip()
            if command.startswith("cr "):
                try:
                    size = int(command.split()[1])
                    print(size)
                    process = mm.allocate_memory(size)
                    if process:
                        print(f"Process {process.pid} created with size {size} KB")
                    else:
                        print("Error: Not enough memory")
                except ValueError:
                    print("Error: Invalid size input.")
            elif command.startswith("dl "):
                try:
                    pid = int(command.split()[1])
                    message = mm.free_memory(pid)
                    print(message)
                except ValueError:
                    print("Error: Invalid process ID.")
            elif command.startswith("cv "):
                parts = command.split()
                try:
                    pid = int(parts[1])
                    virtual_address = int(parts[2])
                    result = mm.convert_virtual_to_physical(pid, virtual_address)
                    print(result)
                except ValueError:
                    print("Error: Invalid input for process ID or virtual address.")
            elif command == "pm":
                mm.print_memory_map()
            elif command == "exit":
                break
            else:
                print("Unknown command")
        except Exception as e:
            print(f"An error occurred: {str(e)}")




