from marshmallow_jsonapi import Schema, fields

field_map = {
        'string': fields.String,
        'integer': fields.Integer,
        'datetime': fields.DateTime,
        'boolean': fields.Boolean,
        'time': fields.Time,
        'formatted_string': fields.FormattedString,
        'float': fields.Float,
        'local_date_time': fields.LocalDateTime,
        'date': fields.Date,
        'url': fields.Url,
        'email': fields.Email,
        'function': fields.Function,
        'array': fields.List,
        }


class ResourceSchemaFactory:
    def create_schema(resource_name, schemas):


        class ResourceSchema(Schema):
            id = fields.String()
            class Meta:
                type_ = resource_name

        resource_schema = ResourceSchema()
        for name, des in schemas['properties'].items():
            field_type = des['type']
            field_obj = None
            if field_type == 'array':
                field_obj = field_map[field_type](
                        field_map[des['items']['type']]
                        )
            else:
                field_obj = field_map[field_type]()

            if name in schemas['required']:
                field_obj.required = True
            
            resource_schema.fields[name] = field_obj
            resource_schema.declared_fields[name] = field_obj

        return resource_schema

