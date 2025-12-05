*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC010 Check All Women Categories From Home Page
    [Tags]    smoke
    [Documentation]    Open the home page and check all womens categories
    Click Category Dress From Women
    Click Category Tops From Women
    Click Category Saree From Women

TC010 Check All Men Categories From Home Page
    [Tags]    smoke
    [Documentation]    Open the home page and check all mens categories
    Click Category TShirts From Men
    Click Category Jeans From Men

TC010 Check All Kids Categories From Home Page
    [Tags]    smoke
    [Documentation]    Open the home page and check all kids categories
    Click Category Dress From Kids
    Click Category Tops From Kids
