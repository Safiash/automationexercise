*** Settings ***

Library    SeleniumLibrary
Library    ../libs/pages/SignLogin.py
Library    ../libs/pages/HomePage.py
Library    ../libs/pages/ProductsPage.py

Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC028 Write Review For A Product
    ${product_name}=    Set Variable    Summer White Top
    ${review_text}=     Generate Random Text
    [Documentation]    Test for writing a review for a product
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Search Product By Name    ${product_name}
    Click View Product After Search
    Write Product Review      ${USERNAME}    ${EMAIL}    ${review_text}

