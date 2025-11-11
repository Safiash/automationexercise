*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py


*** Test Cases ***
Sign Up New User
    [Documentation]    Test for signing up a new user
    HomePage.Open Home Page
    HomePage.Consent Cookies
    HomePage.Click Sign Up Login
    ${username}    ${email}=    SignLogin.Generate Random Credentials
    SignLogin.Fill Signup Form    ${username}    ${email}
    
    
