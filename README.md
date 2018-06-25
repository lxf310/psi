# Stream online viewer
The goal of this task is to display a stream in a web client.

# Instructions
- Install the needed dependencies
```bash
conda install -c conda-forge flask-socketio
```
- Services introduction
   - **stream\_online\/start\_server.py** is the entry point for the web server.
   - **stream\_online\/start\_stream.py** is the entry point for the stream server. 
   - Example:
```bash
python start_server.py -o 8888 -d 1
python start_stream.py -o 8888 -d 0.5
```
- By default, user can access this web application via **http://127.0.0.1:5000**

# Solution description
- Chosen technology and library
   - Backend: [flask-socketio](http://flask-socketio.readthedocs.io/en/latest/)
   - Frontend: jquery, [socket.io](https://socket.io/docs/client-api)
- Basic ideas
   - The server pushes data to the connected clients. 
      - When a new stream message comes, the server will call *socketio.emit()* method to broadcast a named event to all connected clients. A message of server Response contains beam energy, repetition rate and image data in base64 encoded string format. 
      - By default, 60 messages will be processed and emitted to the clients every minute.
   - The client listens to the specific event coming from the server and then update the HTML page accordingly.
      - A client will connect to a specific channel of the server side and then listen to the specific event as soon as the HTML page is ready. When the event is caught, the client will take use of jquery selectors to update the relevant HTML elements. The connection will terminate automatically when the client window is closed.
- Drawbacks
   - All data are not verified and it may lead to fail to display the stream.
   - There is only one thread serving all the connected clients, so if the number of the connected clients is really big, the performance could be bad.
- Further plan for improvement
   - Taking use of message queue
