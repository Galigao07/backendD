import pdb
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from django.core.serializers import serialize
from backend.models import POS_Terminal, PosExtended,PosSalesOrder,PosSalesInvoiceList,PosSalesTrans
from backend.views import get_serial_number

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
    send_to_frontend_data(instance, action)

def send_to_extended(instance, action, **kwargs):
    try:
        print(1)
        instance_json = serialize('json', [instance])
        # Convert serialized data to dictionary
        data = json.loads(instance_json)[0]['fields']
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        print(2)
        pos_extended_count = PosExtended.objects.filter(serial_no=machineInfo.Serial_no.strip()).count()
        # Convert model instance to JSON serializable format
        print('dataaaaaa',data)
        print('action',action)
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

def send_to_extended2(changeData, action, **kwargs):
    try:


        # Send message to consumer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "extended_groupchange",  # Channel group name
            {
                "type": "Send_to_front_end_extendedChange",
                "data": changeData,  # Convert instance data to JSON
            }
        )
    except Exception as e:
        # Handle any exceptions that may occur during message sending
        print(f"Error sending message to consumer: {e}")

@receiver(post_save,sender=PosSalesOrder)
def model_savedSales(sender, instance, created, **kwargs):
    if not created:
        action = "Update"

        send_to_frontend_data(instance, action)
    else:
        action = "Save" 
        send_to_frontend_data(instance, action)

@receiver(post_save,sender=PosSalesInvoiceList)
def model_savedSalesInvoice(sender, instance, created, **kwargs):
    if not created:
        action = "Update"

        send_to_frontend_data(instance, action)
    else:
        action = "Save" 
        # pdb.set_trace()
        send_to_frontend_data(instance, action)
        instance_json = serialize('json', [instance])
        data = json.loads(instance_json)[0]['fields']
        doc_no = data['doc_no']
        serial_number = get_serial_number()
        machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
        print('datainstance',data)
        print('doc_no',doc_no)
        tmp = PosSalesTrans.objects.filter(sales_trans_id = int(float(doc_no)),terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no)).first()
        print('tmp',tmp)
        if tmp:
            total = float(data['sub_total']) - (float(data['vat_exempted']) + float(data['discount']))
            changeData = {
                'AmountTendered':tmp.amount_tendered,
                'AmountDue':total,
            }
            print('changeData',changeData)
            send_to_extended2(changeData, action)


def send_to_frontend_data(instance, action, **kwargs):
    try:
       
        instance_data = {
            "data":'refresh',
            "action":action,
            "message":'',
        }
        print('refreshxxxxx',action)
        # Send message to consumer
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "count_group",  # Channel group name
            {
                "type": "send_to_frontendCOunt",
                "message": instance_data,  # Convert instance data to JSON
            }
        )
    except Exception as e:
        # Handle any exceptions that may occur during message sending
        print(f"Error sending message to consumer: {e}")