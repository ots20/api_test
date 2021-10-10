import unittest
import requests


class TestApi(unittest.TestCase):

    def test_api_list_users(self):
        pages = [1, 2]
        for index in pages:
            post_url = 'https://reqres.in/api/users?page={}'.format(index)
            response = requests.get(post_url)
            response_body = response.json()
            assert response.status_code == 200
            assert len(response_body["data"]) > 0
            assert response_body["page"] == index
            assert response_body["per_page"] == 6
            assert response_body["total_pages"] == len(pages)
            print(len(response_body["data"]))


if __name__ == '__main__':
    unittest.main()