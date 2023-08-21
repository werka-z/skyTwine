def assign_sky_condition(d1, d2):
    d1, d2 = d1.lower(), d2.lower()

    if d1 == d2:
        return assign_image(d1)

    if ("clear" in d1 or "sun" in d1) and ("clear" in d2 or "sun" in d2):
        return "clear sky"

    # Sun and Clouds
    if ("clear" in d1 and "clouds" in d2) or ("clouds" in d1 and "clear" in d2):
        return "partly cloudy"

    # Sun and Rain (sun shower)
    if ("clear" in d1 and "rain" in d2) or ("rain" in d1 and "clear" in d2):
        return "showers"

    # Snow
    if "snow" in d1 or "snow" in d2:
        return "snow"

    # Mist or Fog
    if ("mist" in d1 or "mist" in d2) or ("fog" in d1 or "fog" in d2):
        return "fog"

    # Storm
    if "storm" in d1 or "storm" in d2:
        return "storm"

    return "partly cloudy"


def assign_image(description):
    description = description.lower()
    if "few" in description:
        return "static/icons/few_clouds.png"
    if "clear" in description or "sun" in description:
        return "static/icons/sun.png"
    if "cloud" in description:
        return "static/icons/cloud.png"
    if "rain" in description:
        return "static/icons/rain.png"
    if "snow" in description:
        return "static/icons/snow.png"
    if "storm" in description:
        return "static/icons/storm.png"
    if "mist" in description or "fog" in description:
        return "static/icons/fog.png"
    return "static/icons/sun_behind_cloud.png"
