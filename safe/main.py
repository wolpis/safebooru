import sys
from safe import Posts

update_url = sys.argv[1]
webhook = sys.argv[2]

p = Posts()
if p.save(update_url, webhook):
    sys.exit()
else:
    raise
