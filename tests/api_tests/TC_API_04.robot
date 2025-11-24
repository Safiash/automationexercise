*** Settings ***
Library    RequestsLibrary
Library    Collections
Library    BuiltIn

*** Test Cases ***
API 4: PUT Kaikkien brändien listalle
    [Documentation]    Lähetä PUT-pyyntö /api/brandsList ja varmista että API palauttaa 405

    # Luodaan HTTP-sessio API-palveluun
    Create Session    mysession    https://automationexercise.com

    # Määritetään headerit (kerrotaan että lähetämme JSON-dataa)
    &{headers}=    Create Dictionary    Content-Type=application/json

    # Body – lähetetään esimerkkidata (API ei oikeasti käytä, mutta PUT tarvitsee bodya)
    &{body}=    Create Dictionary    name=testbrand

    # Lähetetään PUT-pyyntö headerien ja bodyn kanssa
    ${response}=    PUT On Session
    ...    mysession
    ...    /api/brandsList
    ...    headers=${headers}
    ...    data=${body}
    ...    expected_status=ANY    # Sallitaan mikä tahansa HTTP-status

    # Tulostetaan vastaus konsoliin debuggausta varten
    Log To Console    Status: ${response.status_code}
    Log To Console    Response: ${response.text}

    # API:n dokumentation mukainen odotettu JSON-koodi = 405
    Should Be Equal As Integers    ${response.json()['responseCode']}    405
