*** Settings ***
Library    ../../libs/api/Api.py


*** Test Cases ***
API 2: POST To All Products List
    [Tags]    regression    api
    ${result}=    Post Products List Should Return 405
    Should Be Equal As Integers    ${result["responseCode"]}    405
