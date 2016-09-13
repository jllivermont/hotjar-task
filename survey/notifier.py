import os
import pusher

CHANNEL = "response-updates"

client = pusher.Pusher(
    app_id=os.environ.get("PUSHER_APP_ID"),
    key=os.environ.get("PUSHER_KEY"),
    secret=os.environ.get("PUSHER_SECRET"),
    cluster='eu',
    ssl=True
) if "IS_PROD" in os.environ else None


def notify(msg_type, payload):
    """Notifies that a SurveyResponse has been created or modified"""

    if client is not None:
        client.trigger(CHANNEL, msg_type, payload)
