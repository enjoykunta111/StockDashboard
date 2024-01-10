
'''
The CheckAccountHandler class in this script is modified to handle socket communication.
It receives an 'accesstoken' from the server, makes an API call, and sends the response back to the server.
'''

import socket
import asyncio
from requests import post
import json

class CheckAccountHandler:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.accessToken = None

    def connect_to_server(self):
        #self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))

    async def wait_for_accesstoken_and_start_check(self):
        # Wait for accesstoken from the server
        accesstoken = self.client_socket.recv(1024).decode()
        # Once received, proceed with start_check
        asyncio.run(self.start_check(accesstoken))

    async def start_check(self, accessToken):
        # API call (mocked for this example)
        response = await self.mock_api_call(accessToken)
        # Send response back to server
        self.client_socket.sendall(response.encode())

    async def mock_api_call(self, accessToken):
        # Mock API call logic
        accessToken = 'example accessToken'
        return f'Mock response for {accessToken}'

# Example usage
if __name__ == "__main__":
    host = 'localhost'  # Server's host
    port = 5000        # Server's port

    handler = CheckAccountHandler(host, port)
    handler.connect_to_server()
    handler.wait_for_accesstoken_and_start_check()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(handler.start_check(accessToken))
