from channels.layers import get_channel_layer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


async def send_message(layer_name, type, message, user):
    """sending a message to a channel"""
    channel_layer = get_channel_layer()
    await channel_layer.group_send(layer_name, {
        'type': 'message_for_user',
        'data': {
            'method': type,
            'message': message,
            'sender_username': user.username,
            'sender_id': user.id
        }
    })


async def send_message_for_users(message, user, ids=None):
    if ids is None:
        ids = await get_user_ids()
    for id in ids:
        await send_message(
            'user_' + str(id),
            'private',
            message,
            user
        )


@database_sync_to_async
def get_user_ids():
    return list(User.objects.all().values_list("id", flat=True))

@database_sync_to_async
def get_user_by_token(token):
    return Token.objects.get(key=token).user
