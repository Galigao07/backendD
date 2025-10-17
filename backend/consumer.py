from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
import json
from asyncio import create_task, sleep
from collections import defaultdict
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
# Buffers to store updates per SERIALNO
update_buffers = defaultdict(list)
send_tasks = {}

DEBOUNCE_INTERVAL = 0.05  # 50ms debounce

class CountConsumerOld(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = "count_group"
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        TableNO = data['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_frontendCOunt',
                'message': data 
                # 'message': f'Received: {message}'
            }
        )
    async def send_to_frontendCOunt(self, event):

        await self.send(text_data=json.dumps(event))


class POSextended(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "extended_group"
        self.room_group_name ="extended_group"
        # self.room_group_name = f"extended_group%_"  % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_frontend',
                'message': f'Received: {message}'
            }
        )

    async def send_to_frontend(self, event):
        await self.send(text_data=json.dumps(event))

    async def Send_to_front_end_extended(self, event):

        data = event['data']
        await self.send(text_data=json.dumps(data))


class POSextendedChange(AsyncWebsocketConsumer):
    async def connect(self):
        # self.room_name = "extended_group"
        self.room_group_name ="extended_groupchange"
        # self.room_group_name = f"extended_group%_"  % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        await self.send(text_data=json.dumps({'message': 'Connected to WebSocket.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data

        await self.channel_layer.group_send(
            self.room_group_name,
            {
               "type": "Send_to_front_end_extendedChange",
                "data": data,  # Convert instance data to JSON
            }
        )


    async def Send_to_front_end_extendedChange(self, event):

        data = event['data']
        await self.send(text_data=json.dumps(data))

class CountConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # SERIALNO comes from routing (urls.py)
        self.SERIALNO = self.scope['url_route']['kwargs']['SERIALNO']
        self.room_group_name = f"count_group_{self.SERIALNO}"  # group per serial
        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser) or self.user is None:
            await self.close()  # Immediately close connection
            return
        # Add this connection to the serial-specific group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({'message': f'Connected to WebSocket for SERIALNO {self.SERIALNO}.'}))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get("message")
        tableno = data.get("TableNO")  # safer than overwriting


        # Broadcast only within this SERIALNO group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_to_frontend_count',
                'message': message,
                'TableNO': tableno,
                'SERIALNO': self.SERIALNO,
            }
        )

    async def send_to_frontend_count(self, event):
        await self.send(text_data=json.dumps(event))



# class PosExtendedMonitor(AsyncWebsocketConsumer):
#     async def connect(self):
#         self.SERIALNO = self.scope['url_route']['kwargs']['SERIALNO'].strip()
#         self.room_group_name = f"extended_monitor_{self.SERIALNO}"

#         await self.channel_layer.group_add(self.room_group_name, self.channel_name)
#         await self.accept()
#         print(f'Connected: {self.SERIALNO}')

#     async def disconnect(self, close_code):
#         await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
#         print(f'Disconnected: {self.SERIALNO}')

#     async def receive(self, text_data):
#         data = json.loads(text_data)
#         action = data.get("action")
#         payload = data.get("data")

#         # Add update to buffer
#         update_buffers[self.SERIALNO].append({
#             "action": action,
#             "data": payload
#         })

#         # Start debounce task if not already running
#         if self.SERIALNO not in send_tasks:
#             send_tasks[self.SERIALNO] = create_task(self._debounced_send(self.SERIALNO))

#     async def _debounced_send(self, serialno):
#         from .models import POS_Terminal, PosExtended
#         from .serializers import PosExtendedSerializer
#         # Wait for the debounce interval
#         await sleep(DEBOUNCE_INTERVAL)

#         # Collect all buffered updates
#         updates = update_buffers[serialno]
#         update_buffers[serialno] = []

#         # Prepare batch to send to frontend
#         batch_data = []
#         for update in updates:
#             action = update.get("action")
#             data = update.get("data")
#             print('action',action)
#             # If action is None, fetch the latest state
#             if action not in ["Save", "Update", "Delete"]:
#                 # Fetch last PosExtended for this SERIALNO
#                 last_data = await sync_to_async(
#                     lambda: PosExtended.objects.filter(serial_no=serialno).last()
#                 )()
#                 if last_data:
#                     data = PosExtendedSerializer(last_data).data

#             # Add to batch
#             if data:
#                 if isinstance(data, list):
#                     batch_data.extend(data)
#                 else:
#                     batch_data.append(data)

