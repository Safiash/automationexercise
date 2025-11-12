*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py

Test Setup       Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***
Sign Up New User
    [Documentation]    Test for signing up a new user
    Click Sign Up Login Link From Homepage
    ${username}    ${email}=    Generate Random Credentials
    Fill Signup Form    ${username}    ${email}
    Press Sign Up Button
    #Jutta
    
