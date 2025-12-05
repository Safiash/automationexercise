*** Settings ***
Library     ../../libs/api/Api.py
Variables   ../../resource/variables/env_var.py

*** Variables ***
${NEW_USER_EMAIL}    apitest_${EMAIL}

*** Test Cases ***
TC_API_12_DELETE_User_Account
    [Tags]    regression    api    critical
    [Documentation]    API 12: DELETE deleteAccount käyttäjätilin poistoon.
    Delete Account Should Return 200    ${NEW_USER_EMAIL}    ${PASSWORD}
