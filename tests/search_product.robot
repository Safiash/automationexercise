*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/SignLogin.py
Library    ../libs/pages/HomePage.py
Library     ../libs/pages/ProductsPage.py

Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC006 Search For A Product
    [Tags]    e2e    regression
    [Documentation]    Open the Automation Exercise products page and search for a product
    ${product_name}=          Set Variable    Fancy Green Top
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Search Product By Name    ${product_name}

