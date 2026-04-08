import socket
import json
from dice import Dice

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost", 8081))
server_socket.listen(1)

print("Server is listening on port 8081...")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address} established.")

    request = client_socket.recv(4096).decode("utf-8")
    print(f"Request received ({len(request)}):")
    print("*" * 50)
    print(request)
    print("*" * 50)

    lines = request.split("\r\n")
    request_line = lines[0]

    if request_line.startswith("POST /roll_dice"):
        try:
            if "\r\n\r\n" not in request:
                raise ValueError("Missing request body")

            body = request.split("\r\n\r\n", 1)[1]
            data = json.loads(body)

            probabilities = data["probabilities"]
            number_of_random = data["number_of_random"]

            dice = Dice(probabilities)
            results = dice.roll(number_of_random)

            response_data = {
                "status": "success",
                "results": results
            }

            response_json = json.dumps(response_data)

            response = (
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_json)}\r\n"
                "\r\n"
                f"{response_json}"
            )

        except Exception as e:
            response_data = {
                "status": "error",
                "message": str(e)
            }

            response_json = json.dumps(response_data)

            response = (
                "HTTP/1.1 400 Bad Request\r\n"
                "Content-Type: application/json\r\n"
                f"Content-Length: {len(response_json)}\r\n"
                "\r\n"
                f"{response_json}"
            )

    elif request_line.startswith("GET /myjson"):
        response_data = {
            "status": "success",
            "message": "Hello, KU!"
        }

        response_json = json.dumps(response_data)

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: application/json\r\n"
            f"Content-Length: {len(response_json)}\r\n"
            "\r\n"
            f"{response_json}"
        )

    elif request_line.startswith("GET"):
        html = f"<html><body><h1>Hello, World!</h1><hr>{request}</body></html>"

        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/html\r\n"
            f"Content-Length: {len(html)}\r\n"
            "\r\n"
            f"{html}"
        )

    else:
        response = "HTTP/1.1 405 Method Not Allowed\r\n\r\n"

    client_socket.sendall(response.encode("utf-8"))
    client_socket.close()

    print("Waiting for the next TCP request...")