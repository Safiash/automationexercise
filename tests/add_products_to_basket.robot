*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py
Library    ../pages/ProductsPage.py
Library    ../pages/Cart.py

Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Variables ***
${product_quantity}    4


*** Test Cases ***
TC011 Add Given Quantity Of Products To Basket
    [Documentation]    Test for open the products page and adding given quantity of products to basket
    Login As Valid User      ${EMAIL}    ${PASSWORD}
    Click Products Link From Homepage
    Add Products To Cart By Quantity     ${product_quantity}
    Open Shopping Cart
    Verify Product Count In Cart         ${product_quantity}
    Empty Shopping Cart
    
    
