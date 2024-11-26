from unittest import TestCase
from rest_framework import status
from rest_framework.test import RequestsClient

class TestViews(TestCase):

# =================================================================================
#USERS

    def setUp(self):
        self.base_url = 'http://127.0.0.1:8000/api/v1/'
        self.user_client = RequestsClient()
        self.project = RequestsClient()
        self.task = RequestsClient()
        self.token = ''


    # def test_registations(self):
    #     response = self.user_client.post(self.base_url + 'signup/',
    #                                     data={"username": "taesfdfgeterjuser", 
    #                                         "password": "1234567890123", 
    #                                         "email": "aa@mail.ru"})
    #     self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_log_in(self):
        response = self.user_client.post(self.base_url + 'login/',
                                        data={"username": "testuser", 
                                            "password": "1234567890123", 
                                            "email": "a@mail.ru"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_log_out(self):
        login_response = self.user_client.post(self.base_url + 'login/',
                                            data={"username": "testuser", 
                                                "password": "1234567890123", 
                                                "email": "a@mail.ru"})
        self.assertEqual(login_response.status_code, status.HTTP_200_OK)

        self.token = login_response.json()['data']['user_token']

        logout_response = self.user_client.post(self.base_url + 'logout/',
                                            headers={"Authorization":
                                                        f"Bearer {self.token}"})
        self.assertEqual(logout_response.status_code, status.HTTP_200_OK)


    def test_get_users(self):
        response = self.user_client.get(self.base_url + 'users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# =============================================================================
# PROJECTS

    def test_create_project(self):
        response =  self.project.post(self.base_url + 'projects/', 
                                    data={"title": "project1"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_project(self):
        response = self.project.get(self.base_url + 'projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# =============================================================================
# TASKS

    def test_create_task(self):
        response = self.task.post(url= self.base_url + 'tasks/',
                            data={"title": "Новая задача",
                                "status": "Active",
                                "priority": "High",
                                "dead_line": "2023-12-31",
                                "project": [1, 2],})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_get_task(self):
        response = self.task.get(url=self.base_url + 'task/1/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
