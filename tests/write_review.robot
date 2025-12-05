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
    [Tags]    e2e    regression
    [Documentation]    Test for writing a review for a product
    ${product_name}=    Set Variable    Summer White Top
    ${review_text}=     Generate Random Text
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Search Product By Name    ${product_name}
    Click View Product After Search
    Write Product Review      ${USERNAME}    ${EMAIL}    ${review_text}
    Submit Review Succesfully

TC029 Write Review For A Product Without Username And Email
    [Tags]    e2e    regression
    [Documentation]    Negative test for writing a review for a product without username and email
    ${product_name}=    Set Variable    Soft Stretch Jeans
    ${review_text}=     Generate Random Text
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Search Product By Name    ${product_name}
    Click View Product After Search
    Write Product Review      ${EMPTY}      ${EMPTY}    ${review_text}
    Submit Review Missing Info Failure

TC030 Write Review For A Product Without Review Text
    [Tags]    e2e    regression
    [Documentation]    Negative test for writing a review for a product without review text
    ${product_name}=    Set Variable    Frozen Tops For Kids
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Search Product By Name    ${product_name}
    Click View Product After Search
    Write Product Review      ${USERNAME}    ${EMAIL}    ${EMPTY}
    Submit Review Missing Text Failure