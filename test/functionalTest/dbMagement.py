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
    
    querys = [f"DELETE FROM {table}" for table in tables]
    sqlQuery(querys)