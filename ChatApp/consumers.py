from channels.consumer import SyncConsumer, AsyncConsumer
from channels.generic.websocket import (
    WebsocketConsumer, 
    AsyncWebsocketConsumer,
    JsonWebsocketConsumer,
    AsyncJsonWebsocketConsumer,
)

from channels.db import database_sync_to_async ## মুলত Channel Layout Django ORM support করে না, তাই এর সাহায্যে তা support করানো হয়েছে।
from channels.exceptions import StopConsumer

from ChatApp.models import Group, Chat

from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync ## এর মাধ্যমে async এর সকল Proparty কে sync এ ব্যবহার করার যায়


## NOTE Channel Layer -> দুটি বা multiple Instance নিজেদের মধ্যে জাতে Communicate করতে পারে তার জন্যে Channel Layer ব্যবহার করা হয়।


class MyJsonWebsocketConsumer(JsonWebsocketConsumer):

    def connect(self):
        print("Connect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## To Accept Connection
        self.accept()

        ## To Reject Connection
        # self.close()

        ## Group name is receive from frontend
        self.groupName = self.scope['url_route']['kwargs']['group_name']
        # print("Group Name = ", self.groupName)

        ## NOTE Add a channel to a new or existing group
        async_to_sync(self.channel_layer.group_add)(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )




    def receive_json(self, content, **kwargs):
        print("------------------------------------")
        print("Receive...........")
        print("Msg Receive = ", content)
        print("------------------------------------")

        ## To send message by Server
        # self.send_json({"message":"Message is receive by server."})

        data = content
        ## Find Group Object (If find then go else create group)
        group = Group.objects.get(name = self.groupName)

        if self.scope['user'].is_authenticated:
            ## Create a new chat object
            chat = Chat(
                group = group,
                user = self.scope['user'],
                content = data['msg'],
            ).save()

            ## username msg এর সাথে fontend এ show করানোর জন্যে একটি variable এ store করা হয়েছে
            data['user'] = self.scope['user'].username
            # print("---------------------------")
            # print("Data = ", python_dic)
            # print("---------------------------")

        ## Display the massage in user chat page
            async_to_sync(self.channel_layer.group_send)(
                self.groupName,{
                    'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                    'message': data,
                }
            )
        else:
            self.send_json({
                "msg": "Login Required", 
                "user": "unknown",
                })

    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায়গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    def chat_message(self, event):  
        print('Event....', event)
        print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        self.send_json({
            'msg':event['message'],
        })




    def disconnect(self, close_code):
        print("Disconnect...........", close_code)
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        












class MyAsyncJsonWebsocketConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):
        print("Connect...........")
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)

        ## To Accept Connection
        await self.accept()

        ## To Reject Connection
        # await self.close()

        ## Group name is receive from frontend
        self.groupName = self.scope['url_route']['kwargs']['group_name']
        print("Group Name = ", self.groupName)

        ## NOTE Add a channel to a new or existing group
        await self.channel_layer.group_add(
            # 'Bangladesh',   # Group Name
            self.groupName,   # Group Name
            self.channel_name
        )




    async def receive_json(self, content, **kwargs):
        print("------------------------------------")
        print("Receive...........")
        print("Msg Receive = ", content)
        print("------------------------------------")

        ## To send Maggage by Server
        await self.send_json({"message":"Maggage is received by server."})

        ## To Reject Connection
        # await self.close(code=4045) # error show by custome code 

        data = content

        ## এখানে Group obj find করা হয়েছে জাগে আমরা সেই Group এর Chat Table এ ঐ massage গুলো save করাতে পারি।
        # if Group.objects.filter(name = self.groupName).exists():
        group = await database_sync_to_async(Group.objects.get)(name = self.groupName)

        if self.scope['user'].is_authenticated:
            chat = Chat(
                group = group,
                user = self.scope['user'],
                content = data['msg'],
            )
            await database_sync_to_async(chat.save)()

            ## username msg এর সাথে fontend এ show করানোর জন্যে একটি variable এ store করা হয়েছে
            data['user'] = self.scope['user'].username

            await self.channel_layer.group_send(
                self.groupName,{
                    'type': 'chat.message',   # Chat Message Hendler টি নিচে Creat করা হয়েছে
                    'message': data,
                }
            )
        else:
            await self.send_json({
                "msg": "Login Required", 
                "user": "unknown",
                })
            

    ## Chat Message Event Hendler টি Create করার জন্যে . এর যায় গায় শুধু _ দিতে হবে chat.message কে chat_message লিখতে হবে।
    async def chat_message(self, event):  
        # print('Event....', event)
        # print('Data', event['message']) # Data type is string 

        # এখন আমাদের এই data টি কে Text area তে দেখাতে চাইলে তা Send করতে হবে
        await self.send_json({
            'msg':event['message']
        })
                



    async def disconnect(self, close_code):
        print("Disconnect...........", close_code)
        print("Channel Layer = ", self.channel_layer)  
        print("Channel Name = ", self.channel_name)
