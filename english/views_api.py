import csv
import io
import random
import traceback

from django.core.handlers.wsgi import WSGIRequest
from django.http import FileResponse, HttpResponse, HttpResponseServerError
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfgen import canvas
from reportlab.pdfgen.canvas import Canvas
from reportlab.platypus import SimpleDocTemplate, TableStyle
from reportlab.platypus.tables import Table
from rest_framework.views import APIView

from services.english_test_generator import EngTestGenerator
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

inch = 72.0
cm = inch / 2.54
mm = cm * 0.1
pica = 12.0


class EnglishTestPDFGeneratorAPIView(APIView):
    def post(self, request: WSGIRequest, *args, **kwargs):
        try:
            word_data = EngTestGenerator.generate_by_google_sheet_url(
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

            # kor = Korean: 'HYSMyeongJoStd-Medium', 'HYGothic-Medium'

            doc = SimpleDocTemplate(
                response,
                rightMargin=1 * cm,
                leftMargin=1 * cm,
                topMargin=1 * cm,
                bottomMargin=1 * cm,
            )

            # 테이블 스타일 지정 2,3 번째 튜플 데이터는 해당 스타일의 적용 범위를 의미함 (cell 주소)
            # 모든 cell 에 스타일을 적용하려면 (0, 0), (-1, -1) 사용하면 됨
            table_style = TableStyle(
                [
                    ("FONT", (0, 0), (-1, -1), "HYSMyeongJoStd-Medium"),
                    ("FONTSIZE", (0, 0), (-1, -1), 20),
                    ("BOTTOMPADDING", (0, 0), (-1, -1), 15),
                    ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black),  # 테이블 내부 구분선
                    ("BOX", (0, 0), (-1, -1), 0.25, colors.black),  # 테이블 외곽선
                ]
            )

            # table = Table(value_list[:questionCount], colWidths=270, rowHeights=79)

            value_list = [
                [1, "hello", "안녕하세요", 2, "dead", "죽었다"],
                [1, "hello", "안녕하세요", 2, "dead", "죽었다"],
            ]
            table = Table(
                data=value_list,
                colWidths=[50, 100, 150, 50, 100, 150],
                rowHeights=35,
                hAlign="CENTER",
            )
            table.setStyle(table_style)

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
