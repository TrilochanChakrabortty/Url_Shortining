
# # realuse case for users

# from locust import HttpUser, task, constant


# class LoginUser(HttpUser):

#     wait_time = constant(0)

#     @task
#     def login(self):

#         with self.client.post(
#             "/auth/login",
#             json={
#                 "username": "username",
#                 "password": "abcd1234"
#             },
#             catch_response=True
#         ) as response:

#             if response.status_code == 200:

#                 response.success()

#             else:

#                 response.failure(
#                     f"Login failed: {response.status_code}"
#                 )

from locust import HttpUser, task, constant
import uuid


class ShortenUser(HttpUser):

    wait_time = constant(1)

    # ========================================================
    # LOGIN ONCE WHEN EACH LOCUST USER STARTS
    # ========================================================

    def on_start(self):

        self.token = None

        with self.client.post(
            "/auth/login",
            json={
                "username": "Trilochan",
                "password": "abcd1234"
            },
            catch_response=True
        ) as response:

            if response.status_code == 200:

                try:
                    data = response.json()

                    self.token = data.get("access_token")

                    if self.token:
                        response.success()
                    else:
                        response.failure(
                            "Login successful but access_token missing"
                        )

                except Exception as e:
                    response.failure(
                        f"Invalid login response: {e}"
                    )

            else:
                response.failure(
                    f"Login failed: {response.status_code}"
                )

    # ========================================================
    # SHORTEN UNIQUE URL
    # ========================================================

    @task
    def shorten_url(self):

        if not self.token:
            return

        unique_url = (
            f"https://performance-test.com/"
            f"{uuid.uuid4()}"
        )

        with self.client.post(
            "/shorten",
            json={
                "url": unique_url
            },
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            catch_response=True
        ) as response:

            if response.status_code == 200:

                response.success()

            else:

                if response.status_code == 401:
                    print(
                        "\nAUTH ERROR:"
                        "\nToken was rejected by /shorten"
                        "\nResponse:",
                        response.text
                    )

                response.failure(
                    f"Shorten failed: {response.status_code}"
                )