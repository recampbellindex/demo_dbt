-- liquibase formatted sql

-- changeset JBennett:1755033235424-1 labels:"add_email_column" splitStatements:false
ALTER TABLE PUBLIC.CUSTOMERS ADD EMAIL VARCHAR(255);

--rollback empty;
               
--changeset JBennett:seed_customer_emails labels:add_email_column
UPDATE PUBLIC.customers SET email = 'alice.smith@example.com' WHERE customer_id = 1;
UPDATE PUBLIC.customers SET email = 'bob.johnson@example.com' WHERE customer_id = 2;
UPDATE PUBLIC.customers SET email = 'carlos.diaz@example.com' WHERE customer_id = 3;
UPDATE PUBLIC.customers SET email = 'dana.lee@example.com' WHERE customer_id = 4;
--rollback UPDATE PUBLIC.customers SET email = NULL WHERE customer_id IN (1, 2, 3, 4);
