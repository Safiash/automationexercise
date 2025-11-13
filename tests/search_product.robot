*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py
Library    ../pages/ProductsPage.py

Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
Search For A Product
    [Documentation]    Open the Automation Exercise products page and search for a product
    ${product_name}=        Set Variable    Fancy Green Top
    Login As Valid User      ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Input Search Text        ${product_name}
    Click Search Button
    Verify Search Results    ${product_name}

