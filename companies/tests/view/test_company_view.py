
def test_ping(client):
        response_valid = client.get("/companies/ping")
        assert response_valid.json == "Pong"