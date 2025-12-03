import requests


class Api:
    BASE_URL = "https://automationexercise.com/api"

    # --------------------------------------------------------------
    # Yhteinen apumetodi
    # --------------------------------------------------------------
    def _ensure_success_status_code(self, status_code: int) -> None:
        if not 200 <= status_code < 300:
            raise AssertionError(f"Expected 2xx status code, but got {status_code}")

    # --------------------------------------------------------------
    # API 5 – POST /searchProduct (haku parametrilla)
    # --------------------------------------------------------------
    def search_product(self, term: str) -> requests.Response:
        url = f"{self.BASE_URL}/searchProduct"
        payload = {"search_product": term}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response

    def search_product_json(self, term: str) -> dict:
        response = self.search_product(term)
        self._ensure_success_status_code(response.status_code)
        return response.json()

    def search_product_should_return_results(self, term: str) -> dict:
        data = self.search_product_json(term)
        if "products" not in data:
            raise AssertionError("Response JSON does not contain 'products' key.")
        if len(data["products"]) == 0:
            raise AssertionError(f"No products found for '{term}'")
        return data

    # --------------------------------------------------------------
    # API 6 – POST /searchProduct ilman search_product-parametria
    # --------------------------------------------------------------
    def search_product_without_parameter_should_return_400(self) -> dict:
        """
        POST /searchProduct ilman search_product-parametria.

        Odotetaan:
          - HTTP status 200
          - responseCode 400
          - oikea virheviesti.
        """
        url = f"{self.BASE_URL}/searchProduct"
        response = requests.post(url)

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 400:
            raise AssertionError(
                f"Expected responseCode 400, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = (
            "Bad request, search_product parameter is missing in POST request."
        )
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        return data

    # --------------------------------------------------------------
    # API 9 – DELETE /verifyLogin (ei sallittu metodi)
    # --------------------------------------------------------------
    def verify_login_delete_should_return_405(self) -> dict:
        url = f"{self.BASE_URL}/verifyLogin"
        response = requests.delete(url)

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP status code 200, but got {response.status_code}. "
                f"Response body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, but got {data.get('responseCode')}. "
                f"Full JSON: {data}"
            )

        expected_message = "This request method is not supported."
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', but got '{data.get('message')}'. "
                f"Full JSON: {data}"
            )

        return data

    # --------------------------------------------------------------
    # API 1 – GET /productsList
    # --------------------------------------------------------------
    def get_all_products(self) -> requests.Response:
        url = f"{self.BASE_URL}/productsList"
        return requests.get(url)

    def get_all_products_should_return_200(self) -> dict:
        response = self.get_all_products()
        if response.status_code != 200:
            raise AssertionError(
                f"Expected status 200, got {response.status_code}. Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if "products" not in data:
            raise AssertionError(f"'products' key missing. JSON: {data}")

        first = data["products"][0]
        for key in ("id", "name", "price"):
            if key not in first:
                raise AssertionError(
                    f"Missing key '{key}' in first product. Product: {first}"
                )

        return data

    # --------------------------------------------------------------
    # API 2 – POST /productsList
    # --------------------------------------------------------------
    def post_products_list(self) -> requests.Response:
        url = f"{self.BASE_URL}/productsList"
        return requests.post(url)

    def post_products_list_should_return_405(self) -> dict:
        response = self.post_products_list()
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200 wrapper, got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        return data

    # --------------------------------------------------------------
    # API 3 – GET /brandsList
    # --------------------------------------------------------------
    def get_all_brands(self) -> requests.Response:
        url = f"{self.BASE_URL}/brandsList"
        return requests.get(url)

    def get_all_brands_should_return_200(self) -> dict:
        response = self.get_all_brands()
        if response.status_code != 200:
            raise AssertionError(
                f"Expected status 200, got {response.status_code}. Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if "brands" not in data:
            raise AssertionError(f"'brands' key missing. JSON: {data}")

        return data

    # --------------------------------------------------------------
    # API 4 – PUT /brandsList
    # --------------------------------------------------------------
    def put_brands_list(self) -> requests.Response:
        url = f"{self.BASE_URL}/brandsList"
        return requests.put(url)

    def put_brands_list_should_return_405(self) -> dict:
        response = self.put_brands_list()
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200 wrapper, got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        return data

    # --------------------------------------------------------------
    # API 7 – POST /verifyLogin (validit tunnukset)
    # --------------------------------------------------------------
    def verify_login(self, email: str, password: str) -> requests.Response:
        """
        POST /verifyLogin email- ja password-parametreilla.
        """
        url = f"{self.BASE_URL}/verifyLogin"
        payload = {
            "email": email,
            "password": password,
        }
        return requests.post(url, data=payload)

    def verify_login_valid_should_return_200(self, email: str, password: str) -> dict:
        """
        API 7: POST To Verify Login with valid details

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 200
          - JSON message = 'User exists!'
        """
        url = f"{self.BASE_URL}/verifyLogin"
        response = self.verify_login(email, password)

        # HTTP-status
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        # JSON-parsiminen
        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        # JSON responseCode
        if data.get("responseCode") != 200:
            raise AssertionError(
                f"Expected responseCode 200, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = "User exists!"
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        # Tulostetaan description-tyylinen yhteenveto
        print("API 7: POST To Verify Login with valid details")
        print(f"API URL: {url}")
        print("Request Method: POST")
        print("Request Parameters: email, password")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 8 – POST /verifyLogin ilman email-parametria
    # --------------------------------------------------------------
    def verify_login_without_email(self, password: str) -> requests.Response:
        """
        POST /verifyLogin vain password-parametrilla (email puuttuu).
        """
        url = f"{self.BASE_URL}/verifyLogin"
        payload = {
            "password": password,  # email jätetään tarkoituksella pois
        }
        return requests.post(url, data=payload)

    def verify_login_without_email_should_return_400(self, password: str) -> dict:
        """
        API 8: POST To Verify Login without email parameter

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 400
          - JSON message = 'Bad request, email or password parameter is missing in POST request.'
        """
        url = f"{self.BASE_URL}/verifyLogin"
        response = self.verify_login_without_email(password)

        # HTTP-status
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        # JSON-parsiminen
        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        # JSON responseCode
        if data.get("responseCode") != 400:
            raise AssertionError(
                f"Expected responseCode 400, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = (
            "Bad request, email or password parameter is missing in POST request."
        )
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        # Tulostetaan description-tyylinen yhteenveto
        print("API 8: POST To Verify Login without email parameter")
        print(f"API URL: {url}")
        print("Request Method: POST")
        print("Request Parameter: password")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 10 – POST /verifyLogin with invalid details
    # --------------------------------------------------------------
    def verify_login_invalid(self, email: str, password: str) -> requests.Response:
        """
        POST /verifyLogin virheellisillä tunnuksilla.
        """
        url = f"{self.BASE_URL}/verifyLogin"
        payload = {
            "email": email,
            "password": password,
        }
        return requests.post(url, data=payload)

    def verify_login_invalid_should_return_404(
        self, email: str, password: str
    ) -> dict:
        """
        API 10: POST To Verify Login with invalid details

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 404
          - JSON message = 'User not found!'
        """
        url = f"{self.BASE_URL}/verifyLogin"
        response = self.verify_login_invalid(email, password)

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 404:
            raise AssertionError(
                f"Expected responseCode 404, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = "User not found!"
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        print("API 10: POST To Verify Login with invalid details")
        print(f"API URL: {url}")
        print("Request Method: POST")
        print("Request Parameters: email, password (invalid values)")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 11 – POST /createAccount
    # --------------------------------------------------------------
    def create_account(
        self,
        name: str,
        email: str,
        password: str,
        title: str,
        birth_date: str,
        birth_month: str,
        birth_year: str,
        firstname: str,
        lastname: str,
        company: str,
        address1: str,
        address2: str,
        country: str,
        zipcode: str,
        state: str,
        city: str,
        mobile_number: str,
    ) -> requests.Response:
        """
        POST /createAccount uuden käyttäjän luontiin.
        """
        url = f"{self.BASE_URL}/createAccount"
        payload = {
            "name": name,
            "email": email,
            "password": password,
            "title": title,
            "birth_date": birth_date,
            "birth_month": birth_month,
            "birth_year": birth_year,
            "firstname": firstname,
            "lastname": lastname,
            "company": company,
            "address1": address1,
            "address2": address2,
            "country": country,
            "zipcode": zipcode,
            "state": state,
            "city": city,
            "mobile_number": mobile_number,
        }
        return requests.post(url, data=payload)

    def create_account_should_return_201(
        self,
        name: str,
        email: str,
        password: str,
        title: str,
        birth_date: str,
        birth_month: str,
        birth_year: str,
        firstname: str,
        lastname: str,
        company: str,
        address1: str,
        address2: str,
        country: str,
        zipcode: str,
        state: str,
        city: str,
        mobile_number: str,
    ) -> dict:
        """
        API 11: POST To Create/Register User Account

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 201
          - JSON message = 'User created!'
        """
        url = f"{self.BASE_URL}/createAccount"
        response = self.create_account(
            name,
            email,
            password,
            title,
            birth_date,
            birth_month,
            birth_year,
            firstname,
            lastname,
            company,
            address1,
            address2,
            country,
            zipcode,
            state,
            city,
            mobile_number,
        )

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 201:
            raise AssertionError(
                f"Expected responseCode 201, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = "User created!"
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        print("API 11: POST To Create/Register User Account")
        print(f"API URL: {url}")
        print("Request Method: POST")
        print("Request Parameters: name, email, password, ...")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 12 – DELETE /deleteAccount
    # --------------------------------------------------------------
    def delete_account(self, email: str, password: str) -> requests.Response:
        """
        DELETE /deleteAccount olemassa olevan käyttäjätilin poistoon.
        """
        url = f"{self.BASE_URL}/deleteAccount"
        payload = {
            "email": email,
            "password": password,
        }
        return requests.delete(url, data=payload)

    def delete_account_should_return_200(self, email: str, password: str) -> dict:
        """
        API 12: DELETE METHOD To Delete User Account

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 200
          - JSON message = 'Account deleted!'
        """
        url = f"{self.BASE_URL}/deleteAccount"
        response = self.delete_account(email, password)

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 200:
            raise AssertionError(
                f"Expected responseCode 200, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = "Account deleted!"
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        print("API 12: DELETE METHOD To Delete User Account")
        print(f"API URL: {url}")
        print("Request Method: DELETE")
        print("Request Parameters: email, password")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 13 – PUT /updateAccount
    # --------------------------------------------------------------
    def update_account(
        self,
        name: str,
        email: str,
        password: str,
        title: str,
        birth_date: str,
        birth_month: str,
        birth_year: str,
        firstname: str,
        lastname: str,
        company: str,
        address1: str,
        address2: str,
        country: str,
        zipcode: str,
        state: str,
        city: str,
        mobile_number: str,
    ) -> requests.Response:
        """
        PUT /updateAccount käyttäjätilin tietojen päivittämiseen.
        """
        url = f"{self.BASE_URL}/updateAccount"
        payload = {
            "name": name,
            "email": email,
            "password": password,
            "title": title,
            "birth_date": birth_date,
            "birth_month": birth_month,
            "birth_year": birth_year,
            "firstname": firstname,
            "lastname": lastname,
            "company": company,
            "address1": address1,
            "address2": address2,
            "country": country,
            "zipcode": zipcode,
            "state": state,
            "city": city,
            "mobile_number": mobile_number,
        }
        return requests.put(url, data=payload)

    def update_account_should_return_200(
        self,
        name: str,
        email: str,
        password: str,
        title: str,
        birth_date: str,
        birth_month: str,
        birth_year: str,
        firstname: str,
        lastname: str,
        company: str,
        address1: str,
        address2: str,
        country: str,
        zipcode: str,
        state: str,
        city: str,
        mobile_number: str,
    ) -> dict:
        """
        API 13: PUT METHOD To Update User Account

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 200
          - JSON message = 'User updated!'
        """
        url = f"{self.BASE_URL}/updateAccount"
        response = self.update_account(
            name,
            email,
            password,
            title,
            birth_date,
            birth_month,
            birth_year,
            firstname,
            lastname,
            company,
            address1,
            address2,
            country,
            zipcode,
            state,
            city,
            mobile_number,
        )

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 200:
            raise AssertionError(
                f"Expected responseCode 200, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        expected_message = "User updated!"
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', "
                f"but got '{data.get('message')}'. JSON: {data}"
            )

        print("API 13: PUT METHOD To Update User Account")
        print(f"API URL: {url}")
        print("Request Method: PUT")
        print("Request Parameters: name, email, password, ...")
        print(f"Response Code: {data.get('responseCode')}")
        print(f"Response Message: {data.get('message')}")

        return data

    # --------------------------------------------------------------
    # API 14 – GET /getUserDetailByEmail
    # --------------------------------------------------------------
    def get_user_detail_by_email(self, email: str) -> requests.Response:
        """
        GET /getUserDetailByEmail hakee käyttäjän tiedot emailin perusteella.
        """
        url = f"{self.BASE_URL}/getUserDetailByEmail"
        params = {"email": email}
        return requests.get(url, params=params)

    def get_user_detail_by_email_should_return_200(self, email: str) -> dict:
        """
        API 14: GET user account detail by email

        Odotetaan:
          - HTTP-status 200
          - JSON responseCode = 200
          - Response JSON sisältää käyttäjätiedot
        """
        url = f"{self.BASE_URL}/getUserDetailByEmail"
        response = self.get_user_detail_by_email(email)

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200, but got {response.status_code}. "
                f"Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(
                f"Response is not valid JSON. Raw body: {response.text}"
            )

        if data.get("responseCode") != 200:
            raise AssertionError(
                f"Expected responseCode 200, but got {data.get('responseCode')}. "
                f"JSON: {data}"
            )

        if "user" not in data:
            raise AssertionError(
                f"Expected key 'user' in response JSON. Got: {data}"
            )

        print("API 14: GET user account detail by email")
        print(f"API URL: {url}")
        print("Request Method: GET")
        print("Request Parameters: email")
        print(f"Response Code: {data.get('responseCode')}")
        print("Response JSON: User Detail")

        return data
