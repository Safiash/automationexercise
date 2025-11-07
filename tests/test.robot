*** Settings ***
Library    ../pages/home_page.py
Library    SeleniumLibrary

*** Test Cases ***
Open Home Page And Verify
    [Documentation]    Open the Automation Exercise home page and check main elements
    Open Home Page
    Is Home Page Loaded
    Is Featured Items Visible

Click Test Cases Button
    Open Home Page
    Click Test Cases
