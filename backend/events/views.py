from rest_framework import viewsets, filters, mixins
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend
from .models import EventType, EventCalculatorRequest
from .serializers import EventTypeSerializer, EventCalculatorRequestCreateSerializer, EventCalculatorRequestSerializer
from .services import send_event_request_email


class EventTypeViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = EventType.objects.filter(is_active=True)
    serializer_class = EventTypeSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['is_active']
    ordering_fields = ['order', 'title']
    ordering = ['order', 'title']

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['request'] = self.request
        return context


class EventCalculatorRequestViewSet(mixins.CreateModelMixin,
                                    mixins.ListModelMixin,
                                    mixins.RetrieveModelMixin,
                                    viewsets.GenericViewSet):

    queryset = EventCalculatorRequest.objects.all()
    parser_classes = [JSONParser]

    def get_serializer_class(self):
        if self.action == 'create':
            return EventCalculatorRequestCreateSerializer
        return EventCalculatorRequestSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        with transaction.atomic():
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            send_event_request_email(serializer.instance)
        out = EventCalculatorRequestSerializer(serializer.instance)
        return Response(out.data, status=status.HTTP_201_CREATED)
