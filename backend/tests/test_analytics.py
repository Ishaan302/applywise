def test_stats_shape(client, auth_headers):
    r = client.get("/analytics/stats", headers=auth_headers)
    assert r.status_code == 200
    data = r.json()
    assert "total_applications" in data
    assert "response_rate" in data
    assert "interview_conversion_rate" in data

def test_response_rate_calculation(client, auth_headers):
    client.post("/applications", json={"company": "X", "role": "A", "status": "Interview"}, headers=auth_headers)
    client.post("/applications", json={"company": "Y", "role": "B", "status": "Applied"}, headers=auth_headers)
    r = client.get("/analytics/stats", headers=auth_headers)
    assert r.json()["response_rate"] > 0