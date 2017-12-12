from flask import Flask, request, jsonify
from time import time
from pygit2 import Repository, clone_repository

app = Flask(__name__)

# pulls repo from url and stores clone
def set_repo():
    try:
        repo = Repository('./repo')
    except:
        repo_url = 'https://github.com/rubik/radon.git'#'https://github.com/AjayKumar4/Client-Server.git'
        repo_path = './repo'
        repo = clone_repository(repo_url, repo_path)
    return repo

# walk through commits in the given repo and store in list
def get_commits(repo):
    commits = []
    for commit in repo.walk(repo.head.target):
        commits.append(repo.get(commit.id))
    return commits

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
@app.route('/results', methods=['GET', 'POST'])
def store_result():
    global executiontime_list, execution_time, result
    executiontime_list = []
    if request.method == 'POST':
        result = request.json
        executiontime_list = result['executiontime']
        execution_time = sum(executiontime_list)/len(executiontime_list)
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})
    else :
        return jsonify({'complexity_score': result['Result'], 'execution_time': execution_time})

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route('/shutdown', methods=['POST'])
def shutdown():
    shutdown_server()
    return 'Server shutting down...'

if __name__ == '__main__':
    next_task = 0
    global result_list
    result_list = []
    #app.run(threaded=True, debug=True)
    app.run()
