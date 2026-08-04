from src import app as app_module


def test_get_activities_returns_known_activity(client):
    # Arrange
    path = "/activities"

    # Act
    response = client.get(path)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload


def test_signup_success_adds_participant(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"
    new_email = "new.student@mergington.edu"

    # Act
    response = client.post(activity_path, params={"email": new_email})

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {new_email} for Chess Club"
    }
    assert new_email in app_module.activities["Chess Club"]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_path = "/activities/Unknown%20Club/signup"
    email = "someone@mergington.edu"

    # Act
    response = client.post(activity_path, params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_email_returns_400(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(activity_path, params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_missing_email_returns_422(client):
    # Arrange
    activity_path = "/activities/Chess%20Club/signup"

    # Act
    response = client.post(activity_path)

    # Assert
    assert response.status_code == 422
