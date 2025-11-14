*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py

Test Setup       Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***
TC015 Click All Main Links From Home Page
    [Documentation]    Open the Automation Exercise home page and click all main links
    Click Products Link From Homepage
    Click Cart Link From Homepage
    Click Signup Login Link From Homepage
    Click Contact Us Link From Homepage
    Click Home Link From Homepage
