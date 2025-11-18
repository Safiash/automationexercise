*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py
Library    ../pages/SignLogin.py
Variables    ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC014 Contact Us When Signed In
    [Documentation]    Fills in the contact us form and sends it
    Login As Valid User      ${EMAIL}    ${PASSWORD}
