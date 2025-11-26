*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/ProductsPage.py
Library     ../libs/pages/Cart.py
Library     ../libs/pages/Checkout.py
Library     ../libs/pages/Payment.py
Variables    ../resource/variables/env_var.py


Test Setup       Run Keywords    Open Home Page    headless=False
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Variables ***


*** Test Cases ***

TC004 Create New User With Valid Default Values
    [Documentation]    Sign up with default values
    Sign Up New User
    Click Products Link From Homepage
    Select Product
    Proceed To Checkout
    Address Line1 Should Match Registration