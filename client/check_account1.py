import socket
import asyncio

class CheckAccountClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    async def connect_to_server(self):
        reader, writer = await asyncio.open_connection(self.host, self.port)
        return reader, writer

    async def listen_for_requests(self):
        reader, writer = await self.connect_to_server()
        while True:
            data = await reader.read(1024)
            if data.decode() == 'check_account_request_2':
                account_data = self.fetch_account_data()  # API 호출 및 데이터 처리
                writer.write(account_data.encode())
                await writer.drain()
        writer.close()

    def fetch_account_data(self):
        # 외부 API 호출 및 데이터 처리 로직
        return 'account data'

async def main():
    client = CheckAccountClient('localhost', 5000)
    await client.listen_for_requests()

asyncio.run(main())
