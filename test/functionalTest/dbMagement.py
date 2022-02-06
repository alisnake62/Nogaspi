from nogaspi.dbEngine import EngineSQLAlchemy
            
def sqlQuery(querys):
    with EngineSQLAlchemy() as session:
        for query in querys:
            session.execute(query)
        session.commit()

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
    sqlQuery(querys)