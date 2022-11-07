#https://pypi.org/project/api4jenkins/
from api4jenkins import Jenkins

def client(address,auth):
    return Jenkins(address,auth=auth)
