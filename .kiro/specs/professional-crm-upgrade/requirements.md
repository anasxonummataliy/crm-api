# Requirements Document

## Introduction

This document defines the requirements for upgrading the existing NexusCRM system from a basic prototype to a professional-grade CRM application. The upgrade encompasses five major areas: a modern responsive UI built with React, a JWT-based authentication system, comprehensive automated testing, Docker Compose multi-service configuration, and a complete CI/CD pipeline using GitHub Actions. The existing FastAPI backend with SQLite database and basic HTML frontend serves as the foundation.

## Glossary

- **CRM_System**: The complete NexusCRM application including frontend, backend API, and database
- **Frontend**: The React-based single-page application that provides the user interface
- **Backend_API**: The FastAPI server that handles HTTP requests and business logic
- **Auth_Service**: The authentication and authorization module within the Backend_API
- **User**: A person who has registered credentials and can log into the CRM_System
- **JWT_Token**: A JSON Web Token used to authenticate API requests after login
- **Access_Token**: A short-lived JWT_Token used for API request authorization
- **Refresh_Token**: A longer-lived token used to obtain new Access_Tokens without re-login
- **Dashboard**: The main overview page showing summary statistics and recent activity
- **Customer**: A contact record stored in the CRM database with associated deals and tasks
- **Deal**: A sales opportunity associated with a Customer moving through pipeline stages
- **Task**: An actionable item that may be linked to a Customer with status and priority tracking
- **Activity**: A logged interaction event (call, email, meeting, note) associated with a Customer
- **Pipeline**: The visual representation of Deal progression through sales stages
- **Test_Suite**: The complete collection of automated tests including unit, integration, and property-based tests
- **CI_Pipeline**: The GitHub Actions workflow that runs tests and linting on code changes
- **CD_Pipeline**: The GitHub Actions workflow that builds and deploys Docker images on successful merges
- **Docker_Compose**: The multi-container orchestration configuration for local development and deployment

## Requirements

### Requirement 1: User Registration

**User Story:** As an administrator, I want to register new users with credentials, so that only authorized personnel can access the CRM_System.

#### Acceptance Criteria

1. WHEN a registration request is submitted with a unique username and valid password, THE Auth_Service SHALL create a new User record and return a success confirmation
2. WHEN a registration request is submitted with an existing username, THE Auth_Service SHALL reject the request and return a conflict error with a descriptive message
3. THE Auth_Service SHALL store passwords using bcrypt hashing with a minimum cost factor of 12
4. WHEN a registration request is submitted with a password shorter than 8 characters, THE Auth_Service SHALL reject the request and return a validation error

### Requirement 2: User Authentication

**User Story:** As a user, I want to log in with my credentials, so that I can securely access CRM data.

#### Acceptance Criteria

1. WHEN valid credentials are submitted to the login endpoint, THE Auth_Service SHALL return an Access_Token with a 30-minute expiration and a Refresh_Token with a 7-day expiration
2. WHEN invalid credentials are submitted to the login endpoint, THE Auth_Service SHALL return a 401 Unauthorized response within 500 milliseconds
3. WHEN a valid Refresh_Token is submitted to the token refresh endpoint, THE Auth_Service SHALL return a new Access_Token
4. WHEN an expired or invalid Refresh_Token is submitted, THE Auth_Service SHALL return a 401 Unauthorized response

### Requirement 3: API Route Protection

**User Story:** As a system administrator, I want all CRM data endpoints protected by authentication, so that unauthorized access is prevented.

#### Acceptance Criteria

1. WHEN an API request is made without an Authorization header, THE Backend_API SHALL return a 401 Unauthorized response
2. WHEN an API request includes a valid Access_Token in the Authorization header, THE Backend_API SHALL process the request and return the appropriate response
3. WHEN an API request includes an expired Access_Token, THE Backend_API SHALL return a 401 Unauthorized response with an "expired" error code
4. THE Backend_API SHALL exempt the login, registration, and health-check endpoints from authentication requirements

### Requirement 4: Professional Frontend Architecture

**User Story:** As a developer, I want a React-based frontend with modern tooling, so that the UI is maintainable and scalable.

