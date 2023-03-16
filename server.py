# Welcome to PyShine

# This code is for the server 
# Lets import the libraries
import socket, cv2, pickle,struct

# Socket Create
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)		#configures client socket with TCP protocol
host_name  = socket.gethostname()
host_ip = '10.42.0.1'			#host IPV4 Adress
print('HOST IP:',host_ip)
port = 9999						#Port to host server
socket_address = (host_ip,port)

# Socket Bind
server_socket.bind(socket_address)		#bind server with IP and Port

# Socket Listen
server_socket.listen(5)					#allows max connection of 5 at a time
print("LISTENING AT:",socket_address)

# Socket Accept
while True:
	client_socket,addr = server_socket.accept()			#wait untill got any client request
	print('GOT CONNECTION FROM:',addr)
	if client_socket:
		vid = cv2.VideoCapture(0)						#configures default camera to capture frames
		vid.set(cv2.CAP_PROP_FRAME_WIDTH,80)			#configures resolution of camera capture
		vid.set(cv2.CAP_PROP_FRAME_HEIGHT,100)
		while(vid.isOpened()):
			xyz,frame = vid.read()						#returns frames
			#frame = cv2.resize(tframe, (480,480), fx=100, fy=100,interpolation=cv2.INTER_LANCZOS4)
			a = pickle.dumps(frame)						#convert frames into serial data
			message = struct.pack("Q",len(a))+a			#genrates message to send with frame size
			client_socket.sendall(message)				#sends message to client
			
			#cv2.imshow('TRANSMITTING VIDEO',frame)
			
			if cv2.waitKey(1) & 0xFF == ord('q'): 
			    client_socket.close()					#close client socket when key 'Q' pressed
