*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

*** Test Cases ***
API 3: Get All Brands List
    [Documentation]    Hae kaikki brändit listasta ja varmista, että JSON sisältää odotetut kentät

    # Luo sessio
    Create Session    mysession    https://automationexercise.com

    # Suorita GET-pyyntö
    ${response}=    GET On Session    mysession    /api/brandsList

    # Tarkista statuskoodi
    Should Be Equal As Integers    ${response.status_code}    200

    # Hae JSON dictionaryksi suoraan
    ${json_data}=    Set Variable    ${response.json()}

    # Tarkista, että 'brands' avain on olemassa
    Dictionary Should Contain Key    ${json_data}    brands

    # Hae ensimmäinen brändi ja tarkista kentät
    ${brands}=    Get From Dictionary    ${json_data}    brands
    ${first_brand}=    Set Variable    ${brands}[0]
    Dictionary Should Contain Key    ${first_brand}    id
    Dictionary Should Contain Key    ${first_brand}    brand

    # Kirjaa JSON konsoliin
    Log To Console    Status: ${response.status_code}, Response: ${json_data}
