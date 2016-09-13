import os
import pusher

CHANNEL = "response-updates"

client = pusher.Pusher(
    app_id=os.environ["PUSHER_APP_ID"],
    key=os.environ["PUSHER_KEY"],
    secret=os.environ["PUSHER_SECRET"],
    cluster='eu',
    ssl=True
)


def notify(msg_type, payload):
    """Notifies that a SurveyResponse has been created or modified"""

    client.trigger(CHANNEL, msg_type, payload)
