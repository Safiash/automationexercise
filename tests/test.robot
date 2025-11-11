*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py


*** Test Cases ***
Open Home Page And Verify
    [Documentation]    Open the Automation Exercise home page and check if page is loaded
    Open Home Page
    Press Consent Cookies Button
    Check Is Home Page Loaded
    Check Is Featured Items Visible
    Close Browser

Click Test Cases Button
    [Documentation]    Open the Automation Exercise home page and check main links
    Open Home Page
    Press Consent Cookies Button
    Click Products Link From Homepage
    Click Test Cases Link From Homepage
    Click Api Testing From Homepage
    Click Home Link From Homepage
    Close Browser
