#https://pypi.org/project/api4jenkins/
from api4jenkins import Jenkins


class jenkins_helper():

    def __init__(self,address,auth):
        self.client=Jenkins(address,auth=auth)

    def is_running(self,job_name):
        job=self.client.get_job(job_name)
        return job.building

    def running_builds(self):
        return [ (b,b.get_parameters()) for b in self.client.nodes.iter_builds() ]

    


