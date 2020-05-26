#!/usr/bin/env python
#
# Semaphore: A simple (rule-based) bot library for Signal Private Messenger.
# Copyright (C) 2020
# Lazlo Westerhof <semaphore@lazlo.me>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser Public License for more details.
#
# You should have received a copy of the GNU Lesser Public License
# along with this program.  If not, see [http://www.gnu.org/licenses/].
"""This class handles sending bot messages."""
from typing import Any, Dict

from .message import Message
from .reply import Reply
from .socket import Socket


class MessageSender:
    def __init__(self, username: str, socket: Socket):
        self._username: str = username
        self._socket: Socket = socket

    def _send(self, message: Dict) -> None:
        self._socket.send(message)

    def send_message(self, message: Message, reply: Reply) -> None:
        """
        Send the bot message.

        recipient:          The recipient's phone number.
        reply:              The reply to send.
        recipient_group_id: Group id if recicpient is a group.
        """
        # Construct reply message.
        bot_message: Dict[str, Any] = {"type": "send",
                                       "username": self._username,
                                       "recipientNumber": message.source,
                                       "messageBody": reply.message}

        # Add group id for group messages.
        if message.get_group_id():
            bot_message["recipientGroupId"] = message.get_group_id()

        # Add attachments to message.
        if reply.attachments:
            bot_message["attachments"] = reply.attachments

        # Add quote to message.
        if reply.quote:
            quote = {"id": message.timestamp,
                     "author": message.source,
                     "text": message.get_text()}
            bot_message["quote"] = quote

        self._send(bot_message)

    def mark_read(self, message: Message) -> None:
        """
        Mark a Signal message you received as read.

        message: The Signal message you received.
        """
        self._send({"type": "mark_read",
                    "username": self._username,
                    "recipientNumber": message.source,
                    "timestamps": [message.timestamp]})