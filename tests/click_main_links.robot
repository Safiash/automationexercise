*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py

Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC015 Click All Main Links From Home Page
    [Tags]    smoke
    [Documentation]    Open the Automation Exercise home page and click all main links
    Click Products Link From Homepage
    Click Cart Link From Homepage
    Click Signup Login Link From Homepage
    Click Contact Us Link From Homepage
    Click Home Link From Homepage

TC041 Click Logo In Home Page
    [Tags]    smoke
    [Documentation]    Opens another page first and then returns to the home page by clicking the logo
    Click Products Link From Homepage
    Click Logo From Homepage
