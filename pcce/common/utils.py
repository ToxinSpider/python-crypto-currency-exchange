import uuid


def flat_uuid() -> str:
    return str(uuid.uuid4()).replace('-', '')
