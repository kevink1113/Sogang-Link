from firebase_admin import messaging

def send_topic_notification(topic, title, body, data=None):
    """
    FCM 토픽 푸시 알림을 보냅니다.

    :param topic: FCM 토픽 이름
    :param title: 알림 제목
    :param body: 알림 내용
    :param data: 추가 데이터 (선택 사항)
    """
    print('Sending topic notification to', topic)
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        topic=topic,
        data=data if data else {},
    )

    response = messaging.send(message)
    print('Successfully sent message:', response)