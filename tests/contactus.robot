*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Variables    ../resource/variables/env_var.py


Test Setup       Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC014 Contact Us When Signed In
    [Documentation]    Fills in the contact us form and sends it
    ${name}=    Set Variable    Pekka
    ${subject}=    Set Variable    666
    ${message}=    Set Variable    olen todella pettynyt tuotteisiinne ja haluan kaikki rahani takaisin heti
    Login As Valid User      ${EMAIL}    ${PASSWORD}
    Click Contact Us Link From Homepage
    Submit Name    ${name}
    Submit Email Contactus    ${EMAIL}
    Submit Subject    ${subject}
    Submit Message    ${message}
    Submit Contact Us