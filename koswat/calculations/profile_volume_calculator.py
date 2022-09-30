from koswat.profiles.koswat_profile import KoswatProfile


class ProfileVolumeCalculator:
    """
    TODO: This class (like many others) is still a work in progress.
    Not entirely sure yet which structure will be applied once we start using layers.
    """

    def calculate_total_volume(
        self, old_profile: KoswatProfile, new_profile: KoswatProfile
    ) -> float:
        _old_cross_section = old_profile.layers.base_layer
        _new_cross_section = new_profile.layers.base_layer
        _diff_polygon = _new_cross_section.geometry - _old_cross_section.geometry
        return _diff_polygon.area