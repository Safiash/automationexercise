*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/ProductsPage.py
Library     ../libs/pages/Cart.py
Library     ../libs/pages/Checkout.py
Variables    ../resource/variables/env_var.py



Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC009 Product Removal From The Cart
    Login As Valid User    ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Select Product
    Click Cart Link From Homepage
    Empty Shopping Cart