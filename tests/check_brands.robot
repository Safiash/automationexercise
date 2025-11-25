*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/ProductsPage.py
Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***
Check All Brands From Home Page
    [Documentation]    Test to open product page and check all brands navigation
    Login As Valid User       ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Verify All Brands Navigation