#### Acceptance Criteria

1. THE Frontend SHALL be built using React 18 with TypeScript and Vite as the build tool
2. THE Frontend SHALL use a component-based architecture with reusable UI components separated from page-level components
3. THE Frontend SHALL use React Router for client-side navigation between Dashboard, Customers, Deals, Tasks, and Activities pages
4. THE Frontend SHALL communicate with the Backend_API using a centralized HTTP client that automatically attaches Access_Tokens to requests
5. WHEN an API request returns a 401 response with an "expired" error code, THE Frontend SHALL automatically attempt token refresh and retry the original request

### Requirement 5: Responsive Dashboard UI

**User Story:** As a user, I want a clean and informative dashboard, so that I can quickly understand the current state of my sales pipeline.

#### Acceptance Criteria

1. THE Dashboard SHALL display summary statistics cards showing total customers, active pipeline value, won deals value, and pending tasks count
2. THE Dashboard SHALL display a visual pipeline showing deal counts and values per stage (new, contacted, proposal, negotiation, won, lost)
3. THE Dashboard SHALL display recent deals and recent activities in a two-column layout on desktop viewports
4. WHEN the viewport width is less than 768 pixels, THE Dashboard SHALL reorganize into a single-column layout with stacked components
5. THE Dashboard SHALL load and display data within 2 seconds of page render on a standard broadband connection

### Requirement 6: Customer Management UI

**User Story:** As a sales representative, I want to manage customer records through an intuitive interface, so that I can efficiently track my contacts.

#### Acceptance Criteria

1. THE Frontend SHALL display customers in a sortable, searchable table with columns for name, company, email, phone, status, and creation date
2. WHEN the user types in the search field, THE Frontend SHALL filter displayed customers by name, email, or company within 300 milliseconds
3. WHEN the user clicks the add button, THE Frontend SHALL display a modal form for creating a new customer with validation on required fields
4. WHEN the user clicks the edit action on a customer row, THE Frontend SHALL display a pre-filled modal form for updating the customer record
5. WHEN the user clicks the delete action, THE Frontend SHALL display a confirmation dialog before executing the deletion
6. IF a customer creation or update request fails, THEN THE Frontend SHALL display an error notification with the failure reason

### Requirement 7: Deal Management UI

**User Story:** As a sales representative, I want to manage deals with pipeline visualization, so that I can track sales progress effectively.

#### Acceptance Criteria

1. THE Frontend SHALL display deals in a filterable table with columns for title, customer name, value, stage, probability, and close date
2. THE Frontend SHALL provide a stage filter dropdown to view deals by pipeline stage
3. WHEN a deal is created or updated, THE Frontend SHALL reflect the change in the deals list and dashboard pipeline without requiring a full page reload
4. WHEN the user edits a deal stage, THE Frontend SHALL display the updated stage with the appropriate color-coded badge

### Requirement 8: Task Management UI

**User Story:** As a user, I want to manage tasks with priority and status tracking, so that I can stay organized with my follow-up actions.

#### Acceptance Criteria

1. THE Frontend SHALL display tasks in a filterable table with columns for title, associated customer, priority, status, and due date
2. THE Frontend SHALL provide filter controls for task status (todo, in_progress, done) and priority (low, medium, high)
3. WHEN a task due date has passed and the task status is not "done", THE Frontend SHALL visually highlight the task row as overdue
4. WHEN the user creates or updates a task, THE Frontend SHALL validate that the title field is not empty before submitting

### Requirement 9: Activity Feed

**User Story:** As a user, I want to view a chronological feed of all customer interactions, so that I can review communication history.

#### Acceptance Criteria

1. THE Frontend SHALL display activities in a reverse-chronological feed showing activity type, description, associated customer name, and timestamp
2. WHEN the user creates a new activity, THE Frontend SHALL prepend the new entry to the feed without requiring a page reload
3. THE Frontend SHALL display distinct visual indicators (icons and colors) for each activity type: call, email, meeting, and note

### Requirement 10: UI Design System

**User Story:** As a user, I want a consistent and visually appealing interface, so that the application feels professional and easy to navigate.

#### Acceptance Criteria

