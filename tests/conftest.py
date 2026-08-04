from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(scope="session")
def activities_baseline():
    return deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def reset_activities(activities_baseline):
    app_module.activities = deepcopy(activities_baseline)
    yield
    app_module.activities = deepcopy(activities_baseline)


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
