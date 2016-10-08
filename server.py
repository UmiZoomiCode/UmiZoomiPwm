import socketserver;

class handler(socketserver.StreamRequestHandler):
	def handle(self):
		print("here");
		self.data = self.rfile.readline().strip()
		print("here1");
		self.wfile.write(bytearray("Hello World", "utf8"));
		print("here2");

if __name__ == "__main__":
	HOST, PORT = "localhost", 9999
	
	server = socketserver.TCPServer((HOST, PORT), handler)
	
	server.serve_forever()