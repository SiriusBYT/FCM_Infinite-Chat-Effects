import socket
import time 

def FlashClient_API_Request(API_Request):
    def Ready(RemoteServer):
        print(f'[Flashstore API // Client] Sent to the server that we are ready to receive data.')
        RemoteServer.send(str.encode('READY'))

    print(f'[Flashstore API // Client] INFO: Attempting to communicate with the FlashStore API...')
    # Server Information
    ServerAddress = "aura-two.sirio-network.com"
    ServerPort = 1407
    PacketSize = 1024
    RemoteServer = socket.socket()
    API_Version = "2.01"
    DebugMode = False
    Data = []
    try:
        RemoteServer.connect((ServerAddress, ServerPort))
    except socket.error as ErrorInfo:
        print(f'[Flashstore API // Client] Error connecting to the FlashStore API: "{ErrorInfo}".')
    print(f'[Flashstore API // Client] Successfully connected to {ServerAddress}:{ServerPort}.')
    print(f'[Flashstore API // Client] Sent that we are requesting to use version v{API_Version} of the API.')
    RemoteServer.send(str.encode(API_Version))
    RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
    if True and RemoteServer_Response == "OK" or RemoteServer_Response == "SERVER-OUTDATED_API-VERSION":
        if RemoteServer_Response == "OK":
            print(f'[Flashstore API // Client] Received Code: {RemoteServer_Response}, starting loop.')
        else:
            print(f'[Flashstore API // Client] WARNING: Received Code: {RemoteServer_Response}, which means the server is running an outdated API version, we are ignoring it and are starting the loop anyways, note that the request may fail.')
        print(f'[Flashstore API // Client] Requesting to the server "{API_Request}".')
        RemoteServer.send(str.encode(API_Request))
        while True:
            RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
            if RemoteServer_Response == "":
                if DebugMode == True: print("Server didn't send new data.")
            else:
                print(f'[Flashstore API // Client] Received Code: {RemoteServer_Response}.')
                if RemoteServer_Response == "DONE":
                    return Data
                elif RemoteServer_Response == "SENDING":
                    Ready(RemoteServer)
                    while RemoteServer_Response != "DONE":
                        RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
                        if RemoteServer_Response == "":
                            if DebugMode == True: print("Server didn't send new data.")
                            time.sleep(1)
                        elif RemoteServer_Response != "DONE":
                            print(f'[Flashstore API // Client] Server filled our request with the data "{RemoteServer_Response}".')
                            Data = RemoteServer_Response
                    return Data
                elif RemoteServer_Response == "INVALID_ARGUMENTS":
                    print(f'[Flashstore API // Client] The server told us that our "{API_Request}" request is invalid!')
                    break
                elif RemoteServer_Response == "MISSING_ARGUMENTS":
                    print(f'[Flashstore API // Client] The server told us that "{API_Request}" is missing arguments!')
                    break
                elif RemoteServer_Response == "NOT_FOUND":
                    print(f'[Flashstore API // Client] The server told us that "{API_Request}" could not be found!')
                    break
                elif RemoteServer_Response == "UNKNOWN_ERROR":
                    print(f'[Flashstore API // Client] An Unknown Error Occurred!')
                    return Data
    elif True and RemoteServer_Response == "INVALID_API-VERSION":
        print(f'[Flashstore API // Client] The Flashstore Client is outdated! Server sent "{RemoteServer_Response}".')
    else:
        print(f'[Flashstore API // Client] Unknown error while connecting to server ! Server sent "{RemoteServer_Response}".')