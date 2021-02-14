""" APIs useful functions."""
from datetime import datetime, timedelta, timezone
from marshmallow import post_load, post_dump, Schema, validates_schema, ValidationError
from marshmallow.fields import DateTime, Date


class DateRangeQuerySchema(Schema):
    """Basic marshmallow schema to handle query parameters for a range of dates.

    The start and end are optinals. If provided, we check that the start date occured
    before the end date.
    """

    start = Date(description="The start date ('YYYY-MM-DD')", example="2020-04-01")
    end = Date(description="The end date ('YYYY-MM-DD')", example="2020-04-01")

    @post_load
    def set_default(  # pylint: disable=no-self-use,unused-argument
        self, data, **kwargs
    ):
        """ Set default dates."""
        if "end" not in data:
            data["end"] = datetime.now(timezone.utc).date()

        if "start" not in data:
            data["start"] = data["end"] - timedelta(days=30)

        data["end"] = data["end"] + timedelta(days=1)

        return data

    @validates_schema
    def validate_date(  # pylint: disable=no-self-use,unused-argument
        self, data, **kwargs
    ):
        """ Validate date for query."""
        if data and "start" in data and "end" in data and data["start"] > data["end"]:
            raise ValidationError("The start date must be before the end date.")


class DatetimeRangeQuerySchema(Schema):
    """Basic marshmallow schema to handle query parameters for a range of datetimes.

    The start and end are optionals. If provided, we check that the start date occured
    before the end date.
    """

    start = DateTime(
        description="The start date in format ISO-8601, the parameter must be in UTC ('YYYY-MM-DDTHH:mm:SSZ') or contain a deltatime to reference the user timezone (YYYY-MM-DDTHH:mm:SS-+HH:mm)",  # pylint: disable=line-too-long # noqa
        example="2020-04-01T08:06:47.890+01:00",
    )

    end = DateTime(
        description="The end date in format ISO-8601, the parameter must be in UTC ('YYYY-MM-DDTHH:mm:SSZ') or contain a deltatime to reference the user timezone (YYYY-MM-DDTHH:mm:SS-+HH:mm)",  # pylint: disable=line-too-long # noqa
        example="2020-04-01T08:06:47.890+01:00",
    )

    @post_load
    def set_default(  # pylint: disable=no-self-use,unused-argument
        self, data, **kwargs
    ):
        """ Set default times."""
        if "start" not in data:
            data["start"] = datetime.now(timezone.utc)
        if "end" not in data:
            data["end"] = data["start"] + timedelta(days=5)

        # set end and start to UTC
        if data["start"].tzinfo == data["end"].tzinfo:
            if data["start"].tzinfo is not None:
                data["start"] = datetime.utcfromtimestamp(data["start"].timestamp())
                data["end"] = datetime.utcfromtimestamp(data["end"].timestamp())

        return data

    @validates_schema
    def validate_date(  # pylint: disable=no-self-use,unused-argument
        self, data, **kwargs
    ):
        """ Date validation for events."""
        if data and "start" in data and "end" in data and data["start"] > data["end"]:
            raise ValidationError("The start datetime must be before the end datetime.")

