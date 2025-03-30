from flask import Flask, request, jsonify
from flask_cors import CORS
from copy import deepcopy

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Solver function
def callPuzzle(init, goal, row, col, depth, path):
    if init == goal:
        return 1, path
    if depth ==11:
        return 0, []
    if col != 0:
        init[row][col], init[row][col - 1] = init[row][col - 1], init[row][col]
        found, new_path = callPuzzle(init, goal, row, col - 1, depth + 1, path + ["Left"])
        if found:
            return 1, new_path
        init[row][col], init[row][col - 1] = init[row][col - 1], init[row][col]
    if row != 0:
        init[row][col], init[row - 1][col] = init[row - 1][col], init[row][col]
        found, new_path = callPuzzle(init, goal, row - 1, col, depth + 1, path + ["Up"])
        if found:
            return 1, new_path
        init[row][col], init[row - 1][col] = init[row - 1][col], init[row][col]
    if col != 2:
        init[row][col], init[row][col + 1] = init[row][col + 1], init[row][col]
        found, new_path = callPuzzle(init, goal, row, col + 1, depth + 1, path + ["Right"])
        if found:
            return 1, new_path
        init[row][col], init[row][col + 1] = init[row][col + 1], init[row][col]
    if row != 2:
        init[row][col], init[row + 1][col] = init[row + 1][col], init[row][col]
        found, new_path = callPuzzle(init, goal, row + 1, col, depth + 1, path + ["Down"])
        if found:
            return 1, new_path
        init[row][col], init[row + 1][col] = init[row + 1][col], init[row][col]
    return 0, []

@app.route('/solve', methods=['POST'])
def solve_puzzle():
    data = request.json
    initial = data.get('initial')
    goal = data.get('goal')
    row, col = data.get('row'), data.get('col')
    success, path = callPuzzle(deepcopy(initial), goal, row, col, 0, [])
    return jsonify({
        "success": success,
        "path": path
    })

if __name__ == '__main__':
    app.run(debug=True)
