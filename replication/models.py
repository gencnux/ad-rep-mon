from django.db import models

class ReplicationLog(models.Model):
    source_server = models.CharField(max_length=200)
    target_server = models.CharField(max_length=200)
    status = models.CharField(max_length=50)
    last_checked = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source_server} → {self.target_server}: {self.status}"