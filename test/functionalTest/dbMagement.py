from nogaspi.dbEngine import EngineSQLAlchemy
            
def sqlQuery(querys):
    with EngineSQLAlchemy() as session:
        for query in querys:
            session.execute(query)
        session.commit()