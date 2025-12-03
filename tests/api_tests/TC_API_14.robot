*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py

*** Test Cases ***
TC_API_14_GET_User_Account_Detail_By_Email
    [Documentation]    API 14: GET getUserDetailByEmail olemassa olevan käyttäjän hakemiseen emaililla.
    Get User Detail By Email Should Return 200    ${EMAIL}
