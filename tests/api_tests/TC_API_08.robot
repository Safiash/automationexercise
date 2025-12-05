*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py


*** Test Cases ***
TC_API_08_POST_Verify_Login_Without_Email
    [Tags]    regression    api
    [Documentation]    API 8: POST verifyLogin ilman email-parametria. Tarkistukset tehdään Python-kirjastossa.
    Verify Login Without Email Should Return 400    ${PASSWORD}
