from rest_framework import status, viewsets
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response

from .documentation import booking_schema, room_schema
from .models import Booking, Room
from .serializers import BookingSerializer, RoomSerializer


@room_schema
class RoomViewSet(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    filter_backends = (OrderingFilter,)
    ordering_fields = ("id", "price")
    ordering = ("id",)


@booking_schema
class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def list(self, request, *args, **kwargs):
        room_id = request.query_params.get("room_id")

        if not room_id:
            return Response(
                {"error": "Необходимо указать room_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        self.queryset = self.queryset.filter(room_id=room_id).order_by("date_start")

        return super().list(request, *args, **kwargs)
