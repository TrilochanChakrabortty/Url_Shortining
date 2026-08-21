
# realuse case for users

from locust import HttpUser, task, constant


class LoginUser(HttpUser):

    wait_time = constant(0)

    @task
    def login(self):

        with self.client.post(
            "/auth/login",
            json={
                "username": "username",
                "password": "abcd1234"
            },
            catch_response=True
        ) as response:

            if response.status_code == 200:

                response.success()

            else:

                response.failure(
                    f"Login failed: {response.status_code}"
                )

from locust import HttpUser, task, constant
import uuid


class ShortenUser(HttpUser):

    wait_time = constant(0)

    # ----------------------------------------------------
    # LOGIN ONCE WHEN EACH LOCUST USER STARTS
    # ----------------------------------------------------

    def on_start(self):

        response = self.client.post(
            "/auth/login",
            json={
                "username": "username",
                "password": "abcd1234"
            }
        )

        if response.status_code == 200:

            data = response.json()

            self.headers = {
                "Authorization": (
                    f"Bearer {data['access_token']}"
                )
            }

        else:

            print(
                f"Login failed: {response.status_code}"
            )

            self.headers = {}

    # ----------------------------------------------------
    # SHORTEN UNIQUE URL
    # ----------------------------------------------------

    @task
    def shorten_url(self):

        # Generate a unique URL for every request
        unique_url = (
            f"https://performance-test.com/"
            f"{uuid.uuid4()}"
        )

        with self.client.post(
            "/shorten",
            json={
                "url": unique_url
            },
            headers=self.headers,
            catch_response=True,
        ) as response:

            if response.status_code == 200:

                response.success()

            else:

                response.failure(
                    f"Shorten failed: "
                    f"{response.status_code} - "
                    f"{response.text}"
                )

from locust import HttpUser, task, constant
import uuid


class ShortenUser(HttpUser):

    wait_time = constant(1)

    # ========================================================
    # LOGIN WHEN EACH LOCUST USER STARTS
    # ========================================================

    def on_start(self):

        self.token = None

        with self.client.post(
            "/auth/login",
            json={
                "username": "",
                "password": "abcd1234"
            },
            catch_response=True
        ) as response:

            print("\n========== LOGIN DEBUG ==========")
            print("STATUS CODE:", response.status_code)
            print("RAW RESPONSE:", response.text)

            if response.status_code == 200:

                try:

                    data = response.json()

                    print("PARSED RESPONSE:", data)

                    self.token = data.get(
                        "access_token"
                    )

                    print(
                        "ACCESS TOKEN EXISTS:",
                        self.token is not None
                    )

                    if self.token:

                        print(
                            "TOKEN PREVIEW:",
                            self.token[:50]
                        )

                        print("LOGIN SUCCESSFUL")

                        response.success()

                    else:

                        print(
                            "ERROR: access_token key not found"
                        )

                        response.failure(
                            "Access token missing"
                        )

                except Exception as e:

                    print(
                        "JSON PARSE ERROR:",
                        repr(e)
                    )

                    response.failure(
                        "Could not parse login response"
                    )

            else:

                print("LOGIN REQUEST FAILED")

                response.failure(
                    f"Login failed: "
                    f"{response.status_code}"
                )

            print("=================================\n")


    # ========================================================
    # SHORTEN URL
    # ========================================================

    @task
    def shorten_url(self):

        # Do not send request if login/token failed
        if not self.token:

            print("SHORTEN SKIPPED: NO VALID TOKEN")

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
                "Authorization": (
                    f"Bearer {self.token}"
                )
            },
            catch_response=True
        ) as response:

            print(
                "SHORTEN STATUS:",
                response.status_code
            )

            if response.status_code == 200:

                response.success()

            else:

                print(
                    "SHORTEN RESPONSE:",
                    response.text
                )

                response.failure(
                    f"Shorten failed: "
                    f"{response.status_code}"
                )