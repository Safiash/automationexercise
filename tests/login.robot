*** Settings ***

Library    SeleniumLibrary
Library    ../pages/SignLogin.py
Library    ../pages/HomePage.py

Variables    ../resource/variables/env_var.py

Test Setup       Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser


*** Test Cases ***
TC002 Login With Valid Credentials
    [Documentation]    Open the signup/login page and login with valid credentials
    Click Sign Up Login Link From Homepage
    Fill Login Form    ${EMAIL}    ${PASSWORD}
    Press Login Button
    Verify Login
    Press Logout Button

TC003 Login With Invalid Credentials
    [Documentation]    Open the signup/login page and try login with invalid credentials
    Click Sign Up Login Link From Homepage
    Fill Login Form    wrong@wrong.com    wrongpassword
    Press Login Button
    Check Login Error Message Is Visible

TC018 Login With Empty Credentials
    [Documentation]    Open the signup /login page and try login with empty credentials
    Click Sign Up Login Link From Homepage
    Fill Login Form        ${EMPTY}    ${EMPTY}
    Press Login Button
    Check Please Fill All Fields Message Is Visible

TC019 Login With Invalid Password
    [Documentation]    Open the signup/login page and try login with invalid password
    Click Sign Up Login Link From Homepage
    Fill Login Form    ${EMAIL}    wrongpassword
    Press Login Button
    Check Login Error Message Is Visible

    