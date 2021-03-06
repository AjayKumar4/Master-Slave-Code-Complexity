from radon.metrics import mi_visit
from radon.complexity import cc_visit, cc_rank
from pygit2 import Repository, clone_repository
import requests, json
from time import time
from gitrepo import set_repo, get_commits



# computes the complexity of all .py files in the given list
def compute_complexity(source):
    result =[]
    # get cc blocks
    blocks = cc_visit(source)
    # get MI score
    #mi = mi_visit(source, True)
    for func in blocks:
        result.append(func.name+"- CC Rank:"+cc_rank(func.complexity))
    return result

# walks through the tree of the given repo and stores any .py files in a list
def get_data(tree, repo):
    sources = []
    for entry in tree:
        if ".py" in entry.name:
            sources.append(entry)
        if "." not in entry.name:
           if entry.type == 'tree':
                new_tree = repo.get(entry.id)
                sources += (get_data(new_tree, repo))
    return sources

# decodes the files stored in the list
def extract_files(sources):
    files = []
    for source in sources:
        files.append(repo[source.id].data.decode("utf-8"))
    return files


# ask for work from the given iurl
def get_work(repo):
    post = requests.post('http://127.0.0.1:5000/executiontime', json={'start_time': time()})
    response = requests.get('http://127.0.0.1:5000/work', params={'key': 'value'})
    while response.status_code == 200:
        response.encoding = 'utf-8'
        json_file = response.json()
        post.encoding = 'utf-8'
        post_file = post.json()
        executiontime = post_file['executiontime']
        id = json_file['id']
        tree = repo.get(json_file['commit']).tree
        sources = get_data(tree, repo)
        files = extract_files(sources)
        return files, id, executiontime

# compute the complexity of each file in the given list
def do_work(work):
    results = []
    for file in work:
        try:
            results.append(compute_complexity(file))
        except:
            results.append('')
    return results

# post results to the url
def send_results(result):
    requests.post('http://127.0.0.1:5000/results', json=result,  params={'key': 'value'})
    response = requests.get('http://127.0.0.1:5000/results',  params={'key': 'value'})
    return response

if __name__ == '__main__':
    bool = True
    executiontime_list = []
    result_list = []
    id = 0
    while bool: #run until work is finished
        repo = set_repo()
        commits = get_commits(repo)
        try:
            #while id < len(commits):
            work, id, executiontime = get_work(repo)
            print(id)
            result = do_work(work)
            result_list.append(result)
            executiontime_list.append(executiontime)
        except:
            bool = False
            print("Process Terminated")
    report = {'Result': result_list, 'executiontime': executiontime_list}
    response = send_results(report)
    message = response.json()
    print("complexity_score", message['complexity_score'])
    print("execution_time", message['execution_time'])
    #requests.get('http://127.0.0.1:5000/shutdown', params={'key': 'value'})
    # Run URL "http://127.0.0.1:5000/shutdown" in any browser to stop Flask APP


