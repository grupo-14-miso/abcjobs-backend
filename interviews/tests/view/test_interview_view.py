
def test_ping(client):
        response_valid = client.get("/interviews/ping")
        assert response_valid.json == "Pong"