1. THE Frontend SHALL implement a consistent color scheme using CSS custom properties with a green-based primary palette matching the existing NexusCRM brand identity
2. THE Frontend SHALL use the Plus Jakarta Sans font family for all typography with appropriate weight variations for headings, body text, and labels
3. THE Frontend SHALL provide visual feedback on all interactive elements through hover states, focus indicators, and transition animations not exceeding 200 milliseconds
4. THE Frontend SHALL display toast notifications for successful operations and error states with auto-dismiss after 4 seconds
5. THE Frontend SHALL maintain WCAG 2.1 Level AA color contrast ratios for all text content

### Requirement 11: Comprehensive Test Coverage

**User Story:** As a developer, I want automated tests covering all API endpoints and business logic, so that regressions are caught before deployment.

#### Acceptance Criteria

1. THE Test_Suite SHALL include unit tests for all CRUD operations covering create, read, update, and delete paths for Customer, Deal, Task, and Activity entities
2. THE Test_Suite SHALL include integration tests for the authentication flow covering registration, login, token refresh, and protected route access
3. THE Test_Suite SHALL include tests verifying that invalid inputs return appropriate HTTP 422 validation error responses
4. THE Test_Suite SHALL include tests verifying that requests for non-existent resources return HTTP 404 responses
5. THE Test_Suite SHALL achieve a minimum of 80% code coverage across the Backend_API module
6. THE Test_Suite SHALL use an isolated in-memory SQLite database for each test function to prevent test interdependencies

### Requirement 12: Docker Compose Configuration

**User Story:** As a developer, I want a Docker Compose setup for local development and deployment, so that the application is easy to run in any environment.

#### Acceptance Criteria

1. THE Docker_Compose SHALL define separate services for the Backend_API and Frontend with appropriate networking between them
2. THE Docker_Compose SHALL configure volume mounts for local development enabling hot-reload of source code changes
3. THE Docker_Compose SHALL expose the Backend_API on port 8000 and the Frontend on port 3000
4. THE Docker_Compose SHALL include a health check for the Backend_API service that verifies the application is responding
5. WHEN `docker compose up` is executed, THE Docker_Compose SHALL start all services and have the application accessible within 30 seconds

### Requirement 13: CI Pipeline

**User Story:** As a developer, I want automated testing and linting on every code change, so that code quality is maintained consistently.

#### Acceptance Criteria

1. WHEN a push or pull request targets the main branch, THE CI_Pipeline SHALL execute the full Test_Suite
2. WHEN any test in the Test_Suite fails, THE CI_Pipeline SHALL report the failure and block the merge
3. THE CI_Pipeline SHALL run Python linting using ruff and type checking using mypy on the Backend_API code
4. THE CI_Pipeline SHALL run TypeScript type checking and ESLint on the Frontend code
5. THE CI_Pipeline SHALL complete all checks within 5 minutes for a typical code change

### Requirement 14: CD Pipeline

**User Story:** As a developer, I want automated deployment on successful merges to main, so that releases are consistent and reliable.

#### Acceptance Criteria

1. WHEN code is merged to the main branch and all CI checks pass, THE CD_Pipeline SHALL build a Docker image tagged with both "latest" and the git commit SHA
2. THE CD_Pipeline SHALL push the built Docker image to Docker Hub using configured repository credentials
3. IF the Docker image build fails, THEN THE CD_Pipeline SHALL report the failure and halt the deployment process
4. THE CD_Pipeline SHALL only execute after the CI_Pipeline completes successfully

### Requirement 15: Login Page UI

**User Story:** As a user, I want a professional login page, so that I can securely access the CRM system.

#### Acceptance Criteria

1. THE Frontend SHALL display a login page with username and password fields and a submit button styled consistently with the application design system
2. WHEN the user submits valid credentials, THE Frontend SHALL store the Access_Token and Refresh_Token securely and redirect to the Dashboard
3. WHEN the user submits invalid credentials, THE Frontend SHALL display an error message below the form without clearing the username field
4. WHILE the login request is in progress, THE Frontend SHALL display a loading indicator on the submit button and disable the form inputs
5. WHEN the user is not authenticated, THE Frontend SHALL redirect all protected routes to the login page
