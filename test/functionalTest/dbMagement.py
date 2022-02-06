from nogaspi.dbEngine import EngineSQLAlchemy
            
def sqlQuerysWithCommit(querys):
    with EngineSQLAlchemy() as session:
        for query in querys:
            session.execute(query)
        session.commit()

def sqlQuery(query):
    with EngineSQLAlchemy() as session:
        return [row for row in session.execute(query)]

def sqlSelect(table, columnsExpected = '*', conditions = ''):
    
    columnNamesTmp = sqlQuery(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'{table}'")
    if columnsExpected == '*':
        queryColumns = '*'
        columnNames = [n[0] for n in columnNamesTmp]
    else:
        queryColumns = ", ".join(columnsExpected)
        columnNames = [n[0] for n in columnNamesTmp if n[0] in columnsExpected]

    queryRtr = sqlQuery(f"SELECT {queryColumns} FROM {table} {conditions};")

    return [dict(zip(columnNames, row)) for row in queryRtr]

def sqlDeleteAllData():
    tables = [
        'allergen',
        'article',
        'conversation',
        'donation',
        'donationCode',
        'favorite_donation',
        'fridge',
        'message',
        'product',
        'product_allergen',
        'rang',
        'user'
    ]
    
    querys = []
    querys.append("SET foreign_key_checks = 0;")
    for table in tables:
        querys.append(f"DELETE FROM {table};")
    querys.append("SET foreign_key_checks = 1;")
    sqlQuerysWithCommit(querys)