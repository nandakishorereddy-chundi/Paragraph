import json
import os

envf = 'envs/{0}.json'.format(os.environ.get('env', 'dev'))
with open(envf) as f: ENV = json.load(f)