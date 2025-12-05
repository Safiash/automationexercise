*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/ProductsPage.py

Variables    ../resource/variables/env_var.py

Test Setup    Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser



*** Test Cases ***
TC033 Scroll Through Products Page And Go Back To Top With Arrow
    [Tags]    smoke
    [Documentation]    Test to scroll through products page and go back to top with arrow button
    Click Products Link From Homepage
    Scroll To The Bottom Of Page
    Go Back To Top Using Arrow Button

