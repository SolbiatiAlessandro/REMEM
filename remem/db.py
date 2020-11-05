"""
CREATE TABLE transcripts (
	transcript_id serial PRIMARY KEY,
	content TEXT,
	created_on TIMESTAMP NOT NULL DEFAULT NOW()
);
 ALTER TABLE transcripts ADD COLUMN job_id VARCHAR(100);
"""
import psycopg2

def add_transcript(content: str, job_id: str):
    conn = psycopg2.connect("dbname=remem user=remem password=remem")
    cur = conn.cursor()
    cur.execute("INSERT INTO transcripts (content, job_id) VALUES (%s, %s)", (content, job_id))
    conn.commit()
    cur.close()
    conn.close()
