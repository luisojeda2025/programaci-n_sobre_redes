# TP Sockets con Threading - Luis Ojeda - IFTS4

import socket
import threading

def manejar_cliente(conn, addr, lista_clientes): # definí "manejar_cliente con (los parámetros que le pasé)"
    print(f"\n[NUEVA CONEXIÓN] {addr} conectado.")
    
    conectado = True
    while conectado:
        try:
            # Recibe el mensaje
            mensaje = conn.recv(1024).decode('utf-8')
            if not mensaje:
                break
            
            # Limpié saltos de línea o espacios innecesarios
            mensaje_limpio = mensaje.strip()
            
            print(f"[{addr}] dice: {mensaje_limpio}")
            
            # 1. Comando /adios: Cierra la conexión del cliente
            if mensaje_limpio == "/adios":
                conn.send("Hasta luego. Desconectando...\n".encode('utf-8'))
                conectado = False
            
            # 2. Comando /users: Muestra lista las direcciones de todos los usuarios conectados
            elif mensaje_limpio == "/users":
                # Armamé una lista legible con las IPs/Puertos conectados
                # Usé getpeername() para obtener la tupla (IP, Puerto) de cada socket
                usuarios_conectados = []
                for cliente in lista_clientes:
                    try:
                        usuarios_conectados.append(str(cliente.getpeername()))
                    except OSError:
                        pass
                
                respuesta = f"Usuarios conectados ({len(usuarios_conectados)}):\n" + "\n".join(usuarios_conectados) + "\n"
                conn.send(respuesta.encode('utf-8'))
            
            # 3. Respuesta por defecto: Eco (devuelve lo que le escribo, exactamente igual)
            else:
                conn.send(f"Eco: {mensaje_limpio}\n".encode('utf-8'))
            
        except (ConnectionResetError, ConnectionAbortedError):
            break

    # Al terminar la conexión
    conn.close()
    if conn in lista_clientes:
        lista_clientes.remove(conn)
    print(f"\n[DESCONEXIÓN] {addr} se ha ido.")
    print(f"[CLIENTES ACTIVOS] {len(lista_clientes)}")

def iniciar_servidor():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Permite reutilizar la dirección/puerto inmediatamente después de reiniciar
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(('localhost', 5050))
    server.listen()
    
    clientes_activos = []
    print("[INICIO] Servidor escuchando en el puerto 5050...")

    while True:
        conn, addr = server.accept()
        clientes_activos.append(conn)
        
        # Crear hilo para el nuevo cliente
        hilo = threading.Thread(target=manejar_cliente, args=(conn, addr, clientes_activos))
        hilo.start()
        
        print(f"[CLIENTES ACTIVOS] {len(clientes_activos)}")

if __name__ == "__main__":
    iniciar_servidor()