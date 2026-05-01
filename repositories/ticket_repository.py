from database.connection import get_connection
from models.ticket import Ticket


class TicketRepository:

    def create(self, ticket: Ticket):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO parking.Ticket (id_vehicle, entry_time, exit_time, total_price)
        VALUES (?, ?, ?, ?)
        """,
        ticket.id_vehicle,
        ticket.entry_time,
        ticket.exit_time,
        ticket.total_price
        )

        conn.commit()
        conn.close()

    def get_all(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_ticket, id_vehicle, entry_time, exit_time, total_price
        FROM parking.Ticket
        """)

        rows = cursor.fetchall()
        conn.close()

        return [
            Ticket(
                id_ticket=row[0],
                id_vehicle=row[1],
                entry_time=row[2],
                exit_time=row[3],
                total_price=row[4]
            )
            for row in rows
        ]

    def get_by_id(self, id_ticket):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_ticket, id_vehicle, entry_time, exit_time, total_price
        FROM parking.Ticket
        WHERE id_ticket = ?
        """, id_ticket)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Ticket(
                id_ticket=row[0],
                id_vehicle=row[1],
                entry_time=row[2],
                exit_time=row[3],
                total_price=row[4]
            )

        return None

    def get_open_ticket_by_vehicle(self, id_vehicle):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT id_ticket, id_vehicle, entry_time, exit_time, total_price
        FROM parking.Ticket
        WHERE id_vehicle = ?
        AND exit_time IS NULL
        """, id_vehicle)

        row = cursor.fetchone()
        conn.close()

        if row:
            return Ticket(
                id_ticket=row[0],
                id_vehicle=row[1],
                entry_time=row[2],
                exit_time=row[3],
                total_price=row[4]
            )

        return None

    def close_ticket(self, id_ticket, exit_time, total_price):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE parking.Ticket
        SET exit_time = ?, total_price = ?
        WHERE id_ticket = ?
        """,
        exit_time,
        total_price,
        id_ticket
        )

        conn.commit()
        rows_affected = cursor.rowcount
        conn.close()

        return rows_affected > 0

    def get_all_with_details(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        SELECT
            t.id_ticket,
            v.plate,
            r.vehicle_type,
            (o.name + ' ' + o.last_name) AS owner_full_name,
            o.phone,
            t.entry_time,
            t.exit_time,
            t.total_price,
            CASE 
                WHEN t.exit_time IS NULL THEN 'Abierto'
                ELSE 'Cerrado'
            END AS status
        FROM parking.Ticket t
        INNER JOIN parking.Vehicle v ON t.id_vehicle = v.id_vehicle
        INNER JOIN parking.Rate r ON v.id_rate = r.id_rate
        INNER JOIN parking.Owner o ON v.id_owner = o.id_owner
        ORDER BY t.id_ticket DESC
        """)

        rows = cursor.fetchall()
        conn.close()

        return rows