def handle_on_message(client, message):
    print("handling message")


def handle_on_ready(client):
    print('We have logged in as {0.user}'.format(client))
