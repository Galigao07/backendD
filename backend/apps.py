from django.apps import AppConfig
from django.db import connection

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'

    def ready(self):
        self.add_columns_if_not_exist()
        self.add_user_columns_if_not_exist()
        self.create_unmanaged_tables()
        self.add_tbl_product_site_setup_columns_if_not_exist()
        # import backend.signals

    def add_columns_if_not_exist(self):
        columns_to_add = [
            ("withHotel", "VARCHAR(6)", "'False'"),
            ("ProductColPerRows", "INT", "6"),
            ("TableColPerRows", "INT", "6"),
            ("ShowArrowUpAndDown", "VARCHAR(6)", "'False'"),
        ]

        with connection.cursor() as cursor:
            for col_name, col_type, default_value in columns_to_add:
                try:
                    # ✅ MySQL-safe check with table_schema
                    cursor.execute(f"""
                        SELECT column_name 
                        FROM information_schema.columns
                        WHERE table_schema = DATABASE()
                        AND table_name = 'tbl_pos_settings'
                        AND column_name = '{col_name}';
                    """)
                    exists = cursor.fetchone()

                    # Add column if it doesn't exist
                    if not exists:
                        cursor.execute(f"""
                            ALTER TABLE tbl_pos_settings
                            ADD COLUMN {col_name} {col_type} DEFAULT {default_value};
                        """)
                        print(f"✅ Column '{col_name}' added to tbl_pos_settings.")
                    else:
                        print(f"ℹ️ Column '{col_name}' already exists.")
                except Exception as e:
                    print(f"⚠️ Error adding column '{col_name}': {e}")

    def add_user_columns_if_not_exist(self):
        columns_to_add = [
            ("username", "VARCHAR(150)", "''"),
            ("email", "VARCHAR(254)", "''"),
            ("password", "VARCHAR(128)", "''"),
            ("first_name", "VARCHAR(150)", "''"),
            ("last_name", "VARCHAR(150)", "''"),
            ("is_active", "TINYINT(1)", "1"),
            ("is_staff", "TINYINT(1)", "0"),
            ("is_superuser", "TINYINT(1)", "0"),
            ("date_joined", "DATETIME", "CURRENT_TIMESTAMP"),
            ("last_login", "DATETIME", None),
        ]

        with connection.cursor() as cursor:
            for col_name, col_type, default_value in columns_to_add:
                try:
                    # ✅ MySQL schema-aware column check
                    cursor.execute(f"""
                        SELECT column_name
                        FROM information_schema.columns
                        WHERE table_schema = DATABASE()
                        AND table_name = 'tbl_user'
                        AND column_name = '{col_name}';
                    """)
                    exists = cursor.fetchone()

                    if not exists:
                        # ✅ Handle columns with NULL default
                        if default_value is None:
                            default_sql = ""
                        else:
                            default_sql = f"DEFAULT {default_value}"

                        cursor.execute(f"""
                            ALTER TABLE tbl_user
                            ADD COLUMN {col_name} {col_type} {default_sql};
                        """)
                        print(f"✅ Added column '{col_name}' to tbl_user.")
                    else:
                        print(f"ℹ️ Column '{col_name}' already exists in tbl_user.")
                except Exception as e:
                    print(f"⚠️ Error adding column '{col_name}': {e}")

    def add_tbl_product_site_setup_columns_if_not_exist(self):
        columns_to_add = [
                ("sys_type", "VARCHAR(150)", "''"),
                
            ]

        with connection.cursor() as cursor:
                for col_name, col_type, default_value in columns_to_add:
                    try:
                        # ✅ MySQL schema-aware column check
                        cursor.execute(f"""
                            SELECT column_name
                            FROM information_schema.columns
                            WHERE table_schema = DATABASE()
                            AND table_name = 'tbl_product_site_setup'
                            AND column_name = '{col_name}';
                        """)
                        exists = cursor.fetchone()

                        if not exists:
                            # ✅ Handle columns with NULL default
                            if default_value is None:
                                default_sql = ""
                            else:
                                default_sql = f"DEFAULT {default_value}"

                            cursor.execute(f"""
                                ALTER TABLE tbl_product_site_setup
                                ADD COLUMN {col_name} {col_type} {default_sql};
                            """)
                            print(f"✅ Added column '{col_name}' to tbl_product_site_setup.")
                        else:
                            print(f"ℹ️ Column '{col_name}' already exists in tbl_product_site_setup.")
                    except Exception as e:
                        print(f"⚠️ Error adding column '{col_name}': {e}")


    def create_unmanaged_tables(self):
        tables = {
            "tbl_pos_client_setup": """
                CREATE TABLE IF NOT EXISTS tbl_pos_client_setup (
                    autonum INT AUTO_INCREMENT PRIMARY KEY,
                    company_code INT DEFAULT 0,
                    company_name VARCHAR(225) DEFAULT '',
                    company_name2 VARCHAR(225) DEFAULT '',
                    company_address VARCHAR(225) DEFAULT '',
                    company_address2 VARCHAR(225) DEFAULT '',
                    company_address3 VARCHAR(225) DEFAULT '',
                    tel_no VARCHAR(50) DEFAULT '',
                    tin VARCHAR(50) DEFAULT '',
                    remarks VARCHAR(225) DEFAULT '',
                    remarks2 VARCHAR(225) DEFAULT '',
                    remarks3 VARCHAR(225) DEFAULT ''
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,
            "tbl_lead_setup": """
                CREATE TABLE IF NOT EXISTS tbl_lead_setup (
                    autonum INT AUTO_INCREMENT PRIMARY KEY,
                    company_code INT DEFAULT 0,
                    company_name VARCHAR(225) DEFAULT '',
                    company_name2 VARCHAR(225) DEFAULT '',
                    company_address VARCHAR(225) DEFAULT '',
                    company_address2 VARCHAR(225) DEFAULT '',
                    tin VARCHAR(50) DEFAULT '',
                    accreditation_no VARCHAR(50) DEFAULT '',
                    date_issued VARCHAR(50) DEFAULT '',
                    date_valid VARCHAR(50) DEFAULT ''
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
            """,    
              "tmp_tbl_pos_web_sc_discount_list": """
            CREATE TABLE IF NOT EXISTS tmp_tbl_pos_web_sc_discount_list (
            id BIGINT(20) NOT NULL AUTO_INCREMENT,
            terminal_no BIGINT(11) DEFAULT 0,
            site_no BIGINT(11) DEFAULT 0,
            so_no BIGINT(11) DEFAULT 0,
            cashier_id BIGINT(11) DEFAULT 0,
            SeniorCount BIGINT(11) DEFAULT 0,
            SGuestCount BIGINT(11) DEFAULT 0,
            SAmountCovered DOUBLE(9,3) DEFAULT 0.000,
            SVatSales DOUBLE(9,3) DEFAULT 0.000,
            SLessVat12 DOUBLE(9,3) DEFAULT 0.000,
            SNetOfVat DOUBLE(9,3) DEFAULT 0.000,
            SLess20SCDiscount DOUBLE(9,3) DEFAULT 0.000,
            SDiscountedPrice DOUBLE(9,3) DEFAULT 0.000,
            PRIMARY KEY (id)
            ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
            """,
                "tmp_tbl_pos_web_sc_discount_listing": """
                CREATE TABLE IF NOT EXISTS tmp_tbl_pos_web_sc_discount_listing (
                id BIGINT(20) NOT NULL AUTO_INCREMENT,
                terminal_no BIGINT(11) DEFAULT 0,
                site_no BIGINT(11) DEFAULT 0,
                cashier_id BIGINT(11) DEFAULT 0,
                so_no BIGINT(11) DEFAULT 0,
                SID BIGINT(11) DEFAULT 0,
                SNAME VARCHAR(225) DEFAULT '',
                STIN VARCHAR(225) DEFAULT '',
                PRIMARY KEY (id)
                ) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4;
                """
        }

        with connection.cursor() as cursor:
            for table_name, create_sql in tables.items():
                try:
                    cursor.execute(create_sql)
                    print(f"✅ Table '{table_name}' ensured.")
                except Exception as e:
                    print(f"⚠️ Error creating table '{table_name}': {e}")
    # def add_columns_if_not_exist(self):
    #     with connection.cursor() as cursor:
    #         try:
    #             # Check if column exists
    #             cursor.execute("""
    #                 SELECT column_name 
    #                 FROM information_schema.columns
    #                 WHERE table_name = 'tbl_pos_settings'
    #                 AND column_name = 'TableColPerRows';
    #             """)
    #             exists = cursor.fetchone()

    #             if not exists:
    #                 cursor.execute("""
    #                     ALTER TABLE tbl_pos_settings
    #                     ADD COLUMN withHotel VARCHAR(6) DEFAULT 'False',
    #                     ADD COLUMN ProductColPerRows INT DEFAULT 6,
    #                     ADD COLUMN TableColPerRows INT DEFAULT 6,
    #                     ADD COLUMN ShowArrowUpAndDown VARCHAR(6) DEFAULT 'False';
    #                 """)
    #         except Exception as e:
    #             print(f"⚠️ Error updating tbl_pos_settings: {e}")
