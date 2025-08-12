<p align="left">
  <img src="img/liquibase.png" alt="Liquibase Logo" title="Liquibase Logo" width="324" height="72">
</p>

This repository contains a Liquibase, Snowflake, and DBT demo. Liquibase licenses Snowflake by schema.

Authentication is done using public/private keys using the instructions [here](https://support.liquibase.com/hc/en-us/articles/29494828838683-How-to-configure-Liquibase-to-connect-to-Snowflake-using-a-Private-Key).

# ✔️ Pre-Demo Steps
1. Pull the repo to ensure you have all available updated files<br>
     ```
     git pull
     ```
1. Update the [liquibase.properties](liquibase.properties) file as required.
1. Update the [profiles.yml](profiles.yml) file as required. More information can be found [here](https://docs.getdbt.com/docs/core/connect-data-platform/profiles.yml).

# 📋 Demo Steps
1. **Create Base Objects**
    1. Run the flow file to create the base objects needed by the models. This also runs DBT.
    ```
    liquibase flow
    ```
    2. Base objects are created in the PUBLIC schema. DBT is configured to create objects in the DBT schema.
1. **Update Customer Model**
    1. Execute the following SQL to create a new column in the database.
    ```
    ALTER TABLE PUBLIC.CUSTOMERS ADD COLUMN EMAIL VARCHAR(255);
    ```
    2. Execute the incremental flow file to generate a new changelog for the column. This also invokes [seed_email.py](Scripts/seed_email.py) to add a new changeset to seed the column with data.
    ```
    liquibase flow --flow-file=liquibase.incremental.yaml
    ```
    3. Edit the [customer_order_summary.sql](../models/customer_order_summary.sql) model file and add email column to the select statement (line 22).
    ```
    customers as (
        select
            customer_id,
            customer_name,
            email,
            signup_date,
            country_code,
            is_active
        from {{ source('prod', 'customers') }}
    ),
    ```
    4. Add the email column to the "final as" statement (line 59).
    ```
    final as (
        select
            c.customer_id,
            c.customer_name,
            c.email,
            coalesce(ao.order_count, 0) as order_count,
            coalesce(ao.total_spent, 0) as total_spent,
            ao.last_order_date,
            case 
                when ao.total_spent > 1000 then 'high_value'
                else 'regular'
            end as customer_type,
            ro.order_id as most_recent_order_id
        from customers c
        left join aggregated_orders ao on c.customer_id = ao.customer_id
        left join recent_orders ro on c.customer_id = ro.customer_id and ro.order_rank = 1
    )
    ```
    5. Execute the main flow to create the column and update DBT.
    ```
    liquibase flow
    ```

# 🏁 Reset
Execute the following steps to ready the environment for the next demo.
1. Drop changes
    ```
    liquibase flow --flow-file=liquibase.reset.yaml
    ```
1. Update model<br>
Edit the [customer_order_summary.sql](../models/customer_order_summary.sql) model file and remove email from the select statements (lines 26 and 59). 
1. Update repository
```
git commit -am "Reset files"
git push
```
4. Remove DBT objects (optional)
Execute these queries
```
DROP SCHEMA DBT CASCADE;
CREATE SCHEMA DBT;
```

# ☎️ Contact Liquibase
Liquibase sales: https://www.liquibase.com/contact-us<br>
Liquibase support: https://support.liquibase.com