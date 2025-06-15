import json
from datetime import datetime
import uuid

class A2AMessage:
    def __init__(self, from_agent, to_agent, message_type, content):
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.content = content
        self.timestamp = datetime.now().isoformat()
        self.message_id = str(uuid.uuid4())

        def to_dict(self):
            return {
                "timestamp": self.timestamp,
                "id": self.id,
                "from_agent": self.from_agent,
                "to_agent": self.to_agent,
                "message":{
                "type": self.message_type,
                "content": self.content
                }
            }

    def to_json(self):
        return json.dumps(self.to_dict(), indent=4)

    @staticmethod
    def from_dict(data):
        message = A2AMessage(
            from_agent=data["from_agent"],
            to_agent=data["to_agent"],
            message_type=data["message"]["type"],
            content=data["message"]["content"]
        )
        message.timestamp = data["timestamp"]
        message.message_id = data["id"]
        return message

    @staticmethod
    def from_json(json_str):
        return A2AMessage.from_dict(json.loads(json_str))
