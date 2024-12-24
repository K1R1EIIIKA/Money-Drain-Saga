import os


def generate_uml(uml_code, output_file="diagram.png"):
    """
    Generates a UML diagram from PlantUML code.

    Args:
        uml_code (str): PlantUML code to generate the diagram.
        output_file (str): Path to save the generated diagram.
    """
    with open("diagram.puml", "w") as file:
        file.write(uml_code)

    os.system(f"java -jar plantuml.jar diagram.puml")
    os.rename("diagram.png", output_file)
    print(f"Diagram saved as {output_file}")


# PlantUML code for the diagram
uml_code = """
@startuml
skinparam messageSpacing 50
skinparam arrowSize 30
skinparam classFontSize 10
skinparam arrowFontSize 10

actor User
database DB_AuthService
database DB_TransactionService
database DB_ShopService

queue RabbitMQ

User -> AuthService : "send login request"
AuthService -> DB_AuthService : "query user data"
AuthService -> TokenManager : "generate token"
TokenManager -up-> AuthService : "return token"
AuthService -> User : "return token"

User -> ShopService : "make purchase request"
ShopService -> DB_ShopService : "get item data"
ShopService -> AuthService : "validate token"
AuthService -> RabbitMQ : "send spend money & validation request"
RabbitMQ -> TransactionService : "handle transaction"
TransactionService -> DB_TransactionService : "save transaction data"
TransactionService -> RabbitMQ : "notify transaction status"
RabbitMQ -> ShopService : "transaction status"
ShopService -> User : "return purchase result"

AuthService -down-> DB_AuthService : "reads/writes user data"
TransactionService -down-> DB_TransactionService : "reads/writes transaction data"
ShopService -down-> DB_ShopService : "reads/writes shop data"


TransactionService -> RabbitMQ : "sends transaction request"
ShopService -> RabbitMQ : "sends money spend request"
@enduml
"""

# Generate the UML diagram
generate_uml(uml_code, 'all_services.png')
