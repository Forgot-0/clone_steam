from fastapi_mail import MessageSchema, MessageType



def conver_event_created_developer_to_message_schema(subject: str, email: str, body: str):
    return MessageSchema(
        subject=subject,
        recipients=[email],
        body=body,
        subtype=MessageType.html
    )