from channels import DEFAULT_CHANNEL_LAYER
from channels_jsonrpc import AsyncJsonRpcWebsocketConsumer

from chats.services import get_user_by_token
from chats.services import send_message
from chats.services import send_message_for_users


class ChatConsumer(AsyncJsonRpcWebsocketConsumer):
    user_id = ""

    async def connect(self):
        token = self.scope['url_route']['kwargs']['token']
        user = await get_user_by_token(token)

        self.user_id = user.id

        # # Join room group
        await self.channel_layer.group_add(
            DEFAULT_CHANNEL_LAYER,
            self.channel_name
        )

        # # # Join self chat
        await self.channel_layer.group_add(
            'user_' + str(self.user_id),
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            DEFAULT_CHANNEL_LAYER,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            'user_' + str(self.user_id),
            self.channel_name
        )

    async def message_for_user(self, event):
        await self.send_json(event["data"])


@ChatConsumer.rpc_method()
async def chat(**kwargs):
    """public chat method"""
    message = kwargs["message"],
    token = kwargs["consumer"].scope['url_route']['kwargs']['token']
    user = await get_user_by_token(token)

    await send_message(DEFAULT_CHANNEL_LAYER, 'public', message, user)


@ChatConsumer.rpc_method()
async def sendMessage(**kwargs):
    """private chat method"""
    """{"id": 1, "jsonrpc": "2.0", "method": "sendMessage", "params": {ids:[], message:}}"""
    """
    {
      "jsonrpc": "2.0",
      "method": "sendMessage",
      "params": {
        "ids": "*", (or [ids])
        "message": "Hi"
      },
      "id": 1
    }
    """
    message = kwargs["message"],
    token = kwargs["consumer"].scope['url_route']['kwargs']['token']
    user = await get_user_by_token(token)

    if kwargs["ids"] == "*":
        await send_message_for_users(message, user)
    else:
        await send_message_for_users(message, user, kwargs["ids"])


@ChatConsumer.rpc_method()
async def sendEcho(**kwargs):
    """send private message  to yourself"""
    message = kwargs["message"],
    token = kwargs["consumer"].scope['url_route']['kwargs']['token']
    user = await get_user_by_token(token)
    await send_message('user_' + str(user.id), 'self', message, user)
