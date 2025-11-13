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
Add Products To Basket
    [Documentation]    Open the products page and add products to basket
    Login As Valid User      ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
