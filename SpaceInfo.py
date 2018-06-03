import wmi, pathlib, sqlite3
pathlib.Path('.\\Logs').mkdir(parents=True, exist_ok=True)
database = '.\\Logs\DiskLogs.db'

def dbConnection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except sqlite3.Error as err:
        self.log.error('dberror: %s' % err)

def getServersFromDB():
    #try:
    conn = dbConnection(database)
    cur = conn.cursor()
    cur.execute("""
        SELECT  ServerName
        FROM    Servers
    """)
    serverNames = cur.fetchall()
    return serverNames, conn, cur

def printDiskUsageToDB():
    serverNames, conn, cur = getServersFromDB()
    for server in serverNames[0]:
        connectedServer = wmi.WMI(server)
        for disk in connectedServer.Win32_LogicalDisk(DriveType=3):
            cur.execute("""
                INSERT INTO DiskUsage(ServerID, Caption, FreeSpace, Size, DateCaptured)
                VALUES ('{SER}', '{CAP}', {FRS}, {SIZ}, DATE('NOW'))
            """\
            .format(SER=server, CAP=disk.caption, FRS=int(disk.FreeSpace), SIZ=int(disk.Size)))
    conn.commit()
    conn.close()

class SpaceInformant():
    def spaceWarning():
        #Check if disk usage is at a certain level, then report it.
        pass
    def reportUsage():
        print('test')

if __name__ == "__main__":
    printDiskUsageToDB()
