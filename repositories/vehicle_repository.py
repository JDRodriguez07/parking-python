from database.connection import get_connection
from models.vehicle import Vehicle


class VehicleRepository:

    def create(self, vehicle: Vehicle):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO parking.Vehicle (id_owner, id_rate, plate)
        VALUES (?, ?, ?)
        """,
        vehicle.id_owner,
        vehicle.id_rate,
        vehicle.plate
        )

        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_vehicle, id_owner, id_rate, plate
        FROM parking.Vehicle
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Vehicle(
                id_vehicle=row[0],
                id_owner=row[1],
                id_rate=row[2],
                plate=row[3]
            )
            for row in rows
        ]

    def get_by_plate(self, plate):
        plate = plate.strip().upper()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_vehicle, id_owner, id_rate, plate
        FROM parking.Vehicle
        WHERE plate = ?
        """, plate)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Vehicle(
                id_vehicle=row[0],
                id_owner=row[1],
                id_rate=row[2],
                plate=row[3]
            )

        return None

    def get_by_id(self, id_vehicle):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_vehicle, id_owner, id_rate, plate
        FROM parking.Vehicle
        WHERE id_vehicle = ?
        """, id_vehicle)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Vehicle(
                id_vehicle=row[0],
                id_owner=row[1],
                id_rate=row[2],
                plate=row[3]
            )

        return None

    def get_by_owner_id(self, id_owner):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_vehicle, id_owner, id_rate, plate
        FROM parking.Vehicle
        WHERE id_owner = ?
        """, id_owner)

        rows = cursor.fetchall()
        conn.close()

        return [
            Vehicle(
                id_vehicle=row[0],
                id_owner=row[1],
                id_rate=row[2],
                plate=row[3]
            )
            for row in rows
        ]

    def update_plate(self, id_vehicle, new_plate):
        new_plate = new_plate.strip().upper()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE parking.Vehicle
        SET plate = ?
        WHERE id_vehicle = ?
        """, new_plate, id_vehicle)

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    def update_owner(self, id_vehicle, id_owner):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE parking.Vehicle
        SET id_owner = ?
        WHERE id_vehicle = ?
        """, id_owner, id_vehicle)

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    def get_with_rate_by_plate(self, plate):
        plate = plate.strip().upper()

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT 
            v.id_vehicle,
            v.id_owner,
            v.id_rate,
            v.plate,
            r.cost_per_hour
        FROM parking.Vehicle v
        INNER JOIN parking.Rate r ON v.id_rate = r.id_rate
        WHERE v.plate = ?
        """, plate)

        row = cursor.fetchone()
        conn.close()

        if row:
            return {
                "id_vehicle": row[0],
                "id_owner": row[1],
                "id_rate": row[2],
                "plate": row[3],
                "cost_per_hour": row[4]
            }

        return None