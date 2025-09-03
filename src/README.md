# 🧠 Financial Knowledge Graph (Neo4j + Python)

This project builds a **Knowledge Graph (KG)** from financial transactions (credits, debits, accounts, vouchers, months).  
It allows you to **import Excel transaction data into Neo4j** and then perform **reasoning, analysis, and visualization**.


---

## 🚀 Setup

Install poetry using "pip install poetry" or pip install pipx
Then 
"pipx install poetry".

## 🌐 How to Access Neo4j

Follow these steps to access and explore the Knowledge Graph in Neo4j:

###  Create a Neo4j AuraDB Account
1. Go to [Neo4j AuraDB Free](https://neo4j.com/cloud/platform/aura-free/).
2. Sign up (or log in).
3. Click **"New Instance"** → select **Aura Free**.
4. Choose a **Region** (closest to you).
5. Set a **Database password** → save this securely.

---

###  Download Connection Credentials
1. In the AuraDB dashboard, click **"Connect"** on your instance.
2. Choose **"Connection details" → Download credentials (.txt)**.



### 1. Install dependencies
```bash
poetry install
```

### 2. Activate environment
```bash
poetry shell
```

### 3. Store Neo4j credentials  
Create a file `Neo4j-credentials.txt` in the project root:

```
NEO4J_URI=neo4j+s://<your-uri>.databases.neo4j.io
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-password
```

### 4. Prepare transaction data  
Put your data file in the project root as `transactions.xlsx`.  
It must have these columns:
- `Voucher No`  
- `Transaction Date`  
- `Account Code`  
- `Account Name`  
- `Class Name`  
- `Description`  
- `Debit Amount`  
- `Credit Amount`

---

## ▶️ Running the Import

```bash
poetry run python src/main.py
```

This will:
1. Connect to Neo4j AuraDB.  
2. Create unique constraints on Accounts, Transactions, Months, and Amounts.  
3. Batch-import the Excel file into the graph.  
4. Print progress while importing.  

After completion, open **Neo4j Browser** (`https://console.neo4j.io`) and run queries.

---

## 🔎 Example Queries

Here are **ready-to-run Cypher queries** to analyze your graph:

### 1. Show all transactions in 2024
```cypher
MATCH (t:Transaction)-[:OCCURRED_IN]->(m:Month)
WHERE m.value STARTS WITH "2024"
RETURN t.voucher_no AS Voucher, t.date AS Date, t.description AS Description
LIMIT 20;
```

---

### 2. Pick a random day’s transactions (e.g., 2024-07-15)
```cypher
MATCH (t:Transaction)
WHERE t.date = date("2024-07-15")
OPTIONAL MATCH (t)-[:HAS_DEBIT]->(d:Amount)-[:TO]->(accD:Account)
OPTIONAL MATCH (t)-[:HAS_CREDIT]->(c:Amount)-[:FROM]->(accC:Account)
RETURN t.voucher_no AS Voucher, t.date AS Date, 
       collect(DISTINCT accD.name) AS DebitAccounts,
       collect(DISTINCT accC.name) AS CreditAccounts,
       collect(DISTINCT d.value) AS DebitValues,
       collect(DISTINCT c.value) AS CreditValues
LIMIT 5;
```

---

### 3. Top 10 accounts by debit amount
```cypher
MATCH (:Transaction)-[:HAS_DEBIT]->(amt:Amount)-[:TO]->(acc:Account)
RETURN acc.name AS Account, SUM(amt.value) AS TotalDebit
ORDER BY TotalDebit DESC
LIMIT 10;
```

---

### 4. Net balance per account
```cypher
MATCH (acc:Account)
OPTIONAL MATCH (acc)<-[:TO]-(d:Amount {type:'Debit'})
OPTIONAL MATCH (acc)<-[:FROM]-(c:Amount {type:'Credit'})
RETURN acc.code AS AccountCode, acc.name AS AccountName,
       coalesce(SUM(d.value),0) - coalesce(SUM(c.value),0) AS NetBalance
ORDER BY NetBalance DESC;
```

---

### 5. Monthly summary (2024)
```cypher
MATCH (t:Transaction)-[:OCCURRED_IN]->(m:Month)
OPTIONAL MATCH (t)-[:HAS_DEBIT]->(d:Amount)
OPTIONAL MATCH (t)-[:HAS_CREDIT]->(c:Amount)
WHERE m.value STARTS WITH "2024"
RETURN m.value AS Month,
       SUM(d.value) AS TotalDebits,
       SUM(c.value) AS TotalCredits,
       SUM(d.value) - SUM(c.value) AS Net
ORDER BY Month;
```

---

### 6. Trace full path of a transaction
```cypher
MATCH (t:Transaction {voucher_no: "12345"})
OPTIONAL MATCH path = (t)-[*1..3]-(n)
RETURN path;
```

This gives a **visual graph of the transaction**, showing accounts, amounts, and months.

---

## 📊 Visualizing in Neo4j Browser

To see your graph visually:
1. Run any query above in [Neo4j Browser](https://console.neo4j.io).  
2. Switch to the **Graph view** (circle diagram).  
3. Drag nodes to rearrange and explore relationships.  
   - Accounts (🟢)  
   - Transactions (🔵)  
   - Amounts (🟡)  
   - Months (🟣)  

---

## 🧩 Future Extensions
- Add **Graph Data Science (GDS)** for anomaly detection.  
- Build a **FastAPI app** to expose KG queries via REST.  
- Create a **Streamlit dashboard** for non-technical users.  

---

