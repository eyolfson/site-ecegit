from django.db.models.signals import post_save, pre_delete
from django_ssh.models import Key

from django_ece459_1161.utils import receive_key_create, receive_key_delete

# Signals
post_save.connect(receive_key_create, Key)
pre_delete.connect(receive_key_delete, Key)
