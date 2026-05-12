from urllib.parse import quote


def test_unregister_success_removes_participant(client):
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {email} from {activity_name}"
    }

    activities = client.get("/activities").json()
    assert email not in activities[activity_name]["participants"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    activity_name = "Unknown Club"
    email = "student@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_missing_participant_returns_404(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-enrolled@mergington.edu"
    encoded_activity = quote(activity_name, safe="")

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister",
        params={"email": email},
    )

    # Assert
    assert response.status_code == 404
    assert response.json() == {"detail": "Participant not found in this activity"}


def test_unregister_only_mutates_target_activity(client):
    # Arrange
    target_activity = "Drama Club"
    email = "grace@mergington.edu"
    encoded_activity = quote(target_activity, safe="")
    before = client.get("/activities").json()

    # Act
    response = client.delete(
        f"/activities/{encoded_activity}/unregister",
        params={"email": email},
    )
    after = client.get("/activities").json()

    # Assert
    assert response.status_code == 200
    assert email not in after[target_activity]["participants"]

    for activity_name, details in before.items():
        if activity_name == target_activity:
            continue
        assert after[activity_name]["participants"] == details["participants"]
