from jobmatchup.api import Query
from jobmatchup.configs import Config, DBConfig

# create config
cfg = Config(without_auth=True)

# create Query-object with parameters
q = Query(cfg=cfg, search="python", amt=100)

# display received vacancies
print(q.get_hh())
