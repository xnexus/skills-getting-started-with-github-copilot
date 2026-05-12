from urllib.parse import quote


def test_signup_success_adds_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {email} for {activity_name}"
    }

    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]


def test_signup_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_duplicate_participant_returns_400(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_signup_only_mutates_target_activity(client):
    # Arrange
    target_activity = "Tennis Club"
    email = "focused-change@mergington.edu"
    encoded_activity = quote(target_activity, safe="")
    before = client.get("/activities").json()

    # Act
    response = client.post(
        f"/activities/{encoded_activity}/signup",
        params={"email": email},
    )
    after = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert email in after[target_activity]["participants"]

    for activity_name, details in before.items():
        if activity_name == target_activity:
            continue
        assert after[activity_name]["participants"] == details["participants"]
