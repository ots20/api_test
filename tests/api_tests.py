import unittest
import requests


class TestApiGetOptionA(unittest.TestCase):

    # stores the URL pagination in a list, based on the number of pages, also stores, the same with the responses and
    #   bodies of the response.
    # Why? - because the endpoint has 2 pages and I did not want to send the request in 2 scenarios
    # Would this be useful in case the endpoint has a big number of pages??
    def setUp(self):
        self.base_url = 'https://reqres.in/api/users'
        self.page = '?page={}'
        self.total_pages = 2
        self.pagination = []
        self.urls = []
        self.request_responses = []
        self.bodies = []
        for x in range(self.total_pages):
            self.pagination.append(x + 1)
            self.paginated_url = self.base_url + self.page.format(self.pagination[x])
            self.urls.append(self.paginated_url)
            self.response = requests.get(self.paginated_url)
            self.request_responses.append(self.response)
            self.body = self.response.json()
            self.bodies.append(self.body)
            # print(self.urls)

    # just to check if the setUp method works
    # def test_get_pages(self):
    #     for x in range(len(self.urls)):
    #         print(self.urls[x])
    #         print(self.request_responses[x])
    #         print(self.bodies[x])

    # validates the 'main attributes' in the response ('page', 'per_page', 'total', 'total_pages', and that 'data' is
    # filled)
    def test_api_list_users(self):
        for x in range(len(self.urls)):
            assert self.request_responses[x].status_code == 200
            assert len(self.bodies[x]["data"]) > 0
            assert self.bodies[x]["page"] == self.pagination[x]
            assert self.bodies[x]["per_page"] == 6
            assert self.bodies[x]["total_pages"] == self.total_pages
            # print(self.bodies[x])

    # asserts 'data' list, that its attributes are present and not empty
    def test_api_list_users_data(self):
        for x in range(len(self.bodies)):
            data = self.bodies[x]["data"]
            for data_index in data:
                assert len(data_index) == 5
                # print(data_index["email"])
                for j in data_index.values():
                    assert j is not None

    def test_single_user(self):
        response = requests.get(self.base_url + '/12')
        body = response.json()
        assert response.status_code == 200
        for x in range(len(self.bodies)):
            data = self.bodies[x]["data"]
            for data_index in data:
                if data_index["id"] == body["data"]["id"]:
                    assert data_index["id"] == body["data"]["id"]
                    assert data_index["email"] == body["data"]["email"]
                    assert data_index["first_name"] == body["data"]["first_name"]
                    assert data_index["last_name"] == body["data"]["last_name"]
                    assert data_index["avatar"] == body["data"]["avatar"]
                    # print("asserted!")
                    return
                # print(data_index["id"])

    def test_single_user_version2(self):
        response = requests.get(self.base_url + '/2')
        body = response.json()
        assert response.status_code == 200
        assert body["data"]["id"] == 2
        assert body["data"]["email"] == "janet.weaver@reqres.in"
        assert body["data"]["first_name"] == "Janet"
        assert body["data"]["last_name"] == "Weaver"
        assert body["data"]["avatar"] == "https://reqres.in/img/faces/2-image.jpg"

    def test_single_user_not_found(self):
        response = requests.get(self.base_url + '/13')
        body = response.json()
        assert response.status_code != 200
        assert response.status_code == 404
        assert len(body) == 0


class TestCRUDMethods(unittest.TestCase):

    def setUp(self):
        print('setting up')
        self.base_url = 'https://reqres.in/api/users'
        self.user_id = '192'

    # using a loop in case I would like to create more users
    # I update the created ID in the dictionary for the PUT test in order to use the same
    def test_create_user(self):
        attributes_create = [{
            "name": "morpheus",
            "job": "leader"},
            {
                "name": "neo",
                "job": "chosen one"},
            {
                "name": "Shinji Ikari",
                "job": "pilot"
            }]
        for x in range(len(attributes_create)):
            response = requests.post(self.base_url, json=attributes_create[x])
            body = response.json()
            assert response.status_code == 201
            assert body["name"] == attributes_create[x]["name"]
            assert body["job"] == attributes_create[x]["job"]
            assert int(body["id"]) > 0
            assert body["createdAt"] is not None
            # print(body)

    def test_update_user(self):

        attributes_update = {
            "name": "morpheus",
            "job": "zion resident updated"}
        response = requests.put(self.base_url+self.user_id, json=attributes_update)
        body = response.json()
        print(attributes_update)
        print(body)

    def test_delete_user(self):
        response = requests.delete(self.base_url+self.user_id)
        assert response.status_code == 204



class TestApiGetOptionB(unittest.TestCase):

    def setUp(self):
        self.pages = [1, 2]

    def test_api_list_users(self):
        for x in self.pages:
            post_url = 'https://reqres.in/api/users?page={}'.format(x)
            response = requests.get(post_url)
            response_body = response.json()
            assert response.status_code == 200
            assert len(response_body["data"]) > 0
            assert response_body["page"] == x
            assert response_body["per_page"] == 6
            assert response_body["total_pages"] == len(self.pages)

    # def test_api_list_users_data(self):
    #     for x in self.pages:
    #         url = self.get_url.format(x)
    #         response = requests.get(url)
    #         response_body = response.json()
    #         data = response_body["data"]
    #         for data_index in data:
    #             print(data_index)


if __name__ == '__main__':
    unittest.main()
