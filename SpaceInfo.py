import wmi, pathlib, sqlite3
pathlib.Path('.\\Logs').mkdir(parents=True, exist_ok=True)
database = '.\\Logs\DiskLogs.db'

def dbConnection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except sqlite3.Error as err:
        self.log.error('dberror: %s' % err)

def getServersFromFile():
    try:
        dbConnection(database)
        serverNameFromFile = open('.\Servers.txt', 'r')
        serverNames = serverNameFromFile.read().splitlines()
        return serverNames
    except IOError:
        print('Error when opening "Servers.txt", Check if the file exists in the root directory')

def printDiskUsageToFile():
    serverNames = getServersFromFile()
    conn = dbConnection(database)
    cur = conn.cursor()
    #printToFile = open('.\Logs\DiskUsage.txt', 'a')
    for server in serverNames:
        c = wmi.WMI(server)
        for disk in c.Win32_LogicalDisk(DriveType=3):
            cur.execute("""
                INSERT INTO DiskUsage(ServerID, Caption, FreeSpace, Size, DateCaptured)
                VALUES ('{SER}', '{CAP}', {FRS}, {SIZ}, DATE('NOW'))
            """\
            .format(SER=server, CAP= disk.caption, FRS=int(disk.FreeSpace), SIZ=int(disk.Size)))
            #printToFile.write(server + ' ' + disk.Caption + "%0.2f%% free" % (100.0 * int(disk.FreeSpace) / int(disk.Size)) + '\n') 
    #printToFile.close()
    conn.commit()
    conn.close()

printDiskUsageToFile()
