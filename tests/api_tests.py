import unittest
import requests


class TestApiOptionA(unittest.TestCase):

    def setUp(self):
        self.total_pages = 2
        self.pagination = []
        self.urls = []
        self.request_responses = []
        self.bodies = []
        for x in range(self.total_pages):
            self.pagination.append(x + 1)
            self.paginated_url = 'https://reqres.in/api/users?page={}'.format(self.pagination[x])
            self.urls.append(self.paginated_url)
            self.response = requests.get(self.paginated_url)
            self.request_responses.append(self.response)
            self.body = self.response.json()
            self.bodies.append(self.body)
            # print(self.urls)

    def test_get_pages(self):
        for x in range(len(self.urls)):
            print(self.urls[x])
            print(self.request_responses[x])
            print(self.bodies[x])

    # validates the 'main attributes' in the response ('page', 'per_page', 'total', 'total_pages', and that 'data' is
    # filled)
    def test_api_list_users(self):
        for x in range(len(self.urls)):
            assert self.request_responses[x].status_code == 200
            assert len(self.bodies[x]["data"]) > 0
            assert self.bodies[x]["page"] == self.pagination[x]
            assert self.bodies[x]["per_page"] == 6
            assert self.bodies[x]["total_pages"] == self.total_pages
            print(self.bodies[x])

    # asserts 'data' list, that its attributes are present and not empty
    def test_api_list_users_data(self):
        for x in range(len(self.bodies)):
            data = self.bodies[x]["data"]
            for data_index in data:
                assert len(data_index) == 5
                for j in data_index.values():
                    assert j is not None


class TestApiOptionB(unittest.TestCase):

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
            assert response_body["total_pages"] == len(pages)

    def test_api_list_users_data(self):
        for x in self.pages:
            url = self.get_url.format(x)
            response = requests.get(url)
            response_body = response.json()
            data = response_body["data"]
            for data_index in data:
                print(data_index)


if __name__ == '__main__':
    unittest.main()