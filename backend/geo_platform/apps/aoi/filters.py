from rest_framework_gis.filters import DistanceToPointOrderingFilter


class _DistanceToPointOrderingFilter(DistanceToPointOrderingFilter):
    def get_schema_operation_parameters(self, view) -> list:
        return [
            {
                "name": self.order_param,
                "required": False,
                "in": "query",
                "description": "",
                "schema": {
                    "type": "enum",
                    "items": {"type": "string", "enum": ["asc", "desc"]},
                    "example": "desc",
                },
                "style": "form",
                "explode": False,
            }
        ]
