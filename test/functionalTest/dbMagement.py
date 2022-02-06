from nogaspi.dbEngine import EngineSQLAlchemy
            
def sqlQuerysWithCommit(querys):
    with EngineSQLAlchemy() as session:
        for query in querys:
            session.execute(query)
        session.commit()

def sqlQuery(query):
    with EngineSQLAlchemy() as session:
        return [row for row in session.execute(query)]

#def sqlQuery(query):
#    with EngineSQLAlchemy() as session:
#        response = session.execute(query)
#        for row in response:
#            for col in row:
#                i = 1


        
def sqlDeleteAllData():
    tables = [
        'allergen',
        'article',
        'conversation',
        'donation',
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