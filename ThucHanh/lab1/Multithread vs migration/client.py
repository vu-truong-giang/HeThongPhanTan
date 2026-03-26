import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect("localhost", 65432)

print("Ví dụ query:")
print('std["gpa"] > 3.5')
print('std["age"] == 20')
print('std["name"] == "Alice"')
query = input("Enter your query (e.g., std['age'] > 20): ")
client.send(query.encode())

res = client.recv(4096).decode()
print(f"Response from server: {res}")
client.close()

