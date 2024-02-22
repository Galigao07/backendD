from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.serializers import serialize
from backend.models import POS_Terminal, PosExtended
from backend.login import get_serial_number

@receiver(post_save,sender=PosExtended)
def model_saved(sender, instance, created, **kwargs):
    if not created:
        print('0')
        print('0',instance)
        action = "Update"

        send_to_extended(instance, action)
    else:
        action = "Save" 
        send_to_extended(instance, action)
  

@receiver(post_delete,sender=PosExtended)
def model_deleted(sender, instance, **kwargs):
    action = "Delete"
    send_to_extended(instance, action)

def send_to_extended(instance, action, **kwargs):
    try:
        print(1)
        instance_json = serialize('json', [instance])
        # Convert serialized data to dictionary
        data = json.loads(instance_json)[0]['fields']
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number).first()
        print(2)
        pos_extended_count = PosExtended.objects.filter(serial_no=serial_number).count()
        # Convert model instance to JSON serializable format
        print('dataaaaaa',data)
        instance_data = {
            "data":data,
            "action": action,
            "count":pos_extended_count
        }

        # Send message to consumer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "extended_group",  # Channel group name
            {
                "type": "Send_to_front_end_extended",
                "data": instance_data,  # Convert instance data to JSON
            }
        )
    except Exception as e:
        # Handle any exceptions that may occur during message sending
        print(f"Error sending message to consumer: {e}")
