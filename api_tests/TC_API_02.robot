*** Settings ***
Library    RequestsLibrary
Library    BuiltIn

*** Test Cases ***
API 2: POST To All Products List
    [Documentation]    Lähetä POST /api/productsList ja varmista että JSON palauttaa 405

    Create Session    mysession    https://automationexercise.com

    ${response}=    POST On Session    mysession    /api/productsList

    # HTTP statuscode API her zaman 200 döndürüyor
    Should Be Equal As Integers    ${response.status_code}    200

    # JSON'u doğru şekilde alıyoruz
    ${json}=    Set Variable    ${response.json()}

    # JSON responseCode 405 olmalı
    Should Be Equal As Integers    ${json["responseCode"]}    405

    # Loglar
    Log To Console    Status Code: ${response.status_code}
    Log To Console    Response JSON: ${json}
