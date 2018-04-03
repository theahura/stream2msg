# socket-wrapper
Basic socket wrapper for python.  
Allows sending of metadata in addition to simple string messages. Metadata can be sent as an array, and is returned as the first LEN-1 elements of the received message. The string data is always the LEN-1 index of the message. 
