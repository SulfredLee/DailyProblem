content_st = """
@startuml twolock_msg_q
' !include https://raw.githubusercontent.com/plantuml-stdlib/C4-PlantUML/master/C4_Container.puml

' System(systemAlias, "UDP Server", "")
' System(clientAlias, "UDP CLient", "")

' Rel(clientAlias, systemAlias, "Send data", "")
' Rel(systemAlias, clientAlias, "Reply ack", "")

' https://plantuml.com/sequence-diagram
skinparam backgroundColor #EEEBDC
skinparam handwritten true

left to right direction

json "Msg Q" as J {
    "head --- mutex_A":"0 --- Data",
    "":"1 --- Data",
    "":"2 --- Data",
    "":"3 --- Data",
    "tail --- mutex_B":"4 --- Data",
    "":"5 --- Empty",
    "":"6 --- Empty",
    "":"...",
    "":"N --- Empty"
}
@enduml
"""
