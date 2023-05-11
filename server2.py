from socket import *

# Set alamat IP dan port yang akan digunakan oleh web server
ip_address = '127.0.0.1'
port = 80

# Buat socket TCP
server_socket = socket(AF_INET, SOCK_STREAM)

# Kaitkan socket dengan alamat IP dan port
server_socket.bind((ip_address, port))

# Mulai menerima koneksi dari client
server_socket.listen(1)

# Tampilkan informasi bahwa web server sudah berjalan
print(f"Server berjalan pada alamat {ip_address} dan port {port}\n")

# Terus lakukan perulangan untuk menerima koneksi dari client
while True:
    # Terima koneksi dari client dan buat socket baru untuk koneksi tersebut
    client_socket, client_address = server_socket.accept()

    try:
        # Terima HTTP request dari client
        request = client_socket.recv(1024).decode()
        
        # Parsing HTTP request untuk mendapatkan method dan file yang diminta
        method = request.split()[0]
        file_path = request.split()[1]

        # Tampilkan informasi tentang request yang diterima
        print(f"{method} {file_path}")
        
        # Jika file path adalah '/', ganti dengan '/index.html'
        if file_path == '/':
            file_path = '/index.html'

        # Buka file yang diminta oleh client
        file = open(file_path[1:], "rb")
        file_content = file.read()

        # Buat HTTP response message dengan header dan konten file yang diminta
        if file_path.endswith('.jpg'):
            content_type = 'image/jpeg'
        elif file_path.endswith('.png'):
            content_type = 'image/png'
        else:
            content_type = 'text/html'

        response = "HTTP/1.1 200 OK\r\nContent-Type: " + content_type + "\r\n\r\n"

        # Kirim response message ke client
        client_socket.send(response.encode())
        client_socket.sendall(file_content)

        # Tutup koneksi dengan client
        client_socket.close()

    except FileNotFoundError:
        # Jika file yang diminta tidak ditemukan, kirim pesan "404 Not Found" ke client
        response = "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n"
        client_socket.send(response.encode())
        client_socket.send("<html><body><h1>404 Not Found</h1></body></html>".encode())

        # Tutup koneksi dengan client
        client_socket.close()

    # Tampilkan status response yang dikirimkan ke client
    print(response.split('\r\n', 1)[0])
    print("\n")
