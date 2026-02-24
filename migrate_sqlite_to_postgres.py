import os
import sqlite3

import psycopg


def create_postgres_tables(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS students (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                roll_no TEXT NOT NULL UNIQUE,
                email TEXT,
                password_hash TEXT,
                reset_otp TEXT,
                reset_otp_expires BIGINT,
                department TEXT,
                semester TEXT
            );

            CREATE TABLE IF NOT EXISTS attendance_records (
                id BIGSERIAL PRIMARY KEY,
                student_id BIGINT NOT NULL REFERENCES students(id) ON DELETE CASCADE,
                attendance_date TEXT NOT NULL,
                subject TEXT NOT NULL,
                status INTEGER NOT NULL CHECK(status IN (0, 1))
            );

            CREATE TABLE IF NOT EXISTS teachers (
                id BIGSERIAL PRIMARY KEY,
                name TEXT NOT NULL,
                username TEXT NOT NULL UNIQUE,
                email TEXT,
                password_hash TEXT NOT NULL,
                reset_otp TEXT,
                reset_otp_expires BIGINT
            );

            CREATE UNIQUE INDEX IF NOT EXISTS idx_students_roll_no ON students(roll_no);
            CREATE INDEX IF NOT EXISTS idx_students_email ON students(email);
            CREATE UNIQUE INDEX IF NOT EXISTS idx_teachers_username ON teachers(username);
            CREATE INDEX IF NOT EXISTS idx_teachers_email ON teachers(email);
            """
        )
    pg_conn.commit()


def truncate_tables(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute("TRUNCATE TABLE attendance_records, teachers, students RESTART IDENTITY CASCADE")
    pg_conn.commit()


def reset_sequences(pg_conn):
    with pg_conn.cursor() as cur:
        cur.execute(
            """
            SELECT setval(
                pg_get_serial_sequence('students', 'id'),
                COALESCE((SELECT MAX(id) FROM students), 1),
                true
            )
            """
        )
        cur.execute(
            """
            SELECT setval(
                pg_get_serial_sequence('teachers', 'id'),
                COALESCE((SELECT MAX(id) FROM teachers), 1),
                true
            )
            """
        )
        cur.execute(
            """
            SELECT setval(
                pg_get_serial_sequence('attendance_records', 'id'),
                COALESCE((SELECT MAX(id) FROM attendance_records), 1),
                true
            )
            """
        )
    pg_conn.commit()


def migrate():
    sqlite_path = os.environ.get("ATTENDANCE_DB_PATH", "").strip() or "attendance.db"
    database_url = os.environ.get("DATABASE_URL", "").strip()

    if not database_url:
        raise RuntimeError("DATABASE_URL is required for PostgreSQL migration.")
    if not os.path.exists(sqlite_path):
        raise RuntimeError(f"SQLite file not found: {sqlite_path}")

    sqlite_conn = sqlite3.connect(sqlite_path)
    sqlite_conn.row_factory = sqlite3.Row
    pg_conn = psycopg.connect(database_url)

    try:
        create_postgres_tables(pg_conn)
        truncate_tables(pg_conn)

        students = sqlite_conn.execute(
            """
            SELECT id, name, first_name, last_name, roll_no, email, password_hash,
                   reset_otp, reset_otp_expires, department, semester
            FROM students
            ORDER BY id
            """
        ).fetchall()
        with pg_conn.cursor() as cur:
            with cur.copy(
                """
                COPY students(
                    id, name, first_name, last_name, roll_no, email, password_hash,
                    reset_otp, reset_otp_expires, department, semester
                ) FROM STDIN
                """
            ) as copy:
                for row in students:
                    copy.write_row(
                        (
                            row["id"],
                            row["name"],
                            row["first_name"],
                            row["last_name"],
                            row["roll_no"],
                            row["email"],
                            row["password_hash"],
                            row["reset_otp"],
                            row["reset_otp_expires"],
                            row["department"],
                            row["semester"],
                        )
                    )
        pg_conn.commit()

        teachers = sqlite_conn.execute(
            """
            SELECT id, name, username, email, password_hash, reset_otp, reset_otp_expires
            FROM teachers
            ORDER BY id
            """
        ).fetchall()
        with pg_conn.cursor() as cur:
            with cur.copy(
                """
                COPY teachers(
                    id, name, username, email, password_hash, reset_otp, reset_otp_expires
                ) FROM STDIN
                """
            ) as copy:
                for row in teachers:
                    copy.write_row(
                        (
                            row["id"],
                            row["name"],
                            row["username"],
                            row["email"],
                            row["password_hash"],
                            row["reset_otp"],
                            row["reset_otp_expires"],
                        )
                    )
        pg_conn.commit()

        attendance_rows = sqlite_conn.execute(
            """
            SELECT id, student_id, attendance_date, subject, status
            FROM attendance_records
            ORDER BY id
            """
        ).fetchall()
        with pg_conn.cursor() as cur:
            with cur.copy(
                """
                COPY attendance_records(
                    id, student_id, attendance_date, subject, status
                ) FROM STDIN
                """
            ) as copy:
                for row in attendance_rows:
                    copy.write_row(
                        (
                            row["id"],
                            row["student_id"],
                            row["attendance_date"],
                            row["subject"],
                            row["status"],
                        )
                    )
        pg_conn.commit()

        reset_sequences(pg_conn)

        print(f"Migrated students: {len(students)}")
        print(f"Migrated teachers: {len(teachers)}")
        print(f"Migrated attendance_records: {len(attendance_rows)}")
    finally:
        sqlite_conn.close()
        pg_conn.close()


if __name__ == "__main__":
    migrate()
