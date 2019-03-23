import MySQLdb

conn = MySQLdb.connect(host = "cs346-project2-1.cbhi0v14khzk.us-west-2.rds.amazonaws.com",
    user = "nicrobkal",
    port = 3306,
    passwd = "Cosmo123$%",
    db = "cs346_project2")

cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE Conversations(
    Topic VARCHAR(100),
    Username VARCHAR(42),
    Text VARCHAR(2000),
    Time DATE,
    CONSTRAINT Conversations PRIMARY KEY(Topic, Username));
""")
