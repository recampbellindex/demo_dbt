# Repository Metadata

## Basic Information
- **Repository Name**: demo_dbt
- **Description**: Comprehensive Liquibase and dbt integration with Snowflake, demonstrating automated schema evolution and analytics model updates
- **Created Date**: 2025-08-12
- **Last Updated**: 2025-08-12
- **Complexity Level**: Advanced

## Database Configuration
- **Database Type**: Snowflake
- **Database Version**: Cloud (latest)
- **Connection Method**: JDBC with PKI authentication
- **Schema Management**: Multi-schema (PUBLIC for raw data, DBT for transformed models)

## Platform Integration
- **CI/CD Platform**: Git-based workflow
- **Cloud Provider**: Snowflake Cloud
- **Container Platform**: None
- **Infrastructure as Code**: None

## Liquibase Features
- **Liquibase Edition**: Pro
- **Liquibase Version**: Latest
- **Key Features Used**:
  - [x] Flow
  - [ ] Drift Detection
  - [x] Policy Checks
  - [x] Generate Changelog
  - [x] Rollback
  - [ ] Targeted Updates
  - [ ] Structured Logging
  - [x] Other: Python integration, DBT integration, Incremental changelog generation

## Use Cases
- **Primary Use Case**: Automated integration between Liquibase schema management and dbt analytics transformations in Snowflake environments
- **Secondary Use Cases**: Incremental schema evolution with automated model updates, demonstration of database-first analytics workflows
- **Industry/Domain**: Analytics/Data Engineering
- **Team Size**: Medium 5-20

## Customer Scenarios
- **Target Customer Profile**: Data engineering teams using both database schema management and analytics transformations, organizations needing coordinated database and model changes
- **Common Pain Points Addressed**: Manual coordination between schema changes and analytics models, complex change propagation across database layers
- **Business Value Delivered**: Automated analytics pipeline updates, reduced manual coordination overhead, faster time-to-insights
- **Demo Duration**: 1hr

## Technical Patterns
- **Deployment Strategy**: Direct with coordinated dbt execution
- **Environment Management**: Dev/QA/Prod through profiles and Flow files
- **Secrets Management**: PKI authentication for Snowflake, dbt profile management
- **Monitoring & Logging**: Liquibase Flow reporting, dbt run logs

## Dependencies
- **External Tools**: dbt Core, Python 3.x, Snowflake CLI tools
- **Third-party Integrations**: dbt-snowflake adapter, Python scripts for automation
- **Prerequisites**: Snowflake account with multiple schema privileges, dbt installation and configuration

## Customization Points
- **Easily Configurable**: Database connections, dbt profile settings, schema names, model selection
- **Requires Modification**: Python automation scripts, dbt model structure, Flow file orchestration
- **Not Recommended to Change**: Core integration patterns between Liquibase and dbt, authentication mechanisms

## Known Limitations
- **Platform Limitations**: Requires coordination between Liquibase and dbt execution timing
- **Scale Limitations**: Large model rebuilds can be time-intensive, complex dependency chains require careful orchestration
- **Feature Gaps**: No automated conflict resolution between schema changes and model dependencies

## Related Repositories
- **Similar Patterns**: Snowflake_private_key (Snowflake authentication), any Flow-based repositories
- **Dependencies**: Requires understanding of both Liquibase and dbt concepts
- **Alternatives**: Separate schema and analytics management approaches, database-last analytics patterns