import pytest
from backend.app import create_app


@pytest.fixture
def contextual_app(cfg, contextual_queue):
    """Create an app which can handle EVENT message publish on the contextual_queue.
    This fixture is used in the messaging tests suite to isolate the tests each other.
    """
    from backend.config import load_config_as_object

    conf = load_config_as_object(cfg)
    return create_app(conf)
