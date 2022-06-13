import os
import sys
sys.path.append("/var/lovelace/venv/lib/python3.8/site-packages")
sys.path.append("/var/lovelace/lovelace/webapp")

import pwd

print(os.getuid())

from lovelace.settings import dev

print(dev.SECRET_KEY)