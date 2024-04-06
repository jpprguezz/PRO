# **************
# DONANDO SANGRE
# **************


def run(age: int, weight: int, heartbeat: int, platelets: int) -> bool:
    if age >= 65:
        suitable_for_donation = False
    else:
        suitable_for_donation = True

    if weight >= 50:
        suitable_for_donation = True
    else:
        suitable_for_donation = False

    if 50 <= heartbeat <= 100:
        suitable_for_donation = False
    else:
        suitable_for_donation = True

    if platelets > 150000:
        suitable_for_donation = True
    else:
        suitable_for_donation = False

    return suitable_for_donation


if __name__ == '__main__':
    run(34, 81, 70, 151000)