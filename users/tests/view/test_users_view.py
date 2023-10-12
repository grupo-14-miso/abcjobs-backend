
def test_ping(client):
        response_valid = client.get("/users/ping")
        assert response_valid.json == "Pong"