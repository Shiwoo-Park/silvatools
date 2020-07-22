import csv
import io
import random
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import FileResponse, HttpResponse, HttpResponseServerError
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.tables import Table
from rest_framework.views import APIView

from services.english_test_generator import EngTestGenerator

cm = 2.54


class EnglishTestPDFGeneratorAPIView(APIView):
    def post(self, request: WSGIRequest, *args, **kwargs):
        try:
            word_data = EngTestGenerator.generate_by_url(
                request.POST["url"],
                int(request.POST["startIdx"]),
                int(request.POST["endIdx"]),
            )
            value_list = list(word_data.values())
            random.shuffle(value_list)
            questionCount = int(request.POST["questionCount"])

            response = HttpResponse(content_type="application/pdf")
            response["Content-Disposition"] = "attachment; filename=somefilename.pdf"
            elements = []

            doc = SimpleDocTemplate(
                response,
                rightMargin=0,
                leftMargin=6.5 * cm,
                topMargin=0.3 * cm,
                bottomMargin=0,
            )

            table = Table(value_list[:questionCount], colWidths=270, rowHeights=79)
            elements.append(table)
            doc.build(elements)

            return response

        except Exception as e:
            return HttpResponseServerError(traceback.format_exc())


class DownloadPDFTestAPIView(APIView):
    def get2(self, request, *args, **kwargs):
        buffer = io.BytesIO()
        canvas = Canvas(buffer)

        # 내용을 채운다
        canvas.drawString(40, 40, "canvas.drawString")
        canvas.drawAlignedString(40, 80, "canvas.drawAlignedString")
        canvas.drawCentredString(40, 120, "canvas.drawCentredString")

        canvas.showPage()
        canvas.save()

        file_name = "hello.pdf"
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=file_name)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = "attachment; filename=somefilename.pdf"

        elements = []

        doc = SimpleDocTemplate(
            response,
            rightMargin=0,
            leftMargin=6.5 * cm,
            topMargin=0.3 * cm,
            bottomMargin=0,
        )

        data = [(1, 2), (3, 4)]
        table = Table(data, colWidths=270, rowHeights=79)
        elements.append(table)
        doc.build(elements)
        return response


def some_view(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(["First row", "Foo", "Bar", "Baz"])
    writer.writerow(["Second row", "A", "B", "C", '"Testing"', "Here's a quote"])

    return response
