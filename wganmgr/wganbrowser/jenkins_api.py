from django.conf import settings
import gc

#https://pypi.org/project/api4jenkins/
from api4jenkins import Jenkins

class jenkins_helper():

    def __init__(self,address,auth):
        self.client=Jenkins(address,auth=auth)

    def refresh_client(self):
        del(self.client)
        gc.collect()
        self.client=Jenkins(address,auth=auth)

    def is_running(self,job_name):
        self.refresh_client()
        job=self.client.get_job(job_name)
        return job.building

    def running_builds(self):
        self.refresh_client()
        for node_name in settings.JENKINS_TRAINING_NODES:
            return [ (b,b.get_parameters(),node_name) for b in self.client.nodes.get(node_name) if b.building ]

    def build(self,job_name,parameters):
        self.refresh_client()
        self.client.build_job(job_name,**parameters)







    


