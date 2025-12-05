*** Settings ***
Library    ../../libs/api/Api.py


*** Test Cases ***
API 1: Get All Products List
    [Tags]    regression    api
    ${result}=    Get All Products Should Return 200
    Should Not Be Empty    ${result}
