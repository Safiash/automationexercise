*** Settings ***
Library    ../../libs/api/Api.py


*** Test Cases ***
API 4: PUT To All Brands List
    [Tags]    regression    api
    ${result}=    Put Brands List Should Return 405
    Should Be Equal As Integers    ${result["responseCode"]}    405
