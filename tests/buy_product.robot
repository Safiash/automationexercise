*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/ProductsPage.py
Library     ../libs/pages/Cart.py
Library     ../libs/pages/Checkout.py
Library     ../libs/pages/Payment.py
Variables    ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC007 Buy Product When Signed In
    [Documentation]    Testing product purchasing via the products page. 
    Login As Valid User    ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Select Product
    Proceed To Checkout
    Place Order
    Pay Order    ${USERNAME}
    Go To Main Page

TC042 Purchasing Product With Incomplete Payment Information 
    [Documentation]    Test purchasing the product with incomplete payment information, name missing. 
    Login As Valid User    ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Select Product
    Proceed To Checkout
    Place Order
    Try Paying Without Name


