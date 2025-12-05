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

TC012 Download Invoice As A Registered User
    [Tags]    e2e    regression    critical
    [Documentation]    Purchase the product, download the receipt,
    ...     and then check to see if the receipt appears in your computer's Downloads folder.
    Login As Valid User    ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Select Product
    Proceed To Checkout
    Place Order
    Pay Order    ${USERNAME}
    Download Invoice
    Verify Invoice Exists    30
