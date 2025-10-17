


# import pdb
# from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# import json
# from django.conf import settings
# from django.core.serializers import serialize
# from backend.models import POS_Terminal, PosExtended,PosSalesOrder,PosSalesInvoiceList,PosSalesTrans,PosSuspendList
# from backend.views import get_serial_number
# from backend.middleware import get_current_request_cookie

# import jwt

# # @receiver(post_save,sender=PosSuspendList)
# # def susppend_saved(sender, instance, created, **kwargs):
# #     if not created:
# #         action = "Update"

# #         send_to_extended(instance, action)
# #     else:
# #         action = "Save" 
# #         send_to_extended(instance, action)
  

# # @receiver(post_delete,sender=PosSuspendList)
# # def susppend_deleted(sender, instance, **kwargs):
# #     action = "Delete"
# #     send_to_extended(instance, action)
# #     send_to_frontend_data(instance, action)



# @receiver(post_save,sender=PosExtended)
# def model_saved(sender, instance, created, **kwargs):
#     if not created:
#         action = "Update"

#         send_to_extended(instance, action)
#     else:
#         action = "Save" 
#         send_to_extended(instance, action)
  

# @receiver(post_delete,sender=PosExtended)
# def model_deleted(sender, instance, **kwargs):
#     action = "Delete"
#     send_to_extended(instance, action)
#     send_to_frontend_data(instance, action)

# def send_to_extended(instance, action, **kwargs):
#     token = get_current_request_cookie()
#     if not token:
#         return

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         serial_number = payload.get("SERIALNO")
#         print("Serial from JWT:", serial_number)
#     except Exception as e:
#         print("JWT decode error:", e)
#     try:
#         instance_json = serialize('json', [instance])
#         # Convert serialized data to dictionary
#         data = json.loads(instance_json)[0]['fields']
        
#         machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
#         pos_extended_count = PosExtended.objects.filter(serial_no=machineInfo.Serial_no.strip()).count()
#         # Convert model instance to JSON serializable format
#         instance_data = {
#             "data":data,
#             "action": action,
#             "count":pos_extended_count
#         }

#         # Send message to consumer
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "extended_group",  # Channel group name
#             {
#                 "type": "Send_to_front_end_extended",
#                 "data": instance_data,  # Convert instance data to JSON
#             }
#         )
#     except Exception as e:
#         # Handle any exceptions that may occur during message sending
#         print(f"Error sending message to consumer: {e}")

# def send_to_extended2(changeData, action, **kwargs):
#     try:


#         # Send message to consumer
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "extended_groupchange",  # Channel group name
#             {
#                 "type": "Send_to_front_end_extendedChange",
#                 "data": changeData,  # Convert instance data to JSON
#             }
#         )
#     except Exception as e:
#         # Handle any exceptions that may occur during message sending
#         print(f"Error sending message to consumer: {e}")

# @receiver(post_save,sender=PosSalesOrder)
# def model_savedSales(sender, instance, created, **kwargs):
#     if not created:
#         action = "Update"

#         send_to_frontend_data(instance, action)
#     else:
#         action = "Save" 
#         send_to_frontend_data(instance, action)

# @receiver(post_save,sender=PosSalesInvoiceList)
# def model_savedSalesInvoice(sender, instance, created, **kwargs):
#     token = get_current_request_cookie()
#     if not token:
#         return

#     try:
#         payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
#         serial_number = payload.get("SERIALNO")
#         print("Serial from JWT:", serial_number)
#     except Exception as e:
#         print("JWT decode error:", e)
#     if not created:
#         action = "Update"

#         send_to_frontend_data(instance, action)
#     else:
#         action = "Save" 
#         # pdb.set_trace()
#         send_to_frontend_data(instance, action)
#         instance_json = serialize('json', [instance])
#         data = json.loads(instance_json)[0]['fields']
#         doc_no = data['doc_no']
#         machineInfo = POS_Terminal.objects.filter(Serial_no=serial_number.strip()).first()
#         tmp = PosSalesTrans.objects.filter(sales_trans_id = int(float(doc_no)),terminal_no = machineInfo.terminal_no,site_code = int(machineInfo.site_no)).first()
#         if tmp:
#             total = float(data['sub_total']) - (float(data['vat_exempted']) + float(data['discount']))
#             changeData = {
#                 'AmountTendered':tmp.amount_tendered,
#                 'AmountDue':total,
#                 'Open':False,
#             }
#             send_to_extended2(changeData, action)


# def send_to_frontend_data(instance, action, **kwargs):
#     try:
#         instance_data = {
#             "data":'refresh',
#             "action":action,
#             "message":'',
#         }
#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "count_group",  # Channel group name
#             {
#                 "type": "send_to_frontendCOunt",
#                 "message": instance_data,  # Convert instance data to JSON
#             }
#         )
#     except Exception as e:
#         # Handle any exceptions that may occur during message sending
#         print(f"Error sending message to consumer: {e}")