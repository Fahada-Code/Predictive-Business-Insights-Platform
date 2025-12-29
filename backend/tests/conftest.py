import pytest
import os
import shutil
from fastapi.testclient import TestClient
from app.main import app

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def setup_data_dir():
    # Ensure data directory exists
    data_dir = "data"
    os.makedirs(data_dir, exist_ok=True)
    yield
    # Cleanup after tests (optional, safe to keep for debugging)
    # shutil.rmtree(data_dir)

@pytest.fixture
def sample_csv():
    content = "ds,y\n2023-01-01,100\n2023-01-02,110\n2023-01-03,105"
    filename = "data/test_sample.csv"
    os.makedirs("data", exist_ok=True)
    with open(filename, "w") as f:
        f.write(content)
    return filename
