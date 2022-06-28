from db.queque.current import EmailCheckerPublisher


def get_email_cheker_queue_publisher() -> EmailCheckerPublisher:
    return EmailCheckerPublisher()
