# HBase bulk load script
# Run with: hbase shell < load_customers.sh

put 'customer_profiles', 'C001', 'info:name', 'Alice Johnson'
put 'customer_profiles', 'C001', 'info:email', 'alice@example.com'
put 'customer_profiles', 'C001', 'info:city', 'Mumbai'
put 'customer_profiles', 'C002', 'info:name', 'Bob Smith'
put 'customer_profiles', 'C002', 'info:email', 'bob@example.com'
put 'customer_profiles', 'C002', 'info:city', 'Delhi'
put 'customer_profiles', 'C003', 'info:name', 'Charlie Brown'
put 'customer_profiles', 'C003', 'info:email', 'charlie@example.com'
put 'customer_profiles', 'C003', 'info:city', 'Bangalore'
put 'customer_profiles', 'C004', 'info:name', 'Diana Prince'
put 'customer_profiles', 'C004', 'info:email', 'diana@example.com'
put 'customer_profiles', 'C004', 'info:city', 'Chennai'
put 'customer_profiles', 'C005', 'info:name', 'Evan Peters'
put 'customer_profiles', 'C005', 'info:email', 'evan@example.com'
put 'customer_profiles', 'C005', 'info:city', 'Hyderabad'