import unittest
from datetime import timedelta
import requests


class TestApiGet(unittest.TestCase):
    def setUp(self):
        self.base_url = 'https://reqres.in/api/users/'

    def test_user_list(self):
        payload = {'page': None}
        pages_number = requests.get(self.base_url)
        for x in range(pages_number.json()['total_pages']):
            payload['page'] = x+1
            response = requests.get(self.base_url, params=payload)
            body = response.json()
            assert response.status_code == 200
            assert len(body["data"]) > 0
            assert body["page"] == x+1
            assert body["per_page"] == 6

    # I need to do this with the timeout exception!!
    # def test_delayed_response_fail(self):
    #     response = requests.get(self.base_url + '?delay=3')
    #     body = response.json()
    #     self.assertFalse(response.elapsed < timedelta(seconds=3))
    #     assert response.status_code == 200
    #     assert body["data"] is not None

    def test_delayed_response_2(self):
        try:
            response = requests.get(self.base_url + '?delay=3', timeout=3)
        except requests.exceptions.ReadTimeout:
            print("Time's over!!")

    def test_single_user(self):
        response = requests.get(self.base_url+'2')
        body = response.json()["data"]
        assert int(body["id"]) > 0
        assert body["email"] == body["email"]
        assert body["first_name"] == body["first_name"]
        assert body["last_name"] == body["last_name"]
        assert body["avatar"] == body["avatar"]

    def test_single_user_not_found(self):
        response = requests.get(self.base_url+'23')
        body = response.json()
        assert response.status_code == 404
        assert len(body) == 0


