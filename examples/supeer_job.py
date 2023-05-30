from jobmatchup.api import Query
from jobmatchup.configs import Config, DBConfig

# create config
# ! need to have env variables !
cfg = Config(without_auth=False, login_pass_auth=False, from_env=True)

# create Query-object with parameters
# async_work - async request is needed if you want to make a request to all available API
q = Query(cfg=cfg, search='Python', amt=100, async_work=True)

# get the result
print(q.get_all())
