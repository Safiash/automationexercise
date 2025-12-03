*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py

*** Variables ***
${NEW_USER_EMAIL}    apitest_${EMAIL}
${NEW_NAME}          Updated Test User

*** Test Cases ***
TC_API_13_PUT_Update_User_Account
    [Documentation]    API 13: PUT updateAccount käyttäjätilin tietojen päivittämiseen.
    Update Account Should Return 200
    ...    ${NEW_NAME}
    ...    ${EMAIL}
    ...    ${PASSWORD}
    ...    Mr
    ...    1
    ...    1
    ...    1990
    ...    Yusuf
    ...    Er
    ...    TestCompany
    ...    TestAddress1
    ...    TestAddress2
    ...    Canada
    ...    12345
    ...    TestState
    ...    TestCity
    ...    +358401234567
