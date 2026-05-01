from database.connection import get_connection
from models.rate import Rate


class RateRepository:

    def create(self, rate: Rate):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO parking.Rate (vehicle_type, cost_per_hour)
        VALUES (?, ?)
        """, rate.vehicle_type, rate.cost_per_hour)

        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_rate, vehicle_type, cost_per_hour
        FROM parking.Rate
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Rate(
                id_rate=row[0],
                vehicle_type=row[1],
                cost_per_hour=row[2]
            )
            for row in rows
        ]

    def get_by_id(self, id_rate):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_rate, vehicle_type, cost_per_hour
        FROM parking.Rate
        WHERE id_rate = ?
        """, id_rate)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Rate(
                id_rate=row[0],
                vehicle_type=row[1],
                cost_per_hour=row[2]
            )

        return None

    def get_by_vehicle_type(self, vehicle_type):
        vehicle_type = vehicle_type.strip().capitalize()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_rate, vehicle_type, cost_per_hour
        FROM parking.Rate
        WHERE vehicle_type = ?
        """, vehicle_type)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Rate(
                id_rate=row[0],
                vehicle_type=row[1],
                cost_per_hour=row[2]
            )

        return None