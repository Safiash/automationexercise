*** Settings ***

Library    SeleniumLibrary
Library     ../libs/pages/HomePage.py
Library     ../libs/pages/SignLogin.py
Variables   ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page    headless=True
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC008 Subscribe Newsletter When Signed In
    [Documentation]    Subscribes the newsletter with a valid email address
    Click Sign Up Login Link From Homepage
    Fill Login Form    ${EMAIL}    ${PASSWORD}
    Press Login Button
    Submit Email Newsletter   ${email}
    Subscribe Newsletter