import os
import sys
sys.path.append("/var/lovelace/venv/lib/python3.8/site-packages")
sys.path.append("/var/lovelace/lovelace/webapp")
from lovelace.settings import dev
print(dev.SECRET_KEY)

import pwd

print(os.getuid())
print(os.geteuid())
#print(os.getsuid())
print(os.getgid())
print(os.getegid())
#print(os.getsgid())


print(sys.version)

from important import key

print(key)