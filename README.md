# Master-Slave-Code-Complexity

calculating code complexity using Python Master-Slave distributed system 

Prerequisite to Run the code in Python 3.6+:
radon (API for calculating code complexity)

flask (API for creating RESTful web application)

requests (handle GET, POST requests over HTTP)

pygit2 (API for pulling git repos and walking through commits)

To run Master-Slave-Code-Complexity code, start the Master, flask app starts and create the server on a localhost network with port 5000. Once the server is running start Slave nodes, which will request work from the Master. The Master and Slave code can be executed using an IDE such as PyCharm, or by performing in the terminal (ALWAYS start a Master code first and Then Slave). Slave code can be executed multiple time in the different terminal.

To execute from the command line run these commands:

python ./Master.py

python ./Slave.py

Once the Master has distributed the work, It is needs to be restarted in order to give any new Slave additional work, as such each time the Slave(s) complete their processes, the time taken for each task by slave to complete the task was logged by the code and POST in Browser using URL(http://127.0.0.1:5000/results) along with List of cyclomatic complexities Results
for each .py file in the commit in Provided Git Repository

![alt text](https://github.com/AjayKumar4/Master-Slave-Code-Complexity/blob/master/execution_graph.png)

The above graph indicating computation time for the given No of workers(Slave) was made before finalising them and fixing the POST request of sending the results back to the Master. Although as the POST request would take an equal amount of time for each slave, it would only scale the results and not alter their ratios.
To stop Flask APP Server use below URL in any Browser
http://127.0.0.1:5000/shutdown

