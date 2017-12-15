from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository
from gitrepo import set_repo, get_commits

app = Flask(__name__)


# give work to any worker who access the url
@app.route('/work' , methods=['GET'])
def give_work():
    repo = set_repo()
    commits = get_commits(repo)
    global next_task
    if next_task < len(commits):
        commit_hash = commits[next_task]
        next_task += 1
        return jsonify({'commit': str(commit_hash.id), 'id': next_task})
    else:
        return "No Work"

# send Execution time
@app.route('/executiontime' , methods=['POST'])
def execution_time():
    start_time = request.json
    end_time = time() - int(start_time['start_time'])
    return jsonify({'executiontime': end_time})

# store results that are sent to this url
@app.route('/results', methods=['POST','GET'])
def store_result():
    global executiontime_list, execution_time, result
    executiontime_list = []
    if request.method == 'POST':
        result = request.json
        executiontime_list = result['executiontime']
        execution_time = sum(executiontime_list)#/len(executiontime_list)
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})
    else:
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['GET'])
def shutdown():
    shutdown_server()
    return jsonify({'message' : 'Server shutting down...'})

if __name__ == '__main__':
    next_task = 0
    global result_list
    result_list = []
    app.run(threaded=True, debug=True)