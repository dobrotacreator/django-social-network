from celery import shared_task

from django_social.settings import ses
from pages.models import Page


@shared_task(queue='post_notification', routing_key='post_notification')
def send_post_notification(page_uuid: str, post_content: str) -> int:
    page: Page = Page.objects.get(uuid=page_uuid)
    followers = page.followers.all()
    recipients = [follower.email for follower in followers]

    message = f"New post on {page.name}\nContent:\n\n{post_content}"
    sender = "noreply@example.com"  # Replace with your desired sender email

    response = ses.send_raw_email(
        Source=sender,
        Destinations=recipients,
        RawMessage={'Data': message}
    )

    return response['MessageId']
