import socket
import signal
import time
import json
import csv
import cv2
import skvideo.io as sk

class Server:
    def __init__(self, port):
        self.host = '10.188.44.145'
        self.port = port
        self.cap = cv2.VideoCapture(0)
        #if you want to read video from file instead, uncomment next line
        # cap = sk.VideoCapture("16_3_5.avi")
        ret, frame = self.cap.read()
        if not ret:
            print "can not get image"
            return
        else:
            print frame.shape
            #store image
            cv2.imwrite("background.jpg", frame);
            self.filename = "background.jpg"

    def activate_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print('Launching HTTP server on ', self.host, ':', self.port)
            self.socket.bind((self.host, self.port))
        except Exception as e:
            print ('Error', e, self.port, '\n')
            return
        print ('Server successfully acquired the socket with port:', self.port)
        self._wait_for_connections()

    #loop function which listens to incoming data until timeout exceeds limit
    def recv_timeout(self, conn, timeout=2):
        #data to return
        total_data = [];
        #we have to make connection non-blocking, otherwise it will be impossible to do anything untill connection is closed
        conn.setblocking(0)
        #piece of data to be received
        data = '';
        begin = time.time()
        while 1:
            if total_data and time.time() - begin > timeout:
                print "no more data\n"
                break
            #if timeout exceeds limit
            elif time.time() - begin > 2 * timeout:
                print "no data at all\n"
                break
            try:
                # print "trying get some more data\n"
                data = conn.recv(8192)
                if data:
                    total_data.append(data)
                    begin = time.time()
                else:
                    time.sleep(0.1)
            except:
                pass
        print (time.time() - begin)
        return ''.join(total_data)

    #function to wait for oncoming connection fro Java client
    def _wait_for_connections(self):
        while True:
            self.socket.listen(1)
            conn, addr = self.socket.accept()
            self.client_addr = addr
            print('Got connection from:', addr)
            data = conn.recv(1024)
            string = bytes.decode(data)
            print string
            request_method = string.strip()
            print ('Method: ', request_method)
            if (request_method == 'GET'):
                try:
                    file_handler = open(self.filename, 'rb')
                    print ('image opened')
                    response_content = file_handler.read()
                    file_handler.close()
                    # response_headers = self._gen_headers(200)
                except:
                    print ('Error', self.filename, '\n')
                server_response = response_content
                print ('sending image')
                conn.send(server_response)
                print ('image sent')
                conn.close()
            if (request_method == 'POST'):
                line = self.recv_timeout(conn)
                print(line)
                conn.close()
                self.writeLineToFile(line)

    def writeLineToFile(self, line):
        rows = json.loads(line)['positions']
        print ('json parsed\n')
        fieldnames = ['x', 'y']
        with open('line.csv', 'wb+') as f:
            print('file opened\n')
            dict_writer = csv.DictWriter(f, fieldnames)
            dict_writer.writeheader()
            dict_writer.writerows(rows)
            print('line written to file  \'line.csv\' \n')

    #function to free ost before closing
    def graceful_shutdown(sig, signum, stack):
        s.shutdown()
        self.cap.release()
        import sys
        sys.exit(1)

print ('Starting web server')
s = Server(8080)
#connect handler to the abort signal
signal.signal(signal.SIGINT, s.graceful_shutdown)
s.activate_server()








