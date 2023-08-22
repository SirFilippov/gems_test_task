import logging
from datetime import datetime

from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import render
from rest_framework.response import Response
from django.db import connection

from .serializers import DealSerializer, UserSerializer
from rest_framework.views import APIView
from .models import Deal


class DealsAPIView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, requset):
        Deal.objects.all().delete()
        try:
            csvfile = requset.FILES['file']
            if not csvfile.name.endswith('.csv'):
                raise TypeError('Проверьте расширение файла')
            import csv
            csv_data = csvfile.read().decode('utf-8')
            print(1)
            csv_data = list(csv.reader(csv_data.splitlines()))[1:]
            print(2)
            for row in csv_data:
                print(row)
                if len(row) == 1:
                    row = row[0].split(',')
                    print(row)
                else:
                    break
                deal_data = {
                    'customer': row[0],
                    'stone_type': row[1],
                    'total_price': int(row[2]),
                    'quantity': int(row[3]),
                    'date': datetime.strptime(row[4], '%Y-%m-%d %H:%M:%S.%f')
                }
                print(4)
                serializer = DealSerializer(data=deal_data)
                print(5)
                if serializer.is_valid(raise_exception=True):
                    print(6)
                    serializer.save()
                    print(7)
            return Response({'Status': 'Ok'})
        except Exception as e:
            print(logging.exception(e))
            return Response({'Status': 'Error',
                             'Desc': f'{e}'})

    def get(self, request):
        queryset = self.custom_raw_query()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def custom_raw_query(self):
        raw_query = """
        SELECT customer, SUM(total_price) AS spent_money, GROUP_CONCAT(DISTINCT stone_type) AS gems
        FROM general_deal
        WHERE customer IN (
            SELECT customer
            FROM general_deal
            GROUP BY customer
            ORDER BY SUM(total_price) DESC
            LIMIT 5
        )
        AND stone_type IN (
            SELECT stone_type
            FROM general_deal
            WHERE customer IN (
                SELECT customer
                FROM general_deal
                GROUP BY customer
                ORDER BY SUM(total_price) DESC
                LIMIT 5
            )
            GROUP BY stone_type
            HAVING COUNT(DISTINCT customer) >= 2
        )
        GROUP BY customer
        ORDER BY spent_money desc
        """

        # Выполнение сырого SQL-запроса
        with connection.cursor() as cursor:
            cursor.execute(raw_query)

            # Получение результатов (если нужно)
            results = cursor.fetchall()

        list_result = []
        for i in results:
            list_result.append({'username': i[0],
                                'spent_money': i[1],
                                'gems': i[2]})

        return list_result


def home_page(request):
    return render(request, template_name='home_page.html', context=None)
