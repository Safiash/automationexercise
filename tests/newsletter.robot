*** Settings ***

Library    SeleniumLibrary
Library    ../pages/HomePage.py
Library    ../pages/SignLogin.py
Variables    ../resource/variables/env_var.py


Test Setup    Run Keywords    Open Home Page
...              AND    Set Selenium Implicit Wait    10s
Test Teardown    Close Browser

*** Test Cases ***

TC008 Subscribe Newsletter When Signed In
    Login As Valid User    ${EMAIL}    ${PASSWORD}

    # eli luon vielä avainsanan, jolla se tilaa sen. luon sen joko jo olemassa olevaan kirjastoon, tai luon oman. jos luon oman, muista linkittää se tuohon settingseihin.