import requests


class Api:
    BASE_URL = "https://automationexercise.com/api"

    def search_product(self, term: str):
        url = f"{self.BASE_URL}/searchProduct"
        payload = {"search_product": term}
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response

    def _ensure_success_status_code(self, status_code):
        if not 200 <= status_code < 300:
            raise AssertionError(f"Expected 2xx status code, but got {status_code}")

    def search_product_json(self, term: str):
        response = self.search_product(term)
        self._ensure_success_status_code(response.status_code)
        return response.json()

    def search_product_should_return_results(self, term):
        data = self.search_product_json(term)
        if "products" not in data:
            raise AssertionError("Response JSON does not contain 'products' key.")
        if len(data["products"]) == 0:
            raise AssertionError(f"No products found for '{term}'")
        return data

    def verify_login_delete_should_return_405(self):
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
            raise AssertionError(f"Response is not valid JSON. Raw body: {response.text}")

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
    #  API 1 – GET /productsList
    # --------------------------------------------------------------

    def get_all_products(self):
        url = f"{self.BASE_URL}/productsList"
        return requests.get(url)

    def get_all_products_should_return_200(self):
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
    #  API 2 – POST /productsList
    # --------------------------------------------------------------

    def post_products_list(self):
        url = f"{self.BASE_URL}/productsList"
        return requests.post(url)

    def post_products_list_should_return_405(self):
        response = self.post_products_list()

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200 wrapper, got {response.status_code}. Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. JSON: {data}"
            )

        return data

    # --------------------------------------------------------------
    #  API 3 – GET /brandsList
    # --------------------------------------------------------------

    def get_all_brands(self):
        url = f"{self.BASE_URL}/brandsList"
        return requests.get(url)

    def get_all_brands_should_return_200(self):
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
    #  API 4 – PUT /brandsList
    # --------------------------------------------------------------

    def put_brands_list(self):
        url = f"{self.BASE_URL}/brandsList"
        return requests.put(url)

    def put_brands_list_should_return_405(self):
        response = self.put_brands_list()

        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP 200 wrapper, got {response.status_code}. Body: {response.text}"
            )

        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Invalid JSON. Body: {response.text}")

        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, got {data.get('responseCode')}. JSON: {data}"
            )

        return data
