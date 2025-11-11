*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py


*** Test Cases ***
Sign Up New User
    [Documentation]    Test for signing up a new user
    Open Home Page
    Press Consent Cookies Button
    Click Sign Up Login Link From Homepage
    ${username}    ${email}=    Generate Random Credentials
    Fill Signup Form    ${username}    ${email}
    #Jutta
    
