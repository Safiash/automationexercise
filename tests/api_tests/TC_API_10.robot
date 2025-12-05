*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py

*** Test Cases ***
TC_API_10_POST_Verify_Login_With_Invalid_Details
    [Tags]    regression    api
    [Documentation]    API 10: POST verifyLogin invalid-tiedoilla. Tarkistukset Python-kirjastossa.
    Verify Login Invalid Should Return 404    invalid_${EMAIL}    invalid_${PASSWORD}
