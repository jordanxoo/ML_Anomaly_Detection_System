import json

async def test_register(client):
    response = await client.post("/auth/register", json={
        "username" : "test",
        "password": "test",
        "email": "email@test.com"
    })

    print(response.json())
    assert response.status_code == 200


async def test_login(client):

    await client.post("/auth/register",json={"username" : "test_login",
                                             "password": "test_login",
                                             "email" : "test@email.com"})

    response = await client.post("/auth/login",data={"username" : "test_login",
                                                     "password" : "test_login"})
    
    body = response.json()
    assert response.status_code == 200 and body["access_token"] != None

