*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py

Test Setup       Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***
Check All Women Categories From Home Page
    [Documentation]    Open the home page and check all womens categories
    Click Category Women
    Click Category Dress From Women
    Click Category Women
    Click Category Tops From Women
    Click Category Women
    Click Category Saree From Women

Check All Men Categories From Home Page
    [Documentation]    Open the home page and check all mens categories
    Click Category Men
    Click Category TShirts From Men
    Click Category Men
    Click Category Jeans From Men

Check All Kids Categories From Home Page
    [Documentation]    Open the home page and check all kids categories
    Click Category Kids
    Click Category Dress From Kids
    Click Category Kids
    Click Category Tops From Kids
