from django.conf import settings


#https://pypi.org/project/api4jenkins/
from api4jenkins import Jenkins

class jenkins_helper():

    def __init__(self,address,auth):
        self.client=Jenkins(address,auth=auth)

    def refresh_client(self):
        self.client=Jenkins(address,auth=auth)

    def is_running(self,job_name):
        try:
            job=self.client.get_job(job_name)
        except:
            self.refresh_client()
            job=self.client.get_job(job_name)
        return job.building

    def running_builds(self):
        try:
            for node_name in settings.JENKINS_TRAINING_NODES:
                return [ (b,b.get_parameters(),node_name) for b in self.client.nodes.get(node_name) if b.building ]
        except:
            self.refresh_client()
            for node_name in settings.JENKINS_TRAINING_NODES:
                return [ (b,b.get_parameters(),node_name) for b in self.client.nodes.get(node_name) if b.building ]


    


