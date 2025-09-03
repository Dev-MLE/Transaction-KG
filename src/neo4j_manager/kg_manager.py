from neo4j import GraphDatabase
import pandas as pd


class Neo4jKGManager:
    def __init__(self, uri, username, password):
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        self.driver.close()

    def create_constraints(self):
        with self.driver.session() as session:
            queries = [
                "CREATE CONSTRAINT account_code_unique IF NOT EXISTS FOR (a:Account) REQUIRE a.code IS UNIQUE",
                "CREATE CONSTRAINT transaction_voucher_unique IF NOT EXISTS FOR (t:Transaction) REQUIRE t.voucher_no IS UNIQUE",
                "CREATE CONSTRAINT amount_id_unique IF NOT EXISTS FOR (amt:Amount) REQUIRE amt.id IS UNIQUE",
                "CREATE CONSTRAINT month_value_unique IF NOT EXISTS FOR (m:Month) REQUIRE m.value IS UNIQUE"
            ]
            for query in queries:
                session.run(query)
                print(f"Executed: {query}")

    def import_data(self, df: pd.DataFrame, batch_size=2000):
        total_batches = (len(df) // batch_size) + 1

        for i in range(0, len(df), batch_size):
            batch = df.iloc[i:i+batch_size].copy()
            batch['Transaction Date'] = pd.to_datetime(batch['Transaction Date'], errors="coerce")
            batch['Transaction Date'] = batch['Transaction Date'].dt.strftime('%Y-%m-%d')

            # Convert to dict
            records = batch.to_dict("records")

            query = """
            UNWIND $rows AS row
            MERGE (acc:Account {code: row.`Account Code`})
              SET acc.name = row.`Account Name`,
                  acc.class = row.`Class Name`

            MERGE (t:Transaction {voucher_no: row.`Voucher No`})
              SET t.date = date(row.`Transaction Date`),
                  t.description = row.Description

            MERGE (m:Month {value: row.Month})
            MERGE (t)-[:OCCURRED_IN]->(m)

            FOREACH (_ IN CASE WHEN row.`Debit Amount` > 0 THEN [1] ELSE [] END |
                MERGE (amt:Amount {id: row.`Voucher No` + "-D-" + row.`Account Code`})
                  SET amt.type = 'Debit', amt.value = row.`Debit Amount`
                MERGE (t)-[:HAS_DEBIT]->(amt)
                MERGE (amt)-[:TO]->(acc)
            )

            FOREACH (_ IN CASE WHEN row.`Credit Amount` > 0 THEN [1] ELSE [] END |
                MERGE (amt:Amount {id: row.`Voucher No` + "-C-" + row.`Account Code`})
                  SET amt.type = 'Credit', amt.value = row.`Credit Amount`
                MERGE (t)-[:HAS_CREDIT]->(amt)
                MERGE (amt)-[:FROM]->(acc)
            )
            """
            with self.driver.session() as session:
                session.run(query, rows=records)

            print(f"Processed batch {i//batch_size + 1}/{total_batches}")
