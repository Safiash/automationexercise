*** Settings ***
Library    SeleniumLibrary
Library    ../pages/home_page.py
Suite Teardown    Close All Browsers

*** Test Cases ***

Open Home Page And Verify
    Open Home Page    chrome
    Is Home Page Loaded
    Is Featured Items Visible

Click Test Cases Button
    Click Test Cases
