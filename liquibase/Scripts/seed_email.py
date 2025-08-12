import sys

if len(sys.argv) != 4:
    print("Usage: python seed_email.py <file_path> <author> <label filter>")
    sys.exit(1)

file_path = sys.argv[1]
author = sys.argv[2]
label_filter = sys.argv[3]

with open(file_path, 'a') as file:
    file.write(f"""--rollback empty;
               
--changeset {author}:seed_customer_emails labels:{label_filter}
UPDATE PUBLIC.customers SET email = 'alice.smith@example.com' WHERE customer_id = 1;
UPDATE PUBLIC.customers SET email = 'bob.johnson@example.com' WHERE customer_id = 2;
UPDATE PUBLIC.customers SET email = 'carlos.diaz@example.com' WHERE customer_id = 3;
UPDATE PUBLIC.customers SET email = 'dana.lee@example.com' WHERE customer_id = 4;
--rollback UPDATE PUBLIC.customers SET email = NULL WHERE customer_id IN (1, 2, 3, 4);
""")