import os
import sys
sys.path.append("/var/lovelace/venv/lib/python3.8/site-packages")
sys.path.append("/var/lovelace/lovelace/webapp")

import pwd

print(os.getuid())
print(os.geteuid())
#print(os.getsuid())
print(os.getgid())
print(os.getegid())
#print(os.getsgid())

for name in sys.modules:
    print(name)

#from lovelace.settings import dev

from important import key

#print(dev.SECRET_KEY)
print(key)