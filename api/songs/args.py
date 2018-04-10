from webargs import fields, validate

songs_args = {
    #required arguments and their validations
    'title':fields.Str(required=True, validate=validate.Length(3)),
    'artist':fields.Str(required=True, validate=validate.Length(3))
}

songs_id_arg = {
    'id':fields.Int()
}