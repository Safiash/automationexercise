*** Settings ***
Library    RequestsLibrary

*** Test Cases ***
API 2: POST To All Products List
    [Documentation]    Lähetä POST /api/productsList ja varmista että JSON palauttaa 405

    # Luodaan sessio API-palveluun
    Create Session    mysession    https://automationexercise.com

    # Lähetetään POST-pyyntö productsList-endpointiin
    ${response}=    POST On Session    mysession    /api/productsList

    # API palauttaa aina HTTP 200, joten statuskoodi tarkistetaan näin
    Should Be Equal As Integers    ${response.status_code}    200

    # Haetaan vastauksen JSON (dictionary-muodossa)
    ${json}=    Set Variable    ${response.json()}

    # Tarkistetaan että responseCode = 405 (metodia ei tueta)
    Should Be Equal As Integers    ${json["responseCode"]}    405

    # Tulostetaan statuskoodi ja JSON konsoliin
    Log To Console    Status Code: ${response.status_code}
    Log To Console    Response JSON: ${json}
