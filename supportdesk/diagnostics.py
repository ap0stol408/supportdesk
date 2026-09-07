import os


def snapshot() -> dict[str, object]:
    return {"environment": dict(os.environ), "pid": os.getpid()}
