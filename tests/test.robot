*** Settings ***
Library    SeleniumLibrary
Library    ../pages/HomePage.py


*** Test Cases ***
Open Home Page And Verify
    [Documentation]    Open the Automation Exercise home page and check main elements
    Open Home Page
    Consent Cookies
    Is Home Page Loaded
    Is Featured Items Visible
    Close Browser

Click Test Cases Button
    [Documentation]    Open the Automation Exercise home page and check main elements
    Open Home Page
    Consent Cookies
    Click Test Cases
    Close Browser
