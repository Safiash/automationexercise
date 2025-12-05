*** Settings ***
Library    ../../libs/api/Api.py


*** Test Cases ***
API 3: Get All Brands List
    [Tags]    regression    api
    ${result}=    Get All Brands Should Return 200
    Should Not Be Empty    ${result}
