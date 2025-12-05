*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py


*** Variables ***
${NEW_USER_EMAIL}    apitest_${EMAIL}
${NEW_NAME}          Test User

*** Test Cases ***
TC_API_11_POST_Create_Register_User_Account
    [Tags]    regression    api    critical
    [Documentation]    API 11: POST createAccount uuden käyttäjän luontiin.
    Create Account Should Return 201
    ...    ${NEW_NAME}
    ...    ${NEW_USER_EMAIL}
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
