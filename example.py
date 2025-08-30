import logging

from polygon.environment import Environment
from polygon.logger import logger
from polygon.testers.mysql_tester import DB_CONFIG, MySQLTester


def main():
    logger.setLevel(logging.INFO)

    # specify the schema and constraints
    schema = [
        {
            "TableName": "Customers",
            "PKeys": [
                {
                    "Name": "customer_id",
                    "Type": "int"
                }
            ],
            "FKeys": [],
            "Others": [
                {
                    "Name": "customer_name",
                    "Type": "varchar"
                },
                {
                    "Name": "email",
                    "Type": "varchar"
                }
            ]
        },
        {
            "TableName": "Contacts",
            "PKeys": [
                {
                    "Name": "user_id",
                    "Type": "int"
                },
                {
                    "Name": "contact_email",
                    "Type": "varchar"
                }
            ],
            "FKeys": [],
            "Others": [
                {
                    "Name": "contact_name",
                    "Type": "varchar"
                }
            ]
        },
        {
            "TableName": "Invoices",
            "PKeys": [
                {
                    "Name": "invoice_id",
                    "Type": "int"
                }
            ],
            "FKeys": [
                {
                    "FName": "user_id",
                    "PName": "customer_id",
                    "PTable": "0"
                }
            ],
            "Others": [
                {
                    "Name": "price",
                    "Type": "int"
                }
            ]
        }
    ]
    constraints = [{'distinct': ['Customers.customer_id']},
                   {'distinct': ['Contacts.user_id', 'Contacts.contact_email']}, {'distinct': ['Invoices.invoice_id']},
                   {'gt': ['Invoices.price', 0]}, {'eq': ['Contacts.user_id', 'Customers.customer_id']},
                   {'eq': ['Invoices.user_id', 'Customers.customer_id']},
                   {'join': ['Customers.customer_name', 'Contacts.contact_name']},
                   {'join': ['Customers.email', 'Contacts.contact_email']}, {
                       'if': [{'col1a': 'Customers.customer_name'}, {'comp1': 'equal'},
                              {'col1b': 'Contacts.contact_name'}, {'col2a': 'Customers.email'}, {'comp2': 'equal'},
                              {'col2b': 'Contacts.contact_email'}]}]

    # create an environment
    env = Environment(schema, constraints, bound=2, time_budget=60)

    # specify the queries
    queries = [
        """
        SELECT INVOICE_ID, T.CUSTOMER_NAME, PRICE, CONTACTS_CNT, TRUSTED_CONTACTS_CNT
        FROM INVOICES I LEFT JOIN (
          SELECT A.CUSTOMER_ID, CUSTOMER_NAME, COUNT(CONTACT_NAME) AS CONTACTS_CNT,
                 SUM(CASE WHEN CONTACT_EMAIL IN (SELECT EMAIL FROM CUSTOMERS) THEN 1 ELSE 0 END) AS TRUSTED_CONTACTS_CNT
          FROM CUSTOMERS A LEFT JOIN CONTACTS B
          ON A.CUSTOMER_ID = B.USER_ID
          GROUP BY A.CUSTOMER_ID, CUSTOMER_NAME
          ) T
          ON I.USER_ID = T.CUSTOMER_ID
          ORDER BY 1
        """,
        """
        SELECT INVOICE_ID, C.CUSTOMER_NAME, PRICE, COUNT(T.CONTACT_NAME) CONTACTS_CNT, COUNT(C1.EMAIL) TRUSTED_CONTACTS_CNT
        FROM INVOICES I LEFT JOIN CUSTOMERS C
        ON I.USER_ID = C.CUSTOMER_ID
        LEFT JOIN CONTACTS T ON C.CUSTOMER_ID = T.USER_ID
        LEFT JOIN CUSTOMERS C1 ON T.CONTACT_EMAIL = C1.EMAIL
        GROUP BY 1,2,3
        ORDER BY INVOICE_ID
        """
    ]

    # run
    eq, cex, checking_time, total_time, ret = env.check(*queries, use_precise_encoding=False)
    print(f'Running time: {total_time}')
    print(f'Result: ', end='')

    if eq is None:
        print('ERR')
    else:
        if not eq:
            print('NEQ')
            logger.info(f'Counterexample: {cex}')
            with MySQLTester(DB_CONFIG, schema) as tester:
                tester.create_all_databases([cex], constraints)
                rejected = tester.test_pair(*queries)
                print('Refuted:', rejected)
        else:
            print('EQ')


if __name__ == '__main__':
    main()
