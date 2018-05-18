# stream2msg

Basic socket wrapper for converting byte stream into messages for python sockets.

Install using pip:

> pip install stream2msg

Initialize sockets: 
```python
from stream2msg import SocketWrapper

# Server. Waits for connection.
server = SocketWrapper(is_listener=True, socket_info=('localhost', 5000))

# Client. Assumes server is already running, will raise exception if connection fails.
client = SocketWrapper(is_listener=False, socket_info=('localhost', 5000))
```
  
Sending and receiving messages:  
```python
from stream2msg import SocketWrapper

# Client sends message.
client.send_data('hello world')

# Server gets message.
print server.get_message()
```
  
Note that messages are buffered, i.e. the most recent message is NOT the one that will appear next. For example:
```python

# Client sends message.
client.send_data('hello world')
client.send_data('hello world2')
client.send_data('hello world3')

# Server gets message.
print server.get_message()  # Will print ['', 'hello world'].
print server.get_message()  # Will print ['', 'hello world2'].
```
  
Allows sending of metadata in addition to string messages. Metadata can be sent as an array, and is returned as the first LEN-1 elements of the received message. The string data is always the LEN-1 index of the message.  

```python
# Client sends message with metadata.
client.send_data('hello world', ['metadata1', 'metadata2'])

# Server gets message with metadata.
print server.get_message()  # Will print ['metadata1', 'metadata2', 'hello world'].
```
  
Can be combined with cPickle, json, or other data-to-string converters to easily send any object of choice.  
```python
import cPickle as pickle

x = {'object': 'data'}

# Client sends message with metadata.
client.send_data(pickle.dumps(x))

# Server gets message with metadata.
message = server.get_message()
print pickle.loads(message[-1])  # Will print 'hello world'.
```

See ExampleClient and ExampleServer for basic echo server implementation.
