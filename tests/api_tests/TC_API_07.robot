*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py

*** Test Cases ***
TC_API_07_POST_Verify_Login_Valid_Details
    [Tags]    regression    api
    [Documentation]    POST verifyLogin oikeilla tunnuksilla. Odotetaan responseCode 200 ja 'User exists!' -viesti.
    Verify Login Valid Should Return 200    ${EMAIL}    ${PASSWORD}
