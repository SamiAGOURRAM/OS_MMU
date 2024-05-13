from flask import Flask, render_template, request, redirect, url_for
from memory_manager import MemoryManager  # Ensure this module is in your path
from memory_block import *
from process import *
from memory_manager import *
from flask import jsonify

app = Flask(__name__)
mm = None



@app.route('/memory-data')
def memory_data():
    memory_blocks = [{'base': block.base, 'size': block.size, 'process_id': block.process_id} for block in mm.memory_blocks]
    return jsonify(memory_blocks=memory_blocks, total_memory=mm.total_memory)


@app.route('/', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        total_memory = int(request.form['total_memory'])
        strategy_id = int(request.form['strategy_id'])
        global mm
        mm = MemoryManager(total_memory, strategy_id)
        return redirect(url_for('manage_memory'))
    return render_template('setup.html')

@app.route('/manage', methods=['GET', 'POST'])
def manage_memory():
    if not mm:
        return redirect(url_for('setup'))
    message = None
    if request.method == 'POST':
        try:
            if 'create' in request.form:
                size = int(request.form['size'])
                process = mm.allocate_memory(size)
                message = f"Process {process.pid} created with size {size} KB" if process else "Error: Not enough memory"
            elif 'delete' in request.form:
                pid = int(request.form['pid'].strip())
                if pid:
                    message = mm.free_memory(pid)
                else:
                    message = "Error: Process ID is required."
            elif 'convert' in request.form:
                pid = int(request.form['pid'].strip())
                va = int(request.form['virtual_address'].strip())
                if pid and va:
                    result = mm.convert_virtual_to_physical(pid, va)
                    message = result
                else:
                    message = "Error: Both Process ID and Virtual Address are required."
        except ValueError:
            message = "Error: Please provide valid integers for Process ID and/or sizes."
    return render_template('manage.html', message=message, memory_map=mm.memory_blocks)



@app.route('/add-process', methods=['POST'])
def add_process():
    if mm:
        try:
            size = int(request.form['size'])
            process = mm.allocate_memory(size)
            if process:
                return jsonify({'message': f"Process {process.pid} created with size {size} KB"})
            else:
                return jsonify({'error': "Not enough memory"})
        except ValueError:
            return jsonify({'error': "Invalid size"})
    else:
        return jsonify({'error': "Memory manager not initialized"})


@app.route('/delete-process', methods=['POST'])
def delete_process():
    if mm:
        try:
            pid = int(request.form['pid'].strip())
            if pid:
                message = mm.free_memory(pid)
                return jsonify({'message': message})
            else:
                return jsonify({'error': "Process ID is required."})
        except ValueError:
            return jsonify({'error': "Invalid Process ID"})
    else:
        return jsonify({'error': "Memory manager not initialized"})
    

@app.route('/convert-address', methods=['POST'])
def convert_address():
    if mm:
        try:
            pid = int(request.form['pid'].strip())
            va = int(request.form['virtual_address'].strip())
            if pid and va:
                result = mm.convert_virtual_to_physical(pid, va)
                return jsonify({'message': result})
            else:
                return jsonify({'error': "Both Process ID and Virtual Address are required."})
        except ValueError:
            return jsonify({'error': "Invalid Process ID or Virtual Address"})
    else:
        return jsonify({'error': "Memory manager not initialized"})
if __name__ == '__main__':
    app.run(debug=True)
