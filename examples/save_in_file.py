# create DB config
db_cfg = DBConfig()

# make the db-object
database = db.Repository(db_cfg)

# Save to file
q.get_all()
for v in q.result.values():
    for vac in v:
        database.db.add_vacancy(vac)