*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

*** Test Cases ***
API 1: Get All Products List
    [Documentation]    GET isteği ile tüm ürünleri çek ve JSON alanlarını doğrula

    # Session oluştur
    Create Session    mysession    https://automationexercise.com

    # GET isteği
    ${response}=    GET On Session    mysession    /api/productsList

    # Status kodunu kontrol et
    Should Be Equal As Integers    ${response.status_code}    200

    # JSON'u dictionary olarak al
    ${json_data}=    To JSON    ${response.text}

    # JSON'u hem log.html hem de terminalde göster
    Log    ${json_data}        # HTML log
    Log To Console    ${json_data}   # Terminal log

    # 'products' key var mı kontrol et
    Dictionary Should Contain Key    ${json_data}    products

    # İlk ürünün id, name ve price alanları var mı kontrol et
    ${products}=    Get From Dictionary    ${json_data}    products
    ${first_product}=    Set Variable    ${products}[0]
    Dictionary Should Contain Key    ${first_product}    id
    Dictionary Should Contain Key    ${first_product}    name
    Dictionary Should Contain Key    ${first_product}    price
