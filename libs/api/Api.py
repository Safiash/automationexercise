import  requests


class Api:
    BASE_URL = "https://automationexercise.com/api"

    def search_product(self, term: str):
        """
        Kutsuu /searchProduct -endpointia annetulla hakusanalla.
        Palauttaa requests.Response-olion.
        """
        url = f"{self.BASE_URL}/searchProduct"
        payload = {"search_product": term}

        response = requests.post(url, data=payload)
        # nostaa poikkeuksen jos status code ei ole 2xx
        response.raise_for_status()
        return response
    
    def _ensure_success_status_code(self, status_code):
        """Tarkistaa status-koodin 2xx alkavaksi, muuten hälyttää virhetekstin"""
        if not 200 <= status_code < 300:
            raise AssertionError(f"Expected 2xx status code, but got {status_code}")

    def search_product_json(self, term: str):
        """
        Palauttaa suoraan parsitun JSONin ja tarkistaa status-koodin.
        """
        response = self.search_product(term)
        self._ensure_success_status_code(response.status_code)
        return response.json()

    def search_product_should_return_results(self, term):
        """
        Palauttaa hakutuloksen tuotteesta ja hälyttää, jos tuotetta ei ole json-datassa tai data on nolla.
        """
        data = self.search_product_json(term)

        if "products" not in data:
            raise AssertionError("Response JSON does not contain 'products' key.")
        if len(data["products"]) == 0:
            raise AssertionError(f"No products found for '{term}'")
        return data
    
    def verify_login_delete_should_return_405(self):
        """
        Kutsuu /verifyLogin -endpointia DELETE-metodilla ja varmistaa,
        että:
          - HTTP statuskoodi on 200
          - JSON:issa responseCode on 405
          - viesti on 'This request method is not supported.'
        """
        url = f"{self.BASE_URL}/verifyLogin"
        response = requests.delete(url)

        # 1) HTTP-status odotetusti 200
        if response.status_code != 200:
            raise AssertionError(
                f"Expected HTTP status code 200, but got {response.status_code}. "
                f"Response body: {response.text}"
            )

        # 2) JSON-parsaus
        try:
            data = response.json()
        except ValueError:
            raise AssertionError(f"Response is not valid JSON. Raw body: {response.text}")

        # 3) Sovellustason koodi 405
        if data.get("responseCode") != 405:
            raise AssertionError(
                f"Expected responseCode 405, but got {data.get('responseCode')}. "
                f"Full JSON: {data}"
            )

        # 4) Virheviesti
        expected_message = "This request method is not supported."
        if data.get("message") != expected_message:
            raise AssertionError(
                f"Expected message '{expected_message}', but got '{data.get('message')}'. "
                f"Full JSON: {data}"
            )

        return data