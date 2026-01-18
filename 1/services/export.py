import csv
from io import StringIO
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

from bot.models.order import Order

class ExportService:
    @staticmethod
    def orders_to_csv(orders: list[Order]) -> str:
        buffer = StringIO()
        writer = csv.writer(buffer)
        writer.writerow(["id", "client_id", "status"])
        for o in orders:
            writer.writerow([o.id, o.client_id, o.status])
        return buffer.getvalue()

    @staticmethod
    def orders_to_pdf(path: str, orders: list[Order]):
        doc = SimpleDocTemplate(path)
        styles = getSampleStyleSheet()
        content = []

        content.append(Paragraph("РћС‚С‡С‘С‚ РїРѕ Р·Р°РєР°Р·Р°Рј", styles["Title"]))
        for o in orders:
            content.append(
                Paragraph(
                    f"Р—Р°РєР°Р· #{o.id} | РљР»РёРµРЅС‚ {o.client_id} | {o.status}",
                    styles["Normal"],
                )
            )

        doc.build(content)