#         # Send batch update to all clients in this SERIALNO group
#         await self.channel_layer.group_send(
#             f"extended_monitor_{serialno}",
#             {
#                 "type": "pos_extended_monitor",
#                 "newData": batch_data,
#                 "action": action,
#             }
#         )

#         # Remove task reference
#         send_tasks.pop(serialno, None)

#     async def pos_extended_monitor(self, event):
#         await self.send(text_data=json.dumps({
#             "type": "extended_monitor",
#             "newData": event["newData"],
#             "action": event["action"],
#         }))


class PosExtendedMonitor(AsyncWebsocketConsumer):
    async def connect(self):
        # SERIALNO comes from your routing (urls.py)
        self.SERIALNO = self.scope['url_route']['kwargs']['SERIALNO']
        self.room_group_name = f"extended_monitor_{self.SERIALNO}"  # unique group per serial
        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser) or self.user is None:
            await self.close()  # Immediately close connection
            return
        # Add this connection to the SERIALNO-specific group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        # Remove connection from the group

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )


    async def receive(self, text_data):
        data = json.loads(text_data)
      
        data1  =''
        SERIALNO = data.get("SERIALNO")
        action = data.get("action")
    
        from .models import POS_Terminal, PosExtended
        from .serializers import PosExtendedSerializer

        SERIALNO = self.SERIALNO.strip()
        machineInfo = await sync_to_async(lambda: POS_Terminal.objects.filter(Serial_no=SERIALNO).first())()
        if machineInfo:
            if action == 'Delete':
                data = data.get('data')
               
            elif action == 'Update':
                data = data.get('data')
  
            else:
                last_data = await sync_to_async(
                    lambda: PosExtended.objects.filter(serial_no=machineInfo.Serial_no.strip()).last()
                )()
                serializer = PosExtendedSerializer(last_data,many=False)
                data = serializer.data

        # Broadcast only within this SERIALNO group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "pos_extended_monitor",  # must match handler name
                "newData": data,
                "action": action,
            }
        )

    async def pos_extended_monitor(self, event):
        await self.send(text_data=json.dumps({
            "type": "extended_monitor",
            "newData": event["newData"],
            "action": event["action"],
        }))



from channels.generic.websocket import AsyncWebsocketConsumer
import json

class LoginSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.SERIALNO = self.scope['url_route']['kwargs']['SERIALNO']
        self.room_group_name = f"login_updates_{self.SERIALNO}"

        self.user = self.scope['user']
        if isinstance(self.user, AnonymousUser) or self.user is None:

            await self.close()  # Immediately close connection
            return
        # Add to group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if not isinstance(self.user, AnonymousUser) and self.user is not None:
            from .models import PosCashiersLogin
            from .views import GetPHilippineDateTime


            # Example: mark user as logged out
            await database_sync_to_async(PosCashiersLogin.objects.filter(
                id_code=self.user.id_code,
                islogout ='NO',
            ).update)(islogout='YES',time_logout=GetPHilippineDateTime())
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )



    async def receive(self, text_data):
        data = json.loads(text_data)

        if data.get('action') == 'Login':
            # Lazy import models here
            from .models import POS_Terminal, PosExtended
            from .serializers import PosExtendedSerializer

            SERIALNO = self.SERIALNO.strip()
            machineInfo = await sync_to_async(lambda: POS_Terminal.objects.filter(Serial_no=SERIALNO).first())()
            if machineInfo:
               data_list = await sync_to_async(lambda: list(PosExtended.objects.filter(serial_no=machineInfo.Serial_no.strip())))()
               serializer = PosExtendedSerializer(data_list,many=True)
               data = serializer.data


            # Broadcast only to this SERIALNO group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    "type": "pos_login",
                    "newData": data,
                    "action": 'Login',
                }
            )

    async def pos_login(self, event):

        await self.send(text_data=json.dumps({
            "type": "login",
            "newData": event["newData"],
            "action": event["action"],
        }))



class LogoutSocket(AsyncWebsocketConsumer):
    async def connect(self):
        self.SERIALNO = self.scope['url_route']['kwargs']['SERIALNO']
        self.room_group_name = f"logout_updates_{self.SERIALNO}"  # group per serial

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        SERIALNO = data.get("SERIALNO")

        # Broadcast only within this SERIALNO group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "pos_logout",
                "SERIALNO": SERIALNO,
            }
        )

    async def pos_logout(self, event):
        await self.send(text_data=json.dumps({
            "type": "logout",
            "SERIALNO": event["SERIALNO"],
        }))
