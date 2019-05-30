#
#	This is the server that handles the requests from snap!.
#	The server recieves an HTTP request from snap! and either
#	hands it over to qa_controller.py or tts.py, depending
#   on what type of request it is
#	

from http.server import BaseHTTPRequestHandler, HTTPServer
from qa_controller import answer_q
from qa_controller import retrieve_exact_matches
from qa_controller import retrieve_inexact_matches
from tts import run_tts
from tts import stop_speak
 
class ctlHTTPServer_RequestHandler(BaseHTTPRequestHandler):

	def make_query_req(self, num_matches, q, type, normalize):
		print("Normalized: %s, # match(es): %d, Bigrams: %s" % (str(self.normalize), self.num_matches, str(self.use_bigrams)))		
		try:
			if(type=='exact_match'):
				answer = retrieve_exact_matches(q)
			elif(type=='inexact_match_overlap'):
				answer = retrieve_inexact_matches(q, normalize, num_matches, "overlap", use_bigrams=self.use_bigrams)
			elif(type=="inexact_match_cosine"):
				answer = retrieve_inexact_matches(q, normalize, num_matches, "cosine", use_bigrams=self.use_bigrams)
			elif(type=="answer"):
				answer = answer_q(q)
			else:
				pass
		except:
			return 'ERROR for query: "' + q + '"'

		if answer is None:
			answer = 'Ran unsuccesfully! "' + q + '"'
		return answer

	# Text to speech
	def make_tts_req(self, prompt):
		return run_tts(prompt)

	def make_stopspeak_req(self):
		stop_speak()
		return "True"


	def do_GET(self):
		self.send_response(200)
		
		response = "Response not processed" #default response
		self.use_bigrams = False
		self.normalize = False
		self.num_matches = 1

		self.send_header('Access-Control-Allow-Origin', '*')
		self.end_headers()

		#Process and split the arguments and parameters from the path
		path = self.path[2:].lower()
		path = path.replace('%20', ' ').replace('%27', '\'').replace('/','')
		split_input = path.split('+')
		req_type = split_input[0]
		req_arg = split_input[1]
		
		#Store extra params, if they exist (Never currently used)
		req_param = ['','','']
		if(len(split_input) > 3):
			req_param = split_input[2:5]
			print(req_param)
		
		if(self.path[1]=='?'):
			#Set parameters
			if(req_param[1] != ''):
				self.num_matches = int(req_param[1])

			if(req_param[2] != '' and req_param[2] == "bigrams"):
				self.use_bigrams = True

			if(req_param[0] != '' and req_param[0] == "normalize"):
				self.normalize = True

			#Check what the request is for
			if(req_type == 'query'):
				print('Query request: ' + req_arg)
				response = self.make_query_req(self.num_matches, req_arg, "answer", self.normalize)

			elif(req_type == 'ematch'):
				print('Exact match request: ' + req_arg)
				response = self.make_query_req(self.num_matches, req_arg, "exact_match", self.normalize)

			elif(req_type == 'inmatch overlap'):
				print('Inexact match overlap request: ' + req_arg)
				response = self.make_query_req(self.num_matches, req_arg, "inexact_match_overlap", self.normalize)

			elif(req_type == 'inmatch cosine'):
				print('Inexact match cosine request: ' + req_arg)
				response = self.make_query_req(self.num_matches, req_arg, "inexact_match_cosine", self.normalize)

			elif(req_type == 'speak'):
				print('TTS request: ' + req_arg)
				response = self.make_tts_req(req_arg)

			elif(req_type == 'stopspeak'):
				print('Stop speak request' + req_arg)
				response = self.make_stopspeak_req()

			else:
				response = 'ERROR 404 - Request not recognized for ' + self.path
				print(response)

		else:
			response = 'ERROR 404 - Request not recognized for ' + self.path
			print(response)


		# Send the response message back to client
		self.wfile.write(bytes(response, "utf8"))
		print('\nRequest finished')
		return
	 	
	def do_POST(self):
		pass

def main():
	print('Starting server...')
	# Server settings
	server_address = ('127.0.0.1', 8000)
	httpd = HTTPServer(server_address, ctlHTTPServer_RequestHandler)
	try:
		print('Server running...')
		httpd.serve_forever()
	except KeyboardInterrupt:
		print('Shutting down...')

if __name__ == '__main__':
	main()