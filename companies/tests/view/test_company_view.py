
def test_ping(client):
        response_valid = client.get("/company/ping")
        assert response_valid.json == "Pong"