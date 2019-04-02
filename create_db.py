import MySQLdb

conn = MySQLdb.connect(host = "cs346-project2-1.cbhi0v14khzk.us-west-2.rds.amazonaws.com",
    user = "nicrobkal",
    port = 3306,
    passwd = "Cosmo123$%",
    db = "cs346_project2")

cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS Conversations, Posts;")

cursor.execute("SET @@time_zone = 'America/Phoenix';")

cursor.execute("""
    CREATE TABLE Conversations(
    Topic VARCHAR(100),
    Username VARCHAR(42),
    CONSTRAINT Conversations PRIMARY KEY(Topic, Username));
""")

cursor.execute("""
    CREATE TABLE Posts(
    PostNum INT(10) AUTO_INCREMENT,
    Topic VARCHAR(100),
    OriginUsername VARCHAR(42),
    Username VARCHAR(42),
    Text VARCHAR(2000),
    Time TIMESTAMP,
    Likes INT(10),
    CONSTRAINT Posts PRIMARY KEY(PostNum));
""")
