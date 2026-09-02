workspace "Browser Task Board Architecture" "Separated frontend and Flask backend architecture baseline." {
    model {
        user = person "Task-board user" "Manages a personal TODO, DOING, and DONE board."

        taskBoard = softwareSystem "Browser Task Board" "Browser-based single-user task board." {
            browserFrontend = container "Browser Frontend" "Provides the HTML, CSS, and JavaScript task-board user interface." "HTML/CSS/JavaScript" {
                boardView = component "Board View" "Renders board sections, tasks, forms, and counts."
                interactionController = component "Interaction Controller" "Translates user interactions into API client calls."
                frontendApiClient = component "Frontend API Client" "Calls the Flask Backend HTTP/JSON API."
            }

            flaskBackend = container "Flask Backend" "Owns task-board product logic and exposes the HTTP/JSON API." "Python / Flask" {
                apiRoutes = component "API Routes" "Receives HTTP/JSON requests and returns JSON responses."
                taskApplicationService = component "Task Application Service" "Applies approved task behavior and validation."
                boardRepositoryPort = component "Board Repository Port" "Defines backend load and save operations."
                persistenceAdapter = component "SQLite Persistence Adapter" "Implements the repository port with SQLite."
                statusCounter = component "Status Counter" "Derives pending, current, and completed task counts."
            }

            persistenceMechanism = container "Persistence Mechanism" "Stores board state in SQLite for the first release." "SQLite"
        }

        user -> taskBoard "Uses to manage a personal board"
        user -> browserFrontend "Uses"
        browserFrontend -> flaskBackend "Calls same-origin HTTP/JSON API on 127.0.0.1"
        boardView -> interactionController "Submits user actions"
        interactionController -> frontendApiClient "Requests API operations"
        frontendApiClient -> apiRoutes "Sends HTTP/JSON requests"
        apiRoutes -> taskApplicationService "Delegates task-board operations"
        taskApplicationService -> boardRepositoryPort "Loads and saves board state"
        persistenceAdapter -> boardRepositoryPort "Implements"
        persistenceAdapter -> persistenceMechanism "Reads and writes board state"
        taskApplicationService -> statusCounter "Requests task counts"

        deploymentEnvironment "Local Personal Deployment" {
            deploymentNode "User Device" "The user's computer; no remote hosting in the first release." "Desktop or laptop" {
                deploymentNode "Web Browser" "Executes the frontend and calls localhost." "Modern web browser" {
                    containerInstance browserFrontend
                }
                deploymentNode "Local Application Runtime" "Runs the Flask backend bound only to 127.0.0.1." "Python runtime" {
                    containerInstance flaskBackend
                    containerInstance persistenceMechanism
                }
            }
        }
    }

    views {
        systemContext taskBoard "SystemContext" {
            include *
            autolayout lr
        }

        container taskBoard "Containers" {
            include *
            autolayout lr
        }

        component flaskBackend "FlaskBackendComponents" {
            include *
            autolayout lr
        }

        deployment taskBoard "Local Personal Deployment" "Deployment" {
            include *
            autolayout lr
        }

        styles {
            element "Person" {
                shape person
                background #0b7285
                color #ffffff
            }
            element "Software System" {
                background #2f9e44
                color #ffffff
            }
            element "Container" {
                background #1971c2
                color #ffffff
            }
            element "Component" {
                background #4c6ef5
                color #ffffff
            }
        }
    }
}
