import wmi, pathlib
pathlib.Path('.\\Logs').mkdir(parents=True, exist_ok=True)

def getServersFromFile():
    try:
        serverNameFromFile = open('.\Servers.txt', 'r')
        serverNames = serverNameFromFile.read().splitlines()
        return serverNames
    except IOError:
        print('Error when opening "Servers.txt", Check if the file exists in the root directory')

def printDiskUsageToFile():
    serverNames = getServersFromFile()
    printToFile = open('.\Logs\DiskUsage.txt', 'a')
    for server in serverNames:
        c = wmi.WMI(server)
        for disk in c.Win32_LogicalDisk(DriveType=3):
            printToFile.write(server + ' ' + disk.Caption + "%0.2f%% free" % (100.0 * int(disk.FreeSpace) / int(disk.Size)) + '\n') 
    printToFile.close()

printDiskUsageToFile()

def mainApp():
    # Sjekke servere for diskplass %
    # Lage rapport for diskplass
    # Evt. slette gamle rapporter?
    # Varsle ved lav %
