import sys
sys.path.append("/var/lovelace/lovelace/webapp")

from lovelace.settings import dev

print(dev.SECRET_KEY)