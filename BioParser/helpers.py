def insertOrganism(organism):
    organism = organism.strip("\n")

    # Connect to the database.
    import pymysql
    conn = pymysql.connect(
        db='parser',
        user='root',
        passwd='bioParser',
        host='localhost')
    c = conn.cursor()

    # check if organisms is already in the database
    c.execute('SELECT 1 FROM organisms WHERE name=%s',(organism))

    # if it's not already there, insert it
    if not c.fetchone():
        c.execute('INSERT INTO organisms (name) VALUES (%s)',(organism))
    conn.commit()

    # Print the contents of the database.
    # c.execute("SELECT * FROM organisms")
    # print([(r[0], r[1]) for r in c.fetchall()])

def getOrganisms():
        # Connect to the database.
    import pymysql
    conn = pymysql.connect(
        db='parser',
        user='root',
        passwd='bioParser',
        host='localhost')
    c = conn.cursor()

    c.execute("SELECT * FROM organisms")
    organisms = []
    for o in c.fetchall():
        a = []
        a.append(o[0])
        a.append(o[1].replace("_"," "))
        organisms.append(a)
    return organisms