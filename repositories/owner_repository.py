from database.connection import get_connection
from models.owner import Owner


class OwnerRepository:

    def create(self, owner: Owner):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO parking.Owner (type_dni, dni, name, last_name, correo, phone)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        owner.type_dni,
        owner.dni,
        owner.name,
        owner.last_name,
        owner.correo,
        owner.phone
        )

        conn.commit()
        conn.close()

    def update(self, owner: Owner):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE parking.Owner
        SET type_dni = ?, 
            dni = ?, 
            name = ?, 
            last_name = ?, 
            correo = ?, 
            phone = ?
        WHERE id_owner = ?
        """,
        owner.type_dni,
        owner.dni,
        owner.name,
        owner.last_name,
        owner.correo,
        owner.phone,
        owner.id_owner
        )

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_owner, type_dni, dni, name, last_name, correo, phone
        FROM parking.Owner
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Owner(
                id_owner=row[0],
                type_dni=row[1],
                dni=row[2],
                name=row[3],
                last_name=row[4],
                correo=row[5],
                phone=row[6]
            )
            for row in rows
        ]

    def get_by_dni(self, dni):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_owner, type_dni, dni, name, last_name, correo, phone
        FROM parking.Owner
        WHERE dni = ?
        """, dni)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Owner(
                id_owner=row[0],
                type_dni=row[1],
                dni=row[2],
                name=row[3],
                last_name=row[4],
                correo=row[5],
                phone=row[6]
            )

        return None

    def get_by_id(self, id_owner):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_owner, type_dni, dni, name, last_name, correo, phone
        FROM parking.Owner
        WHERE id_owner = ?
        """, id_owner)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Owner(
                id_owner=row[0],
                type_dni=row[1],
                dni=row[2],
                name=row[3],
                last_name=row[4],
                correo=row[5],
                phone=row[6]
            )

        return None