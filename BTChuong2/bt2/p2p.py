import websockets
import asyncio

connected_peers = set()

async def handle(websocket):
    connected_peers.add(websocket)
    print("Peer đã tham gia")

    try:
        async for message in websocket:
            print("Peer:", message)
    except:
        pass
    finally:
        connected_peers.remove(websocket)
        print("Peer đã rời khỏi")

async def send_message():
    while True:
        msg = await asyncio.to_thread(input, "Nhập tin nhắn: ")
        for peer in connected_peers.copy():
            try:
                await peer.send(msg)
            except:
                pass

async def connect_to_peer(uri):
    try:
        websocket = await websockets.connect(uri)
        connected_peers.add(websocket)
        print("Đã kết nối tới", uri)
          # 🔥 TẠO TASK LẮNG NGHE
        asyncio.create_task(listen_to_peer(websocket))

    except Exception as e:
        print("Không thể kết nối:", e)
async def listen_to_peer(websocket):
    try:
        async for message in websocket:
            print("Peer:", message)
    except:
        pass
    finally:
        connected_peers.remove(websocket)
        print("Peer đã rời khỏi")
async def main():
    port = input("Nhập port của peer này: ")

    async with websockets.serve(handle, "0.0.0.0", int(port)):
        print(f"Peer đang chạy tại ws://localhost:{port}")

        await asyncio.sleep(1)

        other = input("Nhập port peer khác: ")
        if other:
            await connect_to_peer(f"ws://localhost:{other}")

        await send_message()

asyncio.run(main())