<div align="center">

![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/night-works/sundata/python-app.yml?style=for-the-badge)
![Codecov branch](https://img.shields.io/codecov/c/gh/night-works/sundata/main?style=for-the-badge)
![Sonar Quality Gate](https://img.shields.io/sonar/quality_gate/night-works_sundata?server=https%3A%2F%2Fsonarcloud.io&style=for-the-badge)
![GitHub](https://img.shields.io/github/license/night-works/sundata?color=gre&style=for-the-badge)

</div>

# Sun Data

Simple module to get the angle of the Sun relative to the Horizon for a given geographic location and datetime. Also
allow for the gathering of sunrise and sunset for a given geographical location and datetime, with the option to shift
those to general lighting conditions rather than sunset but instead Astro Night, Night for example.

## Features

- Angle of Sun for given location and date time
- Get modified datetime for location when sun enters different lighting conditions

## Installing

Install using pip into your python virtual environment.

```console
pip install sundata
```

## Usage

Before using sundata to get the lighting information you'll require a location __latitude__ and __longitude__ as well a
datetime in order to perform the calculation.

To get only the sunrise and sunset for a given date time the following will be enough.

```python
position = Position(51.772938, 0.102310)
a_date = datetime(2023, 2, 13, 12, 00)
data = SunData(position, a_date)
data.calculate_sun_data()
sunrise = data.sunrise
sunset = data.sunset
```

To get the lighting periods around sunrise and sunset then a __LightPeriod__ needs to be passed into the calculation
method.

```python
pos = Position(51.772938, 0.102310)
current_datetime = datetime(2023, 2, 12, 17, 7)
data = SunData(position, current_datetime)
data.calculate_sun_data(LightPeriod.NIGHT)
sunrise = data.sunrise
sunset = data.sunset
```

Sunset and Sunrise datetimes have now been shifted to the start of Night and end of Night.

## Running Tests

Module uses pytest and pytest-cov for coverage. To run the tests

```console
pytest 
```

To run the tests with coverage

```console
pytest --cov=src
```

## Contributing

Please first raise an issue then fork the repository referencing the issue in commits and raise a Pull Request.

## Acknowledgements

- [Link](https://example.com)
- [Link](https://example.com)
- [Link](https://example.com)

## License

Licensed under the MIT.
Copyright 2023 Night Works. [Copy of the license](LICENCE).

A list of the Licenses of the dependencies of the project can be found at
the bottom of the [Libraries Summary](https://libraries.io/pypi/sundata).

