# setup_db.py
import os
import mysql.connector
from mysql.connector import Error

def setup_database():
    """
    Setup database and table for the fake job detector.
    Creates database and predictions table if they don't exist.
    """
    
    # Get database credentials from environment
    host = os.getenv("MYSQL_HOST")
    user = os.getenv("MYSQL_USER")
    password = os.getenv("MYSQL_PASSWORD", "")
    port = int(os.getenv("MYSQL_PORT", "3306"))
    database = os.getenv("MYSQL_DATABASE", "fake_job_detector")
    
    # Check if logging is enabled
    if os.getenv("ENABLE_DB_LOGGING", "false").lower() != "true":
        print("ℹ️ Database logging is disabled. Skipping setup.")
        return
    
    # Validate required credentials
    if not all([host, user]):
        print("⚠️ Missing database credentials. Please set MYSQL_HOST and MYSQL_USER.")
        return
    
    try:
        # Step 1: Connect without database specified first
        print("🔄 Connecting to MySQL server...")
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password
        )
        cursor = conn.cursor()
        
        # Step 2: Create database
        print(f"🔄 Creating database '{database}' if not exists...")
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database}")
        print(f"✅ Database '{database}' created/verified")
        
        # Step 3: Use database and create table
        print(f"🔄 Using database '{database}'...")
        cursor.execute(f"USE {database}")
        
        print("🔄 Creating table 'predictions'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS predictions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                input_text TEXT,
                prediction VARCHAR(20),
                fraud_probability DECIMAL(5,2),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        print("✅ Table 'predictions' created/verified")
        
        # Create indexes for better performance
        print("🔄 Creating indexes...")
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_created_at 
                ON predictions(created_at DESC)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_prediction 
                ON predictions(prediction)
            """)
            print("✅ Indexes created/verified")
        except Error as e:
            # Some MySQL versions don't support IF NOT EXISTS for indexes
            if "Duplicate key name" in str(e):
                print("ℹ️ Indexes already exist")
            else:
                print(f"⚠️ Index creation warning: {e}")
        
        # Step 4: Create an optional view for analytics
        print("🔄 Creating analytics view...")
        try:
            cursor.execute("""
                CREATE OR REPLACE VIEW prediction_summary AS
                SELECT 
                    DATE(created_at) as date,
                    prediction,
                    COUNT(*) as count,
                    AVG(fraud_probability) as avg_fraud_score
                FROM predictions
                GROUP BY DATE(created_at), prediction
            """)
            print("✅ Analytics view created/verified")
        except Error as e:
            print(f"ℹ️ View creation skipped: {e}")
        
        conn.commit()
        cursor.close()
        conn.close()
        print("🎉 Database setup complete successfully!")
        return True
        
    except Error as e:
        print(f"❌ Database setup failed: {e}")
        return False

def verify_database():
    """Verify database connection and table exists."""
    try:
        host = os.getenv("MYSQL_HOST")
        user = os.getenv("MYSQL_USER")
        password = os.getenv("MYSQL_PASSWORD", "")
        port = int(os.getenv("MYSQL_PORT", "3306"))
        database = os.getenv("MYSQL_DATABASE", "fake_job_detector")
        
        if not all([host, user]):
            return False
        
        conn = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=database
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM predictions")
        count = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        print(f"✅ Database verified: {count} records found")
        return True
        
    except Error as e:
        print(f"⚠️ Database verification failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🚀 Fake Job Detector - Database Setup")
    print("=" * 50)
    
    success = setup_database()
    if success:
        verify_database()
    else:
        print("⚠️ Please check your environment variables and try again.")
