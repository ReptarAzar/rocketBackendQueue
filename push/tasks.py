from celery import task
import pycurl
from time import sleep
from celery.utils.log import get_task_logger
from django.core.cache import cache

url = "http://192.168.0.141:8080/"

logger = get_task_logger(__name__)

LOCK_EXPIRE = 60 * 5 # Lock expires in 5 minutes

def openSite():
    c = pycurl.Curl()
    c.setopt(c.URL, url)
    c.perform()

@task
def ping():
    lock_id = 'ping-lock'

    # cache.add fails if if the key already exists
    acquire_lock = lambda: cache.add(lock_id, 'true', LOCK_EXPIRE)
    # memcache delete is very slow, but we have to use it to take
    # advantage of using add() for atomic locking
    release_lock = lambda: cache.delete(lock_id)

    if acquire_lock():
        try:
            openSite()
        except :
            sleep(6)
            openSite()
            return "Maybe ping"
        finally:
            release_lock()
        return "Ping!"
    else:
        return "No ping"