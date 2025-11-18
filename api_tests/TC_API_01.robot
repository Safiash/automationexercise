*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

*** Test Cases ***
API 1: Get All Products List
    [Documentation]    Hae kaikki tuotteet GET-pyynnöllä ja varmista JSON-rakenteen oikeellisuus

    # Luodaan sessio API-palveluun
    Create Session    mysession    https://automationexercise.com

    # Lähetetään GET-pyyntö tuotteiden listaan
    ${response}=    GET On Session    mysession    /api/productsList

    # Varmistetaan että HTTP-statuskoodi on 200
    Should Be Equal As Integers    ${response.status_code}    200

    # Muutetaan vastauksen body JSON-muotoon (dictionary)
    ${json_data}=    To JSON    ${response.text}

    # Tulostetaan JSON log.html-tiedostoon ja konsoliin
    Log    ${json_data}              # HTML-logi
    Log To Console    ${json_data}   # Konsoliloki

    # Tarkistetaan että JSON sisältää 'products'-avaimen
    Dictionary Should Contain Key    ${json_data}    products

    # Haetaan products-lista JSON:sta
    ${products}=    Get From Dictionary    ${json_data}    products

    # Otetaan listan ensimmäinen tuote
    ${first_product}=    Set Variable    ${products}[0]

    # Varmistetaan että tuotteella on id, name ja price
    Dictionary Should Contain Key    ${first_product}    id
    Dictionary Should Contain Key    ${first_product}    name
    Dictionary Should Contain Key    ${first_product}    price
