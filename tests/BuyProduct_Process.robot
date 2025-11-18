*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py
Library    ../pages/SignLogin.py
Library    ../pages/ProductsPage.py
Library    ../pages/Cart.py
Library    ../pages/Checkout.py
Library    ../pages/Payment.py
Variables    ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC007 Buy Product When Signed In
    Login As Valid User    ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Select Product
    Proceed To Checkout
    Place Order
    Pay Order    ${USERNAME}