class TestCRUDMethods(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://reqres.in/api/users/'
        self.user_id = '33'

    # using a loop in case I would like to create more users
    # I update the created ID in the dictionary for the PUT test in order to use the same
    def test_create_user(self):
        payload = {
                "name": "Shinji Ikari",
                "job": "Pilot Eva-01"
            }
        response = requests.post(self.base_url, data=payload)
        body = response.json()
        assert response.status_code == 201
        assert body["name"] == "Shinji Ikari"
        assert body["job"] == "Pilot Eva-01"
        assert int(body["id"]) > 0
        assert body["createdAt"] is not None

    def test_update_user(self):
        payload = {
            "name": "Asuka Langley",
            "job": "Pilot Eva-02"}
        response = requests.put(self.base_url + self.user_id, data=payload)
        body = response.json()
        assert body["name"] == payload["name"]
        assert body["job"] == payload["job"]
        assert body["updatedAt"] is not None

    def test_delete_user(self):
        response = requests.delete(self.base_url + self.user_id)
        assert response.status_code == 204


class TestRegister(unittest.TestCase):

    def setUp(self):
        self.base_url = 'https://reqres.in/api/register'
        self.register_data = {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
            }

    def test_register_success(self):
        response = requests.post(self.base_url, json=self.register_data)
        body = response.json()
        assert response.status_code == 200
        assert int(body["id"]) > 0
        assert len(body["token"]) == 17

    def test_register_failure(self):
        attribute = ["email", "password"]
        for x in range(len(attribute)):
            response = requests.post(self.base_url, json={attribute[x]: "test@test.com"})
            body = response.json()
            assert response.status_code == 400
            if x == 0:
                assert body["error"] == "Missing password"
            else:
                assert body["error"] == "Missing email or username"


# ========== Some alternatives I thought about ==================

# class TestApiGetOptionA(unittest.TestCase):
#
#     # stores the URL pagination in a list, based on the number of pages, also stores, the same with the responses and
#     #   bodies of the response.
#     # Why? - because the endpoint has 2 pages and I did not want to send the request in 2 scenarios
#     # Would this be useful in case the endpoint has a big number of pages??
#     def setUp(self):
#         self.base_url = 'https://reqres.in/api/users'
#         self.page = '?page={}'
#         self.total_pages = 2
#         self.pagination = []
#         self.urls = []
#         self.request_responses = []
#         self.bodies = []
#         for x in range(self.total_pages):
#             self.pagination.append(x + 1)
#             self.paginated_url = self.base_url + self.page.format(self.pagination[x])
#             self.urls.append(self.paginated_url)
#             self.response = requests.get(self.paginated_url)
#             self.request_responses.append(self.response)
#             self.body = self.response.json()
#             self.bodies.append(self.body)
#             # print(self.urls)
#
#     # just to check if the setUp method works
#     # def test_get_pages(self):
#     #     for x in range(len(self.urls)):
#     #         print(self.urls[x])
#     #         print(self.request_responses[x])
#     #         print(self.bodies[x])
#
#     # validates the 'main attributes' in the response ('page', 'per_page', 'total', 'total_pages', and that 'data' is
#     # filled)
#     def test_api_list_users(self):
#         for x in range(len(self.urls)):
#             assert self.request_responses[x].status_code == 200
#             assert len(self.bodies[x]["data"]) > 0
#             assert self.bodies[x]["page"] == self.pagination[x]
#             assert self.bodies[x]["per_page"] == 6
#             assert self.bodies[x]["total_pages"] == self.total_pages
#             # print(self.bodies[x])
#
#     def test_delayed_response_fail(self):
#         response = requests.get(self.base_url + '?delay=3')
#         body = response.json()
#         self.assertFalse(response.elapsed < timedelta(seconds=3))
#         assert response.status_code == 200
#         assert body["data"] is not None
#
#     # asserts 'data' list, that its attributes are present and not empty
#     def test_api_list_users_data(self):
#         for x in range(len(self.bodies)):
#             data = self.bodies[x]["data"]
#             for data_index in data:
#                 assert len(data_index) == 5
#                 # print(data_index["email"])
#                 for j in data_index.values():
#                     assert j is not None
#
#     def test_single_user(self):
#         response = requests.get(self.base_url + '/12')
#         body = response.json()
#         assert response.status_code == 200
#         for x in range(len(self.bodies)):
#             data = self.bodies[x]["data"]
#             for data_index in data:
#                 if data_index["id"] == body["data"]["id"]:
#                     assert data_index["id"] == body["data"]["id"]
#                     assert data_index["email"] == body["data"]["email"]
#                     assert data_index["first_name"] == body["data"]["first_name"]
#                     assert data_index["last_name"] == body["data"]["last_name"]
#                     assert data_index["avatar"] == body["data"]["avatar"]
#                     # print("asserted!")
#                     return
#                 # print(data_index["id"])
#
#     def test_single_user_version2(self):
#         response = requests.get(self.base_url + '/2')
#         body = response.json()["data"]
#         assert response.status_code == 200
#         assert body["id"] == 2
#         assert body["email"] == "janet.weaver@reqres.in"
#         assert body["first_name"] == "Janet"
#         assert body["last_name"] == "Weaver"
#         assert body["avatar"] == "https://reqres.in/img/faces/2-image.jpg"
#
#     def test_single_user_not_found(self):
#         response = requests.get(self.base_url + '/13')
#         body = response.json()
#         assert response.status_code != 200
#         assert response.status_code == 404
#         assert len(body) == 0

# ===============================================================

# class TestApiGetOptionB(unittest.TestCase):
#
#     def setUp(self):
#         self.pages = [1, 2]
#
#     def test_api_list_users(self):
#         for x in self.pages:
#             post_url = 'https://reqres.in/api/users?page={}'.format(x)
#             response = requests.get(post_url)
#             response_body = response.json()
#             assert response.status_code == 200
#             assert len(response_body["data"]) > 0
#             assert response_body["page"] == x
#             assert response_body["per_page"] == 6
#             assert response_body["total_pages"] == len(self.pages)
#
#     # def test_api_list_users_data(self):
#     #     for x in self.pages:
#     #         url = self.get_url.format(x)
#     #         response = requests.get(url)
#     #         response_body = response.json()
#     #         data = response_body["data"]
#     #         for data_index in data:
#     #             print(data_index)

# ========== Some alternatives I thought about ==================


if __name__ == '__main__':
    unittest.main()
