import socket
import time 
import math

def FlashClient_API_Request(API_Request):
    DebugMode = False
    RequestTime = time.time()
    def GetLogTime():
        LogTime = time.localtime()
        LogTime_String = f"{LogTime.tm_hour:02d}:{LogTime.tm_min:02d}:{LogTime.tm_sec:02d} - {LogTime.tm_mday:02d}/{LogTime.tm_mon:02d}/{LogTime.tm_year}"
        return LogTime_String
    def WriteToLog(Log,isDebugMessage):
        LogTime = GetLogTime()
        LogString = f"[{LogTime} // FsAPI Client] {Log}"
        if isDebugMessage == True and DebugMode == True: print(LogString)
        elif isDebugMessage == False: print(LogString)
    
    LogString = f'INFO: Now attempting to request "{API_Request}" to the Flashstore API.'
    WriteToLog(LogString,True)

    # Status Codes
    def Ready(RemoteServer):
        LogString = f'INFO: We are ready to receive data.'
        WriteToLog(LogString,True)
        RemoteServer.send(str.encode('READY'))

    # Server Information
    OfflineDebug = False
    if OfflineDebug == True:
        ServerAddress = socket.gethostname()
    else:
        ServerAddress = "aura-two.sirio-network.com"
    ServerPort = 1407
    PacketSize = 1024
    RemoteServer = socket.socket()
    API_Version = "2.02"
    Data = []
    try:
        API_Latency = time.time()
        RemoteServer.connect((ServerAddress, ServerPort))
        API_Latency = math.floor((time.time() - API_Latency)/1000)
        API_Latency_String = f'{API_Latency}ms'
    except socket.error as ErrorInfo:
        LogString = f'ERROR: Failed to connect to the Flashstore API! \n[ERROR TRACEBACK]\n{ErrorInfo}'
        WriteToLog(LogString,False)

    LogString = f'SUCCESS: Connected to {ServerAddress}:{ServerPort}! (Latency: {API_Latency_String})'
    WriteToLog(LogString,False)
    LogString = f'INFOP: Requesting API Version {API_Version}...'
    WriteToLog(LogString,True)

    RemoteServer.send(str.encode(API_Version))
    RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
    if RemoteServer_Response == "OK" or RemoteServer_Response == "SERVER-OUTDATED_API-VERSION":
        if RemoteServer_Response == "OK":
            LogString = f'INFO: Server told us [OK].'
            WriteToLog(LogString,True)
        else:
            LogString = f'WARNING: Server told us that they are running an outdated API version, we will still continue the request but it may fail!'
            WriteToLog(LogString,False)
        LogString = f'INFO: Requesting "{API_Request}.'
        WriteToLog(LogString,True)
        RemoteServer.send(str.encode(API_Request))
        while True:
            try:
                RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
            except socket.timeout:
                LogString = f"ERROR: The server or us timed out!"
                WriteToLog(LogString,False)
                break
            LogString = f"INFO: Received {RemoteServer_Response}."
            WriteToLog(LogString,True)
            if RemoteServer_Response == "SENDING":
                Ready(RemoteServer)
                Data = None
                while Data == None:
                    try:
                        RemoteServer_Response = RemoteServer.recv(PacketSize).decode()
                    except socket.timeout:
                        LogString = f"ERROR: The server or we timed out!"
                        WriteToLog(LogString,False)
                        break
                    else:
                        Data = RemoteServer_Response
                        LogString = f'SUCCESS: Our request got filled with "{Data}"!'
                        WriteToLog(LogString,False)
                    RequestTime = time.time() - RequestTime
                    if Data != None and DebugMode == True:
                        LogString = f'SUCCESS: Request took {RequestTime} seconds to complete'
                        WriteToLog(LogString,True)
                        break
                    elif Data != None:
                        break
                return Data
            elif RemoteServer_Response == "INVALID_ARGUMENTS":
                LogString = f'ERROR: The server told us that our "{API_Request}" request is invalid!'
                WriteToLog(LogString,False)
                break
            elif RemoteServer_Response == "MISSING_ARGUMENTS":
                LogString = f'ERROR: The server told us that "{API_Request}" is missing arguments!'
                WriteToLog(LogString,False)
                break
            elif RemoteServer_Response == "NOT_FOUND":
                LogString = f'ERROR: The server told us that the result of "{API_Request}" could not be found!'
                WriteToLog(LogString,False)
                break
            elif RemoteServer_Response == "UNKNOWN_ERROR":
                LogString = f'ERROR: An unknown server-side error occurred!'
                WriteToLog(LogString,False)
        
        return Data
    elif RemoteServer_Response == "INVALID_API-VERSION":
        LogString = f'ERROR: Server denied our request because the client is outdated!'
        WriteToLog(LogString,False)
    else:
        LogString = f'ERROR: Unknown server response received! They sent us "{RemoteServer_Response}!'
        WriteToLog(LogString,False)

#FlashClient_API_Request("GET/PLUGINS/THARKI-GOD")