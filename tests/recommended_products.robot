*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Library     ../libs/pages/ProductsPage.py
Library     ../libs/pages/Cart.py
Variables    ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC031 Coose A Product From Recommended Items
    [Documentation]    Test scrolling to the bottom of the page, to the recommended item section,
    ...     selects a product from there, goes to the cart, checks and clears the cart.
    Scroll Down To Recommended Items
    Choose Recommended Item
    Check Cart
    Empty Shopping Cart

    