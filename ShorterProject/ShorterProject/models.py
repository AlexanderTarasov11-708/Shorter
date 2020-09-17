import hashlib
import os

from django.db import models


class Link(models.Model):
    link = models.URLField()
    # Store the total redirects here so we don't need to do a possibly expensive SUM query on HitsDatePoint
    hash = models.CharField(max_length=6)
    hits = models.IntegerField(default=0)

    def get_hash(self):
        gen_salt = os.urandom(hashlib.blake2b.SALT_SIZE)  # Generated salt
        key = hashlib.blake2b(salt=gen_salt, digest_size=3)
        key.update(self.link.encode())  # Generated hash
        return key.hexdigest()


class HitsDatePoint(models.Model):
    day = models.DateField(auto_now=True, db_index=True)
    hits = models.IntegerField(default=0)
    link = models.ForeignKey(Link, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("day", "link"),)